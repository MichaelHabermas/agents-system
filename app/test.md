Creating a Python script that generates other Python scripts can be done by writing a function that takes parameters for the content of the new script and then writes that content to a file. Below is an example of such a script:

```python
def create_python_script(script_name, script_content):
    with open(script_name, 'w') as file:
        file.write(script_content)
    print(f\"Script '{script_name}' created successfully.\")

# Example usage
script_name = 'generated_script.py'
script_content = \"\"\"
def hello_world():
    print(\"Hello, world!\")

if __name__ == \"__main__\":
    hello_world()
\"\"\"

create_python_script(script_name, script_content)
```

### Explanation:
- The `create_python_script` function takes two arguments: `script_name` (the name of the new script file) and `script_content` (the content to be written to the script).
- It opens a file with the specified name in write mode and writes the content to it.
- Finally, it prints a confirmation message.

You can modify the `script_content` variable to generate different scripts as needed.

