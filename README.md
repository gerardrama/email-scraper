# Email Scraper Project

## Introduction
This repository contains a Python script designed to scrape emails from websites. The script navigates through the given websites and extracts email addresses, considering specified depth limits for the search. It's an effective tool for gathering email data for various purposes, including marketing, research, or data collection.

## Features
- **Depth-Limited Scraping**: Limit the search to a specified depth to control the breadth of the scraping process.
- **Multi-Threading**: Leverages multi-threading for efficient scraping across multiple websites.
- **Domain Specific**: Extracts emails only from specified domain names to ensure relevance.
- **Headless Browsing**: Uses a headless browser for scraping, reducing resource usage.
- **Error Handling**: Error handling to manage and log issues during scraping.

## Installation
Before running the script, ensure you have the following dependencies installed:

- Python 3.x
- Selenium WebDriver
- BeautifulSoup4
- tldextract

You can install these dependencies using pip:

```
pip install selenium beautifulsoup4 tldextract
```

Additionally, make sure to have the Chrome WebDriver installed on your system.

## Usage

To use the script, provide an input file in JSON format containing the list of URLs to scrape. The script also requires an output file where the results will be saved. The depth limit for scraping can be set as a parameter.

### Command Line Arguments:
- **-i** or **--inputfile**: Path to the input JSON file containing URLs. 
- **-o** or **--outputfile**: Path to the output file where results will be saved. 
- **-d** or **--depthlimit**: Depth limit for the scraping (default is 3).

### Example Usage:
Run the script in the command line as follows:
```
python scraper.py -i input.json -o output.json -d 10
```

### Input File Format

The input file should be a JSON file containing a list of URLs. Example:

```
[
    "http://example.com",
    "https://example.org"
]
```

### Output

The output is a JSON file containing the URLs and their corresponding extracted emails. Example format:
```
[
    {
        "url": "http://example.com",
        "emails": ["info@example.com", "contact@example.com"]
    },
    {
        "url": "http://example.org",
        "emails": ["admin@example.org"]
    }
]
```

## Limitations and Notes
The script is designed to work with websites that are accessible via the Chrome browser.
The performance may vary based on the number of URLs and the depth limit set. Captcha support is not possible yet.

