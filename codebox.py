import json
import logging
from codeboxapi import CodeBox
from decouple import config

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CodeInterpreter:
    def __init__(self):
        # Initialize the CodeBox API client with the provided API key
        self.codebox = CodeBox(api_key=config('CODEBOX_API_KEY'))
        self.history = []  # To keep track of all inputs and outputs

    def execute_code(self, code: str):
        """
        Execute a piece of Python code, store input and output, and return the result.

        Parameters:
            code (str): The Python code to be executed.

        Returns:
            str: The output of the executed code.
        """
        output = self.codebox.exec(code)
        # Log the code (input) and its output
        self.history.append({
            "input": code,
            "output": output.chunks[0].content
        })
        return self.history[-1]

    def run_code_sequence(self, code_sequence: list):
        """
        Run a sequence of code statements and track each input/output.
        """
        results = []
        for code in code_sequence:
            result = self.execute_code(code)
            results.append(result)
        return results

    def get_variable(self, variable_name: str):
        """
        Retrieve the value of a variable and track the code used.
        """
        code = f"logger.info({variable_name})"
        return self.execute_code(code)

    def export_to_py(self, file_path: str):
        """
        Export the history of executed code to a Python script (.py).
        """
        with open(file_path, 'w') as f:
            for num, entry in enumerate(self.history):
                f.write(f"\n\n# In[{num+1}]:\n")
                f.write(f"{entry['input']}\n")

    def export_to_ipynb(self, file_path: str):
        """
        Export the history of executed code to a Jupyter Notebook (.ipynb).
        """
        notebook = {
            "cells": [],
            "metadata": {},
            "nbformat": 4,
            "nbformat_minor": 5
        }

        for entry in self.history:
            # Safely convert output to string if not JSON serializable
            output_text = str(entry['output']) if entry['output'] else ""

            code_cell = {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [{
                    "name": "stdout",
                    "output_type": "stream",
                    "text": [output_text]
                }],
                "source": entry['input'].splitlines()
            }
            notebook["cells"].append(code_cell)

        with open(file_path, 'w') as f:
            json.dump(notebook, f, indent=4)
