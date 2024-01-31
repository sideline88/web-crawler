from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

import requests

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
