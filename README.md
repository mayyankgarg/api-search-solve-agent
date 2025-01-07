# API Search and Code Execution Tool

This project is a Python-based tool designed to search for relevant APIs from a given documentation URL and execute Python code in a persistent Jupyter Notebook environment. It leverages the capabilities of a language model to break down tasks, search for APIs, and execute code.

## Features

- **API Search**: Search for relevant APIs by crawling a documentation URL and its sub-URLs.
- **Code Execution**: Execute Python code in a persistent Jupyter Notebook and retrieve the results.
- **Logging**: Logs important information and tool interactions for debugging and analysis.

## Requirements

- Python 3.x
- Required Python packages: `json`, `logging`, `decouple`, `uuid`
- External modules: `utils`, `find_apis`, `codebox`

## Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:
   Ensure you have all the required Python packages installed. You can use `pip` to install any missing packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration**:
   - Ensure that the `utils`, `find_apis`, and `codebox` modules are available in your Python path.
   - Configure any necessary environment variables using a `.env` file if required by the `decouple` package.

## Usage

1. **Run the Script**:
   Execute the main script to start the tool:
   ```bash
   python main.py
   ```

2. **Customize the Task**:
   Modify the `QUESTION`, `CONNECTOR_NAME`, `DOCUMENTATION_URL`, and `GITHUB_REPO` variables in `main.py` to customize the task and the API search parameters.

3. **View Logs**:
   Check the `app.log` file for detailed logs of the tool's execution and interactions.

## How It Works

- The tool uses a language model to interpret a user-defined task and break it down into steps.
- It searches for relevant APIs using the `search_apis()` function by crawling the specified documentation URL.
- It executes Python code using the `execute_code()` function and logs the results.
- The tool supports iterative interactions with the language model to refine the task and obtain the final result.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## Contact

For any questions or issues, please contact [Your Name] at [Your Email].
