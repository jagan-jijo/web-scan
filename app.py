
# Import necessary FastAPI and utility modules
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import logging
import sys

# Import custom modules for each test

from idor_test import IDORTest
from metadata_analysis import MetadataAnalysis
from google_dorking import GoogleDorking
from footprinting import Footprinting
from banner_grabbing import BannerGrabbing
from architecture_version import ArchitectureVersionChecker


# Setup logging to both file and terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("webpentest.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("webpentest")

# Initialize FastAPI app
app = FastAPI()
# Set up Jinja2 templates directory (must be 'templates/')
templates = Jinja2Templates(directory="templates")

# Pydantic model for POST request body
class URLRequest(BaseModel):
    url: str  # The URL to test

# Home page endpoint: renders the form
from fastapi import Request
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Render the form for user input
    return templates.TemplateResponse("index.html", {"request": request})


# Endpoint to run all security tests (accepts form data from HTML form)
from fastapi import Request

import requests
from urllib.parse import urlparse

@app.post("/run_tests/", response_class=HTMLResponse)
async def run_tests(request: Request):
    form = await request.form()
    url = form.get("url")
    results = {}

    # Ensure the URL has a scheme (http/https)
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    logger.info(f"Received request to analyze: {url}")

    # Ping the website with a HEAD request
    try:
        ping_response = requests.head(url, timeout=5)
        logger.info(f"Pinged {url} - Status: {ping_response.status_code}")
        if ping_response.status_code != 200:
            msg = f"Website did not respond with status 200 (got {ping_response.status_code}). Aborting tests."
            logger.warning(msg)
            results["Error"] = msg
            return templates.TemplateResponse("index.html", {"request": request, "url": url, "results": results})
    except Exception as e:
        msg = f"Could not reach the website: {e}"
        logger.error(msg)
        results["Error"] = msg
        return templates.TemplateResponse("index.html", {"request": request, "url": url, "results": results})


    # Run Architecture & Version Check
    logger.info("Running Architecture & Version Check...")
    arch_checker = ArchitectureVersionChecker(url)
    results["Architecture & Version"] = arch_checker.run_all()

    # Run IDOR Test (checks for Insecure Direct Object Reference vulnerabilities)
    logger.info("Running IDOR Test...")
    idor_test = IDORTest(url)
    results["IDOR"] = idor_test.check_vulnerability()

    # Run Metadata Analysis (extracts meta tags, title, and HTTP headers)
    logger.info("Running Metadata Analysis...")
    metadata_analysis = MetadataAnalysis(url)
    results["Metadata"] = metadata_analysis.fetch_metadata()

    # Run Google Dorking (searches Google for indexed data about the site)
    logger.info("Running Google Dorking...")
    google_dorking = GoogleDorking(f"site:{url}")
    results["Google Dorking"] = google_dorking.search_dorks()

    # Run Footprinting (gathers WHOIS and DNS info)
    logger.info("Running Footprinting...")
    domain = urlparse(url).hostname or url.split("//")[-1].split("/")[0]
    footprinting = Footprinting(domain)
    results["Footprinting"] = footprinting.domain_info()

    # Run Banner Grabbing (gets server banners from HTTP and common ports)
    logger.info("Running Banner Grabbing...")
    banner_grabbing = BannerGrabbing(url)
    results["Banner Grabbing"] = banner_grabbing.grab_banner()

    logger.info(f"Analysis complete for {url}")

    # Render results in the template
    return templates.TemplateResponse("index.html", {"request": request, "url": url, "results": results})

# Main entry point for running with `python app.py`
if __name__ == "__main__":
    # Use 127.0.0.1 for local development
    uvicorn.run(app, host="127.0.0.1", port=8000)
