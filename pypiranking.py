import json
import lxml.cssselect
import lxml.html
import os
# import requests
import concurrent.futures

# from pprint import pprint

ROOT_URL = 'http://pypi-ranking.info/alltime?page={page}'
PACKAGE_ELEM_SELECTOR = lxml.cssselect.CSSSelector('#main_list tr')
PACKAGE_POPULARITY_SELECTOR = lxml.cssselect.CSSSelector('.count span')
PACKAGE_TITLE_SELECTOR = lxml.cssselect.CSSSelector('.list_title')

# total_pages = None
page = 1
packages = None
scraped_pages = None

try:
    with open('pypiranking.json') as infile:
        data = json.load(infile)
        packages = data['packages']
        scraped_pages = data['scraped_pages']
except FileNotFoundError:
    packages = {}
    scraped_pages = []


def get_total_pages():
    document = lxml.html.parse(ROOT_URL.format(page=page)).getroot()
    current = document.cssselect('.step-links .current')[0].text_content().strip()
    index = current.index(' of ') + 4
    return int(current[index:-1])


def save_packages():
    with open('pypiranking.json', 'w') as outfile:
        json.dump({'packages': packages, 'scraped_pages': scraped_pages}, outfile)
    print(len(packages), 'packages already scraped.')


def scrape_page(page):
    if page in scraped_pages:
        return
    print('==================SCRAPING PAGE {page} ++++++++++++++++++'.format(page=page))
    global packages, total_pages
    try:
        document = lxml.html.parse(ROOT_URL.format(page=page)).getroot()
        for package_elem in PACKAGE_ELEM_SELECTOR(document):
            try:
                package_title = PACKAGE_TITLE_SELECTOR(package_elem)[0].text_content()
                package_popularity = int(PACKAGE_POPULARITY_SELECTOR(package_elem)[0].text_content().replace(',', ''))
                packages[package_title] = package_popularity
                print(page, package_title, package_popularity)
                scraped_pages.append(page)
            except IndexError:
                print('++++++++++ERROR AT: ', page)
    finally:
        save_packages()


concurrency = os.cpu_count() * 2
total_pages = get_total_pages()
with concurrent.futures.ThreadPoolExecutor(concurrency) as executor:
    for x in executor.map(scrape_page, range(1, total_pages + 1)):
        pass
