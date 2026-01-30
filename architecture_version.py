import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class ArchitectureVersionChecker:
    """
    Checks website architecture, technology stack, and version info using headers, meta tags, and common paths.
    """
    def __init__(self, url):
        self.url = url if url.startswith("http") else f"https://{url}"
        self.report = []

    def check_headers(self):
        try:
            response = requests.head(self.url, timeout=5, allow_redirects=True)
            headers = response.headers
            tech_info = []
            for header, value in headers.items():
                if header.lower() in ["x-powered-by", "server"] or "php" in value.lower() or "express" in value.lower() or "wordpress" in value.lower():
                    tech_info.append(f"{header}: {value}")
            if tech_info:
                self.report.append("HTTP Response Headers (Possible Tech Stack):\n" + "\n".join(tech_info))
            else:
                self.report.append("No revealing technology headers found.")
        except Exception as e:
            self.report.append(f"Error checking headers: {e}")

    def check_meta_tags(self):
        try:
            response = requests.get(self.url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            meta_tags = soup.find_all('meta')
            found = False
            for meta in meta_tags:
                if meta.get('name', '').lower() == 'generator' and meta.get('content'):
                    self.report.append(f"Meta Generator Tag: {meta['content']}")
                    found = True
            if not found:
                self.report.append("No generator meta tag found.")
        except Exception as e:
            self.report.append(f"Error checking meta tags: {e}")

    def check_common_paths(self):
        # Check for CMS/framework-specific paths
        checks = {
            "WordPress": ["/wp-admin/", "/wp-login.php", "/wp-content/", "/readme.html"],
            "Joomla": ["/components/", "/modules/", "/templates/"],
            "Drupal": ["/node/", "/sites/"],
        }
        for cms, paths in checks.items():
            for path in paths:
                full_url = urljoin(self.url, path)
                try:
                    resp = requests.get(full_url, timeout=5)
                    if resp.status_code == 200:
                        self.report.append(f"{cms} path found: {full_url} (Status 200)")
                except Exception:
                    continue

    def check_wordpress_version(self):
        # Try to get version from readme.html
        readme_url = urljoin(self.url, "/readme.html")
        try:
            resp = requests.get(readme_url, timeout=5)
            if resp.status_code == 200 and "WordPress" in resp.text:
                for line in resp.text.splitlines():
                    if "Version" in line:
                        self.report.append(f"WordPress Version from readme.html: {line.strip()}")
                        break
        except Exception:
            pass

    def run_all(self):
        self.check_headers()
        self.check_meta_tags()
        self.check_common_paths()
        self.check_wordpress_version()
        return self.report
