from typing import Annotated, Any, Dict, List, Optional, Sequence, TypedDict
import functools
import operator

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_experimental.tools import PythonREPLTool
from langgraph.graph import StateGraph, END

from dotenv import load_dotenv
import os

load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

tavily_tool = TavilySearchResults(max_results=5)

python_repl_tool = PythonREPLTool()

members = ["Poetry Writer", "Researcher", "Coder", "Reviewer", "QA Tester"]

system_prompt = (
    f"You are a supervisor agent tasked with managing the conversation between"
    f" the following members: {members}. Based on the following user request,"
    f" respond with the worker to act next. Each worker will preform a task and"
    f" respond with their results and status. When finished, then respond with FINISH."
)
options = members + ["FINISH"]

function_def = {
    "name": "route",
    "description": "Select the next role.",
    "parameters": {
        "title": "routeSchema",
        "type": "object",
        "properties": {
            "next": {
                "title": "Next",
                "anyOf": [{"enum": options}],
                "default": "Supervisor"
            }
        },
        "required": ["next"],
    },
}

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            f"system",
            f"Given the conversation above, who should act next?"
            f" Or should we FINISH? Select one of: {options}",
        ),
    ]
).partial(options=str(options), members=", ".join(members))

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key)
poetry_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5, openai_api_key=openai_api_key)

supervisor_chain = (
    prompt
    | llm.bind_functions(functions=[function_def], function_call="route")
    | JsonOutputFunctionsParser()
)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor


def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}


research_agent = create_agent(llm, [tavily_tool], "You are a web researcher agent.")
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")

code_agent = create_agent(
    llm,
    [python_repl_tool],  # DANGER: This tool executes code locally. Use with caution.
    "You may generate safe Python code to analyze data with pandas and generate charts using matplotlib.",
)
code_node = functools.partial(agent_node, agent=code_agent, name="Coder")

review_agent = create_agent(
    llm,
    [tavily_tool],
    """You are a senior developer. You excel at code reviews.
    You give detailed and specific actionable feedback.
    You are not rude, but you don't worry about being polite either.
    Instead you just communicate directly about the technical review.
    """,
)
review_node = functools.partial(agent_node, agent=research_agent, name="Reviewer")

test_agent = create_agent(
    llm,
    [python_repl_tool],  # DANGER: This tool executes code locally. Use with caution.
    "You may generate safe Python code to test functions and classes using unittest or pytest.",
)
test_node = functools.partial(agent_node, agent=test_agent, name="QA Tester")

poetry_agent = create_agent(poetry_llm, [tavily_tool], "You are to write a short poem based upon the input given in the style of Dr Seuss")
poetry_node = functools.partial(agent_node, agent=poetry_agent, name="Poetry Writer")

workflow = StateGraph(AgentState)
workflow.add_node("Reviewer", review_node)
workflow.add_node("Researcher", research_node)
workflow.add_node("Coder", code_node)
workflow.add_node("QA Tester", test_node)
workflow.add_node("Poetry Writer", poetry_node)
workflow.add_node("supervisor", supervisor_chain)


for member in members:
    workflow.add_edge(member, "supervisor")

conditional_map = {k: k for k in members}
conditional_map["FINISH"] = END
workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)

workflow.set_entry_point("supervisor")

graph = workflow.compile()
