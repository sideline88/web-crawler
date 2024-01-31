from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlsplit
import requests
import urllib.robotparser

class ParseHTML(object):
    def __init__(self, url, base_url):
        self.url = url
        self.base_url = base_url
        try:
            self._retrieve_html()
            self._isolate_links()
        except requests.exceptions.RequestException as error:
            print(f'Error retrieving HTML from {self.url}: {error}')

# retrieves html data from a url
    def _retrieve_html(self):
        try:
            reply = requests.get(self.url)
            reply.raise_for_status()
            soup = BeautifulSoup(reply.text, 'html.parser')
            self.html_data = soup
        except requests.exceptions.RequestException as e:
            raise Exception(f'Failed to retrieve HTML from {self.url}. {e}')

# returns a set of internal and external links from the specified url
    def _isolate_links(self):
        raw_links = self.html_data.find_all('a', href = True)
        raw_links = set(link.get('href') for link in raw_links if link.get('href'))
        self.external_links, self.internal_links = set(), set()
        parse_base = urlparse(self.base_url)
        for link in raw_links:
            full_link = urljoin(self.base_url, link)
            parse_full_link = urlparse(full_link)
            if parse_base.netloc == parse_full_link.netloc:
                self.internal_links.add(link)
            else:
                self.external_links.add(link)

class MapSite(object):
    def __init__(self, url, polite = True):
        self.url = url
        self.polite = polite
        self._base_url()
        self._droid()
        self.found_external_links, self.found_internal_links = set(), set()
        self._recursive_crawl()
        self._dumpdata()

# defines base url of the website
    def _base_url(self):
        url_parts = urlsplit(self.url)
        self.base_url = url_parts.scheme + '://' + url_parts.netloc

# defines robots.txt
    def _droid(self):
        self.droid = urllib.robotparser.RobotFileParser()
        self.droid.set_url(urljoin(self.base_url, '/robots.txt'))
        self.droid.read()

# crawls through all the internal links of a website
    def _recursive_crawl(self, current_url = None):
        if current_url == None:
            current_url = self.url
        if self.droid.can_fetch('*', current_url) or self.polite == False:
            if current_url not in self.found_internal_links:
                print(current_url)
                self.found_internal_links.add(current_url)
                page = ParseHTML(current_url, self.base_url)
                try:
                    new_links = page.internal_links
                    self.found_external_links.update(page.external_links)
                    for link in new_links:
                        if link.startswith(current_url):
                            next_url = link
                        else:
                            next_url = urljoin(current_url, link)
                        self._recursive_crawl(next_url)
                except:
                    pass 

# outputs data to a .txt file
    def _dumpdata(self):
        with open('output.txt', 'w') as f:
            f.write(f'DATA OUTPUT for {self.url}\n\n')
            f.write('INTERNAL LINKS:\n\n')
            sorted_links = sorted(self.found_internal_links)
            for link in sorted_links:
                f.write(link + '\n')
            f.write('\nEXTERNAL LINKS:\n\n')
            sorted_links = sorted(self.found_external_links)
            for link in sorted_links:
                f.write(link + '\n')

'''
DATA
- Yield links as they are found rather than dumping
- Parse emails, images etc.
- Log disallowed links
- Scrape from backend not frontend

ETHICS
- 429 codes
- Crawl Delay

QUIET
- IP rotation
- Fingerprinting
- Traps and Tarpits

ROBOTS.TXT
- Error: No robots.txt
- Get Sitemap data
- Review XML vulnerabilities
'''

test_url = str(input('Website to Analyse: '))

data = MapSite(test_url)

input('Press any key to continue')
