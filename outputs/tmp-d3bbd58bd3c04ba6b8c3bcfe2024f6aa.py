

# In[1]:
import requests
import re

# Constants
GITHUB_API_URL = 'https://api.github.com'
REPO_OWNER = 'run-llama'
REPO_NAME = 'llama_index'

# Function to get repository contents

def get_repo_contents(path=''):
    url = f'{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    response = requests.get(url, headers=headers)
    return response.json()

# Function to extract image URLs from markdown content

def extract_image_urls(markdown_content):
    # Regex to find image URLs in markdown
    image_regex = r'!\[.*?\]\((.*?)\)'
    return re.findall(image_regex, markdown_content)

# Get the contents of the repository
contents = get_repo_contents()

# List to hold image URLs
image_urls = []

# Iterate through the contents to find markdown files
for item in contents:
    if item['name'].endswith('.md'):
        # Fetch the markdown file content
        markdown_content = requests.get(item['download_url']).text
        # Extract image URLs
        image_urls.extend(extract_image_urls(markdown_content))

image_urls
