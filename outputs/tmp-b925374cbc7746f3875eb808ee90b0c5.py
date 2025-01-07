

# In[1]:
import requests
import re

# Constants
GITHUB_API_URL = 'https://api.github.com'
REPO_OWNER = 'shroominic'
REPO_NAME = 'codeinterpreter-api'

# Function to get repository contents
def get_repo_contents(owner, repo):
    url = f'{GITHUB_API_URL}/repos/{owner}/{repo}/contents/'
    response = requests.get(url)
    return response.json()

# Function to get file content
def get_file_content(owner, repo, path):
    url = f'{GITHUB_API_URL}/repos/{owner}/{repo}/contents/{path}'
    response = requests.get(url)
    return response.json()

# Function to extract image URLs from markdown content
def extract_images_from_markdown(content):
    # Regex to find image links in markdown
    image_regex = r'!\[.*?\]\((.*?)\)'
    return re.findall(image_regex, content)

# Main function to get images from markdown files
def get_images_from_markdown_files():
    contents = get_repo_contents(REPO_OWNER, REPO_NAME)
    image_urls = []
    for item in contents:
        if item['name'].endswith('.md'):
            file_content = get_file_content(REPO_OWNER, REPO_NAME, item['path'])
            if 'content' in file_content:
                # Decode the content from base64
                content = file_content['content']
                decoded_content = base64.b64decode(content).decode('utf-8')
                # Extract image URLs
                images = extract_images_from_markdown(decoded_content)
                image_urls.extend(images)
    return image_urls

# Get images from markdown files
image_list = get_images_from_markdown_files()
image_list


# In[2]:
import requests
import re
import base64

# Constants
GITHUB_API_URL = 'https://api.github.com'
REPO_OWNER = 'shroominic'
REPO_NAME = 'codeinterpreter-api'

# Function to get repository contents
def get_repo_contents(owner, repo):
    url = f'{GITHUB_API_URL}/repos/{owner}/{repo}/contents/'
    response = requests.get(url)
    return response.json()

# Function to get file content
def get_file_content(owner, repo, path):
    url = f'{GITHUB_API_URL}/repos/{owner}/{repo}/contents/{path}'
    response = requests.get(url)
    return response.json()

# Function to extract image URLs from markdown content
def extract_images_from_markdown(content):
    # Regex to find image links in markdown
    image_regex = r'!\[.*?\]\((.*?)\)'
    return re.findall(image_regex, content)

# Main function to get images from markdown files
def get_images_from_markdown_files():
    contents = get_repo_contents(REPO_OWNER, REPO_NAME)
    image_urls = []
    for item in contents:
        if item['name'].endswith('.md'):
            file_content = get_file_content(REPO_OWNER, REPO_NAME, item['path'])
            if 'content' in file_content:
                # Decode the content from base64
                content = file_content['content']
                decoded_content = base64.b64decode(content).decode('utf-8')
                # Extract image URLs
                images = extract_images_from_markdown(decoded_content)
                image_urls.extend(images)
    return image_urls

# Get images from markdown files
image_list = get_images_from_markdown_files()
image_list
