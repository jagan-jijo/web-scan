
# IDORTest checks for Insecure Direct Object Reference vulnerabilities by manipulating common ID parameters in the URL.
import requests
from urllib.parse import urlparse

class IDORTest:
    def __init__(self, url):
        self.url = url
        # Common parameters to test for IDOR
        self.common_params = ['id', 'user_id', 'product_id', 'order_id', 'category_id', 'file_id']

    def check_vulnerability(self):
        """
        For each common parameter, modify the URL and check the response.
        If a 200 OK is returned, it may indicate a possible IDOR vulnerability.
        """
        results = []
        for param in self.common_params:
            test_url = self.manipulate_url(param)
            response = requests.get(test_url)

            if response.status_code == 200:
                results.append(f"Possible IDOR vulnerability found! URL: {test_url}")
            else:
                results.append(f"No IDOR vulnerability found for {param} (status code {response.status_code})")
        return results

    def manipulate_url(self, param):
        """
        Replace the query string with the test parameter for IDOR check.
        """
        parsed_url = urlparse(self.url)
        new_url = parsed_url._replace(query=f'{param}=99999')  # Change ID for IDOR test
        return new_url.geturl()
