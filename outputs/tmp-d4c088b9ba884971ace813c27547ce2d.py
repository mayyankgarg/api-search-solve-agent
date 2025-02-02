

# In[1]:
import requests
import re

# Constants
GITHUB_REPO = 'shroominic/codeinterpreter-api'
GITHUB_API_URL = 'https://api.github.com/repos/' + GITHUB_REPO + '/contents/'

# Function to get contents of the repository
def get_repo_contents(path=''):
    response = requests.get(GITHUB_API_URL + path, headers={'Accept': 'application/vnd.github.v3+json'})
    return response.json()

# Function to extract image links from markdown text
def extract_images_from_markdown(markdown_text):
    # Regex to find image links in markdown
    image_regex = r'!\[.*?\]\((.*?)\)'
    return re.findall(image_regex, markdown_text)

# Main function to get images from markdown files
def get_images_from_markdown_files():
    images = []
    contents = get_repo_contents()
    for item in contents:
        if item['type'] == 'file' and item['name'].endswith('.md'):
            # Get the content of the markdown file
            markdown_content = requests.get(item['download_url']).text
            # Extract images
            images.extend(extract_images_from_markdown(markdown_content))
    return images

# Execute the function and get the list of images
image_list = get_images_from_markdown_files()
image_list
