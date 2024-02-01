from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests

class ParseHTML(object):
    def __init__(self, url, base_url):
        self.url = url
        self.base_url = base_url
        self.internal_links = set()
        self.external_links = set()
        try:
            self._retrieve_html_data()
            self._harvest_links()
        except requests.exceptions.RequestException as error:
            print(f'Error retrieving HTML from {self.url}: {error}')

# retrieves html data from a url
    def _retrieve_html_data(self):
        try:
            reply = requests.get(self.url)
            reply.raise_for_status()
            self.html_data = BeautifulSoup(reply.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            raise Exception(f'Failed to retrieve HTML from {self.url}. {e}')

# returns a set of internal and external links from the specified url
    def _harvest_links(self):
        data = self.html_data.find_all('a', href = True)
        data = set(link.get('href') for link in data if link.get('href'))
        parse_base = urlparse(self.base_url)
        for link in data:
            parse_link = urljoin(self.base_url, link)
            parse_link = urlparse(parse_link)
            if parse_base.netloc == parse_link.netloc:
                self.internal_links.add(link)
            else:
                self.external_links.add(link)
