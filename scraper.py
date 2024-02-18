import getopt
import json
import multiprocessing
import re
import sys
from concurrent.futures import ThreadPoolExecutor


import tldextract
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from urllib.parse import urljoin


def extract_emails_from_url(url, domain, depth_limit, current_depth=0, visited_urls=None, extracted_emails=None):
    if current_depth > depth_limit:
        return []

    if visited_urls is None:
        visited_urls = set()

    if extracted_emails is None:
        extracted_emails = set()

    if url in visited_urls:
        return []

    visited_urls.add(url)
    print(f"Visiting URL: {url}")

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(chrome_options)
        driver.implicitly_wait(10)
        driver.get(url)

        html = driver.page_source

        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', html)
        unique_emails = set(emails)
        extracted_emails.update(unique_emails)

        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')

        for link in links:
            href = link.get('href')
            if not href:
                continue

            if href.startswith('http'):
                parsed_link = tldextract.extract(href)
                link_domain = parsed_link.registered_domain
                if link_domain != domain:
                    continue
            elif href.startswith('/') or str.endswith(href, '.html'):
                href = urljoin(url, href)
            else:
                continue

            linked_emails = extract_emails_from_url(href, domain, depth_limit, current_depth + 1, visited_urls,
                                                    extracted_emails)
            extracted_emails.update(linked_emails)

        driver.quit()

    except Exception as e:
        print(f"An error occurred while visiting the URL: {url}")
        print(f"Error message: {e}")

    return extracted_emails


def process_website(entry, depth_limit):
    if entry and entry.startswith('http'):
        parsed_url = tldextract.extract(entry)
        domain = parsed_url.registered_domain

        print(f"Processing website: {entry}")
        found_emails = extract_emails_from_url(entry, domain, depth_limit)

        allUrlsAndEmails.append({
            'url': entry,
            'emails': list(found_emails)
        })


def execute(input_file, output_file, depth_limit):
    with open(input_file) as file:
        data = json.load(file)

    num_cores = multiprocessing.cpu_count()

    executor = ThreadPoolExecutor(num_cores)

    futures = [executor.submit(process_website, entry, depth_limit) for entry in data]

    for future in futures:
        future.result()

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(allUrlsAndEmails, file, indent=4, ensure_ascii=False)


def main(argv):
    depth_limit = 3
    input_file = ''
    output_file = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:d:", ["inputfile=", "outputfile=", "depthlimit="])
    except getopt.GetoptError:
        print('scraper.py -i <inputfile> -o <outputfile> -d <depthlimit>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('scraper.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--inputfile"):
            input_file = arg
        elif opt in ("-o", "--outputfile"):
            output_file = arg
        elif opt in ("-d", "--depthlimit"):
            depth_limit = int(arg)

    execute(input_file, output_file, depth_limit)

    print("Updated URLs saved to", output_file, "file.")


if __name__ == '__main__':
    allUrlsAndEmails = []
    main(sys.argv[1:])
