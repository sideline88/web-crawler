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
            self._mine_html()
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
    def _mine_html(self):
        data = self.html_data.find_all('a', href = True)
        data = set(i.get('href') for i in data if i.get('href'))
        parse_base = urlparse(self.base_url)
        for i in data:
            parse_link = urljoin(self.base_url, i)
            parse_link = urlparse(parse_link)
            if parse_base.netloc == parse_link.netloc:
                self.internal_links.add(i)
            else:
                self.external_links.add(i)
