
# MetadataAnalysis extracts meta tags, title, and HTTP headers from a web page.
import requests
from bs4 import BeautifulSoup

class MetadataAnalysis:
    def __init__(self, url):
        self.url = url

    def fetch_metadata(self):
        """
        Fetch meta tags, page title, and HTTP headers from the target URL.
        """
        results = []
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.content, 'html.parser')
            meta_tags = soup.find_all('meta')
            
            # Extract meta tag information
            for meta in meta_tags:
                if 'name' in meta.attrs:
                    results.append(f"{meta.attrs.get('name')}: {meta.attrs.get('content')}")
            
            # Extract title
            title = soup.title.string if soup.title else 'No title'
            results.append(f"Title: {title}")
            
            # Extract HTTP headers
            for key, value in response.headers.items():
                results.append(f"{key}: {value}")
            
        except requests.exceptions.RequestException as e:
            results.append(f"Error fetching metadata: {e}")
        
        return results
