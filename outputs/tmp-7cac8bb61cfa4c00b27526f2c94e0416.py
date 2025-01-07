

# In[1]:
import requests
import base64

# GitHub repository details
owner = 'run-llama'
repo = 'llama_index'

# Function to get the contents of the repository
def get_repo_contents(owner, repo, path=''):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    response = requests.get(url)
    return response.json()

# Function to get the content of a markdown file
def get_file_content(owner, repo, path):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    response = requests.get(url)
    content = response.json()
    if 'content' in content:
        return base64.b64decode(content['content']).decode('utf-8')
    return None

# Get the contents of the repository
contents = get_repo_contents(owner, repo)

# Filter markdown files and extract image links
markdown_files = []
image_links = []

for item in contents:
    if item['name'].endswith('.md'):
        markdown_files.append(item['path'])
        file_content = get_file_content(owner, repo, item['path'])
        if file_content:
            # Extract image links from markdown content
            lines = file_content.split('\n')
            for line in lines:
                if line.startswith('!['):
                    # Extract the URL from the markdown image syntax
                    start = line.find('(') + 1
                    end = line.find(')')
                    image_links.append(line[start:end])

markdown_files, image_links
