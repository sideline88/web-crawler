from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlsplit
import requests

class ParseRobots(object):
    def __init__(self, url):
        self.url = url
        self._retrieve_robots(self.url)
        self._parse_robots(self.robotsdata)

# retrieves data from /robots.txt
    def _retrieve_robots(self, url):
        robots_url = urljoin(url, '/robots.txt')
        reply = requests.get(robots_url)
        self.robotsdata = reply.text if reply.status_code == 200 else None

# returns a set of allowed and disallowed links for user_agent *
# parse this properly for examples such as the socialist alliance website
    def _parse_robots(self, robotsdata):
        if robotsdata == None:
            self.allowed_links = None
            self.disallowed_links = None
        else:
            self.allowed_links, self.disallowed_links = list(), list()
            attention = False
            for entry in robotsdata.splitlines():
                if entry.startswith('#'):
                    continue
                if entry.lower().startswith('user-agent: *'):
                    attention = True
                    continue
                if len(entry) == 0 or entry.lower().startswith('user-agent:'):
                    attention = False
                    continue
                if attention:
                    link = entry.split(':', 1)[1].strip()
                    if entry.lower().startswith('allow'):
                        self.allowed_links.append(link)
                    elif entry.lower().startswith('disallow'):
                        self.disallowed_links.append(link)

class ParseHTML(object):
    def __init__(self, url, base_url):
        self.url = url
        self.base_url = base_url
        try:
            self._retrieve_html()
            self._isolate_links()
        except requests.exceptions.RequestException as e:
            print(f'Error retrieving HTML from {self.url}: {e}')

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
    def __init__(self, url):
        self.url = url
        self._base_url()
        self.found_external_links, self.found_internal_links = set(), set()
        self._recursive_crawl()
        self._dumpdata()

# defines base url of the website
    def _base_url(self):
        url_parts = urlsplit(self.url)
        self.base_url = url_parts.scheme + '://' + url_parts.netloc

# gathers the robots.txt data
    def _define_limiter(self):
        data = ParseRobots(self.base_url)
        self.robot_allowed = data.allowed_links
        self.robot_disallowed = data.disallowed_links

# crawls through all the internal links of a website
    def _recursive_crawl(self, current_url = None):
        if current_url == None:
            current_url = self.url
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
integrate robots.txt
Parse all data from robots.txt
yield links as they are found rather than dumping at the end
parse other data apart from links (images, emails)
get sitemap from robots.txt
IP rotation
traps and tarpits
'''

test_url = str(input('Website to Analyse: '))

data = MapSite(test_url)

input('Press any key to continue')
