
# GoogleDorking performs a Google search for the given query and extracts URLs from the results.
import requests
import re

class GoogleDorking:
    def __init__(self, query):
        self.query = query

    def search_dorks(self):
        """
        Perform a Google search and extract all URLs from the search results page.
        """
        results = []
        search_query = f'https://www.google.com/search?q={self.query}'
        response = requests.get(search_query)

        # Extract all URLs from the search result HTML
        urls = re.findall(r'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', response.text)
        results.extend(urls)
        
        return results
