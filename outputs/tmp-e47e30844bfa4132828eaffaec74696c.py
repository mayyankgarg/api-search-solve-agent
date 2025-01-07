

# In[1]:
import requests

# GitHub repository details
owner = 'shroominic'
repo = 'codeinterpreter-api'

# Function to get repository contents
def get_repo_contents(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/'
    response = requests.get(url)
    return response.json()

# Fetch the contents of the repository
contents = get_repo_contents(owner, repo)

# Filter for markdown files
markdown_files = [item for item in contents if item['name'].endswith('.md')]
markdown_files


# In[2]:
# Function to get the content of a markdown file
def get_markdown_content(download_url):
    response = requests.get(download_url)
    return response.text

# Download URL for the README.md file
markdown_file_url = 'https://raw.githubusercontent.com/shroominic/codeinterpreter-api/main/README.md'

# Fetch the content of the markdown file
markdown_content = get_markdown_content(markdown_file_url)
markdown_content


# In[3]:
import re

# Function to extract tables from markdown content
def extract_tables(markdown_content):
    # Regular expression to match markdown tables
    table_regex = r'((?:\|.*?\|\n)+)'  # Matches lines that look like tables
    tables = re.findall(table_regex, markdown_content)
    return tables

# Extract tables from the markdown content
extracted_tables = extract_tables(markdown_content)
extracted_tables
