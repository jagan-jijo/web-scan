
# BannerGrabbing attempts to retrieve server banners from HTTP headers and common ports.
import requests
import socket
from urllib.parse import urlparse

class BannerGrabbing:
    def __init__(self, url):
        self.url = url

    def grab_banner(self):
        """
        Grab the HTTP server banner and attempt to read banners from common ports (80, 443, 8080).
        """
        results = []
        try:
            # Get HTTP server header
            response = requests.head(self.url)
            server_header = response.headers.get('Server', 'No server banner found')
            results.append(f"Server Banner: {server_header}")

            # Try to grab banners from common ports
            ports = [80, 443, 8080]
            for port in ports:
                try:
                    socket_connection = socket.create_connection((urlparse(self.url).hostname, port), timeout=5)
                    banner = socket_connection.recv(1024).decode('utf-8', errors='ignore')
                    results.append(f"Banner on port {port}: {banner}")
                except Exception as e:
                    results.append(f"Could not grab banner from port {port}: {e}")

        except requests.exceptions.RequestException as e:
            results.append(f"Error grabbing banner: {e}")

        return results
