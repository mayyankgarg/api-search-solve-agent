

# In[1]:
import requests
import base64
import re

# Constants
GITHUB_REPO = 'shroominic/codeinterpreter-api'
GITHUB_API_URL = 'https://api.github.com/repos/'

# Function to get repository contents

def get_repo_contents(repo):
    url = f'{GITHUB_API_URL}{repo}/contents/'
    response = requests.get(url)
    return response.json()

# Function to get file content

def get_file_content(repo, path):
    url = f'{GITHUB_API_URL}{repo}/contents/{path}'
    response = requests.get(url)
    return response.json()

# Function to extract images from markdown content

def extract_images_from_markdown(content):
    # Decode the base64 content
    decoded_content = base64.b64decode(content).decode('utf-8')
    # Regex to find image links
    image_links = re.findall('!\[.*?\]\((.*?)\)', decoded_content)
    return image_links

# Main function to get images from markdown files

def get_images_from_markdown_files(repo):
    contents = get_repo_contents(repo)
    images = []
    for item in contents:
        if item['type'] == 'file' and item['name'].endswith('.md'):
            file_content = get_file_content(repo, item['path'])
            images.extend(extract_images_from_markdown(file_content['content']))
    return images

# Get images from the specified repository
images = get_images_from_markdown_files(GITHUB_REPO)
images
