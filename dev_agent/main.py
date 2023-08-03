from dotenv import load_dotenv
import os
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.agents import initialize_agent, AgentType, Tool
import subprocess

load_dotenv()


DEVELOPER_TEMPLATE = """
    You're an experienced software engineer.
    Your expertise is software architecture, and Python.

    Your task is to take the specifications of a software and build that
    software in Python language (3.10), in a well architected way, with correct typing,
    and dependencies managed by Poetry.
    
    Don't forget to add:
    - 'README.md' with instructions to launch and test.
    - '__init__.py' in modules.
    - Automatic tests that could be launched by 'poetry run pytest tests'.
    - The code of the app should be inside a directory called 'app'.

    Specifications:
    {{{{{{
    {specifications}
    }}}}}}

    Please, use Poetry to init the code base and install the dependencies,
    and create all necessary files.
"""

developer_prompt = PromptTemplate(
    input_variables=["specifications"],
    template=DEVELOPER_TEMPLATE,
)


llm = ChatOpenAI(model="gpt-4", temperature=0.2)

working_directory = os.path.abspath("workdir")
print(f"Working directory: {working_directory}")

def run_poetry(working_directory, arguments):
    # Prepare the command
    command = ["poetry"] + arguments.split()

    # Run the command
    result = subprocess.run(command, cwd=working_directory, text=True, capture_output=True)

    # Save the output and error indicator
    stdout_output = result.stdout
    stderr_output = result.stderr
    #error_occurred = result.returncode != 0

    return stdout_output + "\n\n" + stderr_output

poetry_tool = Tool(
    name = "Poetry",
    func=lambda arguments: run_poetry(working_directory, arguments),
    description="Useful to run poetry commands in the code repository. Input should be the parameters of the call, like 'add pytest -D', or 'init'."
)

developer_tools = FileManagementToolkit(
    root_dir=str(working_directory),
    selected_tools=[
        "write_file",
    ],
).get_tools()

developer_tools += [poetry_tool]

developer_agent = initialize_agent(
    developer_tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
)

def develop(specifications):
    developer_agent.run(developer_prompt.format(specifications=specifications))

print(len(developer_tools), 'tools')

develop("Create an API REST service for a fully operative to-do list app, with add tasks, remove task, etc.")


def run_pytest(working_directory):
    # Install command
    command = ["poetry", "install"]
    result = subprocess.run(command, cwd=working_directory, text=True, capture_output=True)

    # Run tests
    command = ["poetry", "run", "pytest", "tests"]
    result = subprocess.run(command, cwd=working_directory, text=True, capture_output=True)

    # Save the output and error indicator
    stdout_output = result.stdout
    stderr_output = result.stderr
    error_occurred = result.returncode != 0

    return stdout_output + "\n\n" + stderr_output, error_occurred


def generate_program_context(working_directory):
    file_dict = {}

    # Define encodings to try
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'windows-1252']

    # Walk through the working directory
    for dirpath, dirnames, filenames in os.walk(working_directory):
        # Ignore directories that start with a dot or are named __pycache__
        dirnames[:] = [d for d in dirnames if not d[0] == '.' and d != '__pycache__']

        for filename in filenames:
            if filename in ('poetry.lock',):
                continue

            filepath = os.path.join(dirpath, filename)

            content = None
            for encoding in encodings:
                try:
                    # Open each file and read its contents
                    with open(filepath, 'r', encoding=encoding) as file:
                        content = file.read()
                    break
                except UnicodeDecodeError:
                    continue

            # Check if content could not be decoded
            if content is None:
                print(f'Could not decode {filepath}. Skipping.')
                continue

            # Make the path relative to the working directory
            relative_path = os.path.relpath(filepath, working_directory)

            # Add the content to the dictionary, using the relative path as the key
            file_dict[relative_path] = content

    files_context = "\n".join([
        f"{file_name} = \n{{{{{{\n{file_content}\n}}}}}}\n\n"
        for file_name, file_content in file_dict.items()
    ])

    return files_context


files_context = generate_program_context(working_directory)
print(files_context)


DEBUG_TEMPLATE = """
    You're an experienced software engineer.
    Your expertise is software architecture, and Python.

    Your task is to fix a software written in Python language (3.10).
    In case there are too much errors, focus on solving only one.
    
    Files:
    
    {files}
    
    Error:
    {{{{{{
    {error_output}
    }}}}}}

    Please, use the tools to create or write the files as needed,
    and the Poetry command to manage the dependencies.
"""


debug_prompt = PromptTemplate(
    input_variables=["files", "error_output"],
    template=DEBUG_TEMPLATE,
)

debug_tools = FileManagementToolkit(
    root_dir=str(working_directory),
    selected_tools=[
        "read_file", "write_file", "move_file", "file_delete", "list_directory",
    ],
).get_tools()

debug_tools += [poetry_tool]


debug_agent = initialize_agent(
    debug_tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
)


def debug():
    output, error_ocurred = run_pytest(working_directory)
    
    if not error_ocurred:
        return
    
    files_context = generate_program_context(working_directory)

    debug_agent.run(debug_prompt.format(files=files_context, error_output=output))
