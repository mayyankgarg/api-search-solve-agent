

# In[1]:
import requests
import re

# Constants
GITHUB_OWNER = 'shroominic'
GITHUB_REPO = 'codeinterpreter-api'

# Function to get repository contents
def get_repo_contents(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/'
    response = requests.get(url)
    return response.json()

# Function to get markdown file content
def get_markdown_content(download_url):
    response = requests.get(download_url)
    return response.text

# Function to extract image links from markdown content
def extract_image_links(markdown_content):
    # Regex to find image links in markdown
    image_regex = r'!\[.*?\]\((.*?)\)'
    return re.findall(image_regex, markdown_content)

# Main function to get images from markdown files
def get_images_from_markdown(owner, repo):
    contents = get_repo_contents(owner, repo)
    image_links = []
    for item in contents:
        if item['name'].endswith('.md'):
            markdown_content = get_markdown_content(item['download_url'])
            image_links.extend(extract_image_links(markdown_content))
    return image_links

# Execute the function
image_links = get_images_from_markdown(GITHUB_OWNER, GITHUB_REPO)
image_links
