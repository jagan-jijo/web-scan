
# Web Penetration Testing Toolkit

A Python-based web application for basic website security analysis and reconnaissance. This tool provides a simple web interface to run multiple security and information-gathering tests on any public website.

## Features

- **IDOR Test**: Checks for possible Insecure Direct Object Reference vulnerabilities by manipulating common ID parameters in the URL.
- **Metadata Analysis**: Extracts meta tags, page title, and HTTP headers to reveal SEO and server information.
- **Google Dorking**: Performs Google search queries to find indexed and potentially sensitive data related to the target site.
- **Footprinting**: Gathers domain registration (WHOIS) and DNS information about the target domain.
- **Banner Grabbing**: Attempts to retrieve server banners from HTTP headers and common ports (80, 443, 8080).
- **Logging**: All actions and errors are logged to both the terminal and a `webpentest.log` file for auditing and troubleshooting.

## Requirements
- Python 3.8+
- Linux (tested on Kali Linux)
- Internet access for external lookups

## Setup & Usage

1. **Clone or Download the Repository**

2. **Create a Virtual Environment (Recommended):**
	```bash
	python3 -m venv myenv
	source myenv/bin/activate
	```

3. **Install Dependencies:**
	```bash
	pip install -r requirements.txt
	# Or, if using the provided start.sh, dependencies are installed automatically
	```

4. **Start the Application:**
	```bash
	chmod +x start.sh
	./start.sh
	# Or run directly:
	python app.py
	```

5. **Open the Web Interface:**
	- The app will open automatically, or visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

6. **Usage:**
	- Enter the target website URL (e.g., `www.example.com` or `https://www.example.com`)
	- Click **Analyze**
	- View detailed results for each test in the browser
	- All actions are logged in `webpentest.log`

## What Each Test Provides
- **IDOR**: Shows which URLs were tested for possible direct object reference vulnerabilities.
- **Metadata**: Lists meta tags, page title, and HTTP headers for SEO and server info.
- **Google Dorking**: Displays URLs found via Google search related to the target.
- **Footprinting**: Provides domain registration (WHOIS) and DNS records.
- **Banner Grabbing**: Shows server type and attempts to grab banners from common ports.

## Notes
- This tool is for educational and authorized security testing only.
- Do not use against sites you do not own or have explicit permission to test.
- Some tests may trigger security alerts or rate limits on target sites.

## License
MIT License