from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlsplit
import requests

class ParseRobots(object):
    def __init__(self, url):
        self.url = url
        self._retrieve_robots(self.url)
        self._parse_robots(self.robotsdata)

    def _retrieve_robots(self, url):
        robots_url = urljoin(url, '/robots.txt')
        reply = requests.get(robots_url)
        self.robotsdata = reply.text if reply.status_code == 200 else None

    def _parse_robots(self, robotsdata):
        if robotsdata == None:
            self.allowed_links = None
            self.disallowed_links = None
        else:
            self.allowed_links, self.disallowed_links = list(), list()
            attention = False
            for entry in robotsdata.splitlines():
                if entry.lower().startswith('user-agent: *'):
                    attention = True
                    continue
                if len(entry) == 0:
                    attention = False
                    continue
                if attention:
                    link = entry.split(':', 1)[1].strip()
                    if entry.lower().startswith('allow'):
                        self.allowed_links.append(link)
                    elif entry.lower().startswith('disallow'):
                        self.disallowed_links.append(link)

class ParseHTML(object):
    def __init__(self, url):
        self.url = url
        self._retrieve_html(self.url)
        try:
            self._isolate_links(self.html_data)
        except:
            pass

    def _retrieve_html(self, url):
        reply = requests.get(url)
        if reply.status_code == 200:
            soup = reply.text
            self.html_data = BeautifulSoup(soup, 'html.parser')

    def _isolate_links(self, html_data):
        url_parts = urlsplit(self.url)
        base_url = url_parts.scheme + '://' + url_parts.netloc
        raw_links = html_data.find_all('a', href = True)
        raw_links = set(link.get('href') for link in raw_links if link.get('href'))
        self.external_links, self.internal_links = set(), set()
        for i in raw_links:
            if i.startswith(base_url) or i.startswith('/'):
                self.internal_links.add(i)
            else:
                self.external_links.add(i)

class MapSite(object):
    def __init__(self, url):
        self.url = url
        self.found_links = set()
        self._recursive_crawl(url)
    
    def _recursive_crawl(self, current_url = None):
        if current_url == None:
            current_url = self.url
        if current_url not in self.found_links:
            print(current_url)
            self.found_links.add(current_url)
            page = ParseHTML(current_url)
            new_links = page.internal_links
            for link in new_links:
                if link.startswith(current_url):
                    next_url = link
                else:
                    next_url = urljoin(current_url, link)
                self._recursive_crawl(next_url)

'''
integrate robots.txt
'''

test_url = str(input('Website to Analyse: '))

data = MapSite(test_url)

input('Press any key to continue')
