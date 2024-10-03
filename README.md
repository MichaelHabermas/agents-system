# AI School Architect

## Overview
In this project, we developed AI School Architect to orchestrate AI agents performing various tasks such as research, code review, testing, and coding. This setup enhances productivity by delegating specific tasks to specialized agents, streamlining workflows, and ensuring accuracy and efficiency.

### Set up environment variables:
- Copy the sample environment file:
  ```bash
  cp .env.sample .env
  ```
- Edit the `.env` file:
  ```
  OPENAI_API_KEY=your-openai-key
  LANGCHAIN_API_KEY=your-langchain-key
  LANGCHAIN_TRACING_V2=true
  LANGCHAIN_PROJECT=24a6_6_3
  TAVILY_API_KEY=your-tavily-key
  ```
## Docker
1. Run the agent supervisor with Docker:
   ```
   docker compose up
   ```

## Now It's Your Turn!
Embrace your creativity and personalize this project to craft a solution that uniquely addresses the challenges and inefficiencies you face in your own educational or professional environment. After seeing what our AI agents can do, it’s time for you to take the reins. Use the foundation we’ve built and apply it to a challenge you face in your own context. Here’s how you can get started:

## Minimum Requirements
- **Custom Agent Creation:** Develop new custom agents to match your specific workflow needs. This could include automating repetitive tasks, integrating with specific APIs, or creating specialized commands that you frequently use.

## Stretch Goals
- **Advanced Task Automation:** Enhance the agents to perform more complex tasks such as data analysis, report generation, and project management.
- **Context-Aware Assistance:** Develop features that enable the agents to understand the context of tasks better, offering more accurate suggestions and task executions based on the current project structure and standards.
- **Collaboration Features:** Implement tools that facilitate better collaboration among team members, such as task assignment automation, integration with project management tools, and real-time collaboration features.
- **Continuous Improvement:** Integrate the agents with feedback loops to learn from their actions and improve their performance over time, providing more personalized and relevant assistance as you continue to use them.

## Privacy and Submission Guidelines
- **Submission Requirements:** Please submit a link to your public repo with your implementation or a Loom video showcasing your work on the BloomTech AI Platform.
- **Sensitive Information:** If your implementation involves sensitive information, you are not required to submit a public repository. Instead, a detailed review of your project through a Loom video is acceptable, where you can demonstrate the functionality and discuss the technologies used without exposing confidential data.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.