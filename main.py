import json
import logging
from utils import llm_response
from decouple import config
from find_apis import search
from codebox import CodeInterpreter
from uuid import uuid4

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

codebox = CodeInterpreter()
def execute_code(code):
    return codebox.execute_code(code)['output']

def search_apis(documentation_url, api_question):
    tool_response = search(documentation_url, api_question, 10)
    tool_response = tool_response["relevant_apis"]
    return json.dumps(tool_response, indent=4)

uuid = uuid4().hex

QUESTION = "Give me the list of images from markdown files present in the given github repo"
# QUESTION = "Give me the list of tables from markdown files present in the given github repo"

CONNECTOR_NAME = "Github"
DOCUMENTATION_URL = "https://docs.github.com/en/rest?apiVersion=2022-11-28"

# GITHUB_REPO = "https://github.com/shroominic/codeinterpreter-api"
GITHUB_REPO = "https://github.com/run-llama/llama_index/tree/main"

logging.info(f"UUID: {uuid}")
logging.info(f"Question: {QUESTION}")
logging.info(f"Connector Name: {CONNECTOR_NAME}")
logging.info(f"Documentation URL: {DOCUMENTATION_URL}")
logging.info(f"GitHub Repo: {GITHUB_REPO}")

system_prompt = """

You are a solution implementation expert and a python programmer.
Trump, from the business team, has given you a task and you need to solve that by building and testing a python code.
You have access to certain tools [`search_apis()`, `execute_code()`] which you can use multiple times.

You may breakdown the task into multiple subtasks and attempt to solve it step-by-step.


You have access to following tools:
1. search_apis():
    ```
    Search for relevant APIs by crawling documentation URL and sub-URLs related to task/sub-task.

    Parameters:
        documentation_url (str): Initial URL of the documentation to start the search.
        api_question (str): Question or topics to query APIs for.

    Returns:
        list of dicts: Each dict contains details about an API related to the question. 
        Example structure:
            {
                "name": str,                    # Name of the API
                "method": str,                  # HTTP method (e.g., GET, POST)
                "endpoint": str,                # Endpoint URL
                "description": str,             # Description of the API
                "curl_request_example": str,    # Example curl request
                "sample_response": str,         # Sample response in JSON format
                "headers": list of dicts,       # List of headers for the API request
                "path_parameters": list of dicts, # List of path parameters
                "query_parameters": list of dicts, # List of query parameters
                "documentation": str            # URL of the API documentation
            }
    ```

2. execute_code():
    ```
    Execute a piece of Python code in a persistent Jupyter Notebook and return the result.

    Parameters:
        code (str): The Python code to be executed.

    Returns:
        str: The output of the executed code.
    ```
"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_apis",
            "description": "Search for relevant APIs by crawling documentation URL and sub-URLs related to task/sub-task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "documentation_url": {
                        "type": "string",
                        "description": "Initial URL of the documentation to start the search.",
                    },
                    "api_question": {
                        "type": "string",
                        "description": "Question or topics to query APIs for.",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_code",
            "description": "Execute a piece of Python code in a persistent Jupyter Notebook and return the result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Python code to be executed.",
                    },
                },
            },
        },
    },
]

user_prompt = f"""Task: `{QUESTION}`.
DOCUMENTATION_URL: {DOCUMENTATION_URL}
Github Repo URL: {GITHUB_REPO}
So, first, break down the task into multiple steps and search for find relevant APIs from the {CONNECTOR_NAME}'s documentation.
then, build code to complete the task."""

messages = []
messages.append({'role': 'system', 'content': system_prompt})
messages.append({'role': 'user', 'content': user_prompt})


while True:
    response = llm_response(
        user_message=messages,
        tools=tools,
        temperature=0,
        # temperature=0.5,
        # model_name='gpt-4o'
        model_name="gpt-4o-mini",
    )

    if type(response) == dict:
        ## Tool called
        tool_calls = response["response"]
        messages.append(tool_calls)
        tool_calls = tool_calls.tool_calls

        function_name = tool_calls[0].function.name
        arguments = json.loads(tool_calls[0].function.arguments)

        logging.info(f"Calling **{function_name}** tool. Arguments:")
        for k, v in arguments.items():
            logging.info(f"{k}: {v}")
        
        logging.info('-------Tool Running-----------')
        tool_response = globals().get(function_name)(**arguments)
        logging.info('-------Tool Completed-----------')
        logging.info(tool_response)

        function_call_result_message = {
            "role": "tool",
            "content": tool_response,
            "tool_call_id": tool_calls[0].id,
        }

        messages.append(function_call_result_message)

    else:
        logging.info('=========================================')
        logging.info('---------------Final Answer--------------')
        logging.info(response)
        break
    
    logging.info('######### Next LLM Call ##################')

print('=========================================')
print('UUID', uuid)
print('Question', QUESTION)
print('---------------Final Answer--------------')
print(response)

codebox.export_to_py(f'outputs/tmp-{uuid}.py')
codebox.export_to_ipynb(f'outputs/tmp-{uuid}.ipynb')