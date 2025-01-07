import json
import requests
import logging
from utils import llm_response
from markdownify import markdownify as md

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def search(documentation_url, api_question, min_searches=25):
    """
    Search for relevant APIs from documentation URLs based on a given question.
    
    Parameters:
        documentation_url (str): Initial URL of the documentation to start the search.
        api_question (str): Question or topics to query APIs for.
        min_searches (int): Minimum number of pages to process. Default is 25.
        
    Returns:
        dict: Contains two fields:
            - "relevant_apis": List of APIs directly related to the question.
            - "suggested_pages": List of pages that might contain relevant APIs.
    """
    def url_markdown(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Failed to retrieve {url}: {e}")
            return None
        return md(response.text)

    def fix_url(new_link, base_url):
        new_link = new_link.split('#')[0]
        if 'https' in new_link:
            return new_link
        else:
            return base_url.rstrip('/') + '/' + new_link.lstrip('/')

    api_info = []
    links_to_process = [documentation_url]
    urls_visited = []
    search_count = 0

    TERMINATE_COUNT = 25

    while links_to_process:
        if search_count > min_searches and len(api_info):
            break
        
        if search_count > TERMINATE_COUNT:
            break

        search_count += 1

        documentation_url = links_to_process.pop(0)
        html_markdown = url_markdown(url=documentation_url)
        if not html_markdown:
            continue

        links = llm_response(
            user_message=f'Documentation:\n```{html_markdown}```\n\nQuestion:\n{api_question}',
            system_message="""You have been given a documentation page in markdown format. 
You need to find if any relevant APIs are mentioned in the documentation related to the question.
If not, then shortlist the pages (![Alt text](link)) which may contain relevant APIs related to the question, if any.

## Output Format
The output JSON format can include two main fields:
- Relevant APIs: A list of APIs directly related to the question, if found in the documentation.
- Suggested Pages: A list of pages (in markdown format) that might contain relevant APIs, if no direct APIs are found.
{{
    "relevant_apis": [
        {{
            "name": str,
            "method": str,
            "endpoint": str,
            "description": str,
            "curl_request_example": str,
            "sample_response": str,
            "headers": [
                {{
                    "name": str,
                    "type": str,
                    "description": str
                }}
            ],
            "path_parameters": [
                {{
                    "name": str,
                    "type": str,
                    "description": str
                }},
            ],
            "query_parameters": [
                {{
                    "name": str,
                    "type": str,
                    "description": str
                }}
            ]
        }},
    ],
    "suggested_pages": [
        {{
            "title": str,
            "link": str
        }},
    ]

}}""",
            json_mode=True,
            temperature=0,
            # temperature=0.5,
        )

        links = json.loads(links)
        for relevant_link_json in links['relevant_apis']:
            relevant_link_json['documentation'] = documentation_url
        api_info.extend(links['relevant_apis'])

        new_links = [fix_url(l['link'], documentation_url) for l in links['suggested_pages']]
        new_links = list(set(new_links))

        links_to_process.extend(link for link in new_links if link not in urls_visited)
        links_to_process=list(set(links_to_process))
        urls_visited.append(documentation_url)

        if not links_to_process:
            break

        logging.info(f'Search Count: {search_count}*********************')
        for api in api_info:
            logging.info(f"Name: {api['name']}, Endpoint: {api['endpoint']}")

    return {
        "relevant_apis": api_info,
        "suggested_pages": [{"link": page} for page in links_to_process]
    }
