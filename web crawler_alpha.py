from bs4 import BeautifulSoup
import requests

class ParseRobots(object):
    def __init__(self, url):
        self.url = url
        self._retrieve_robots(self.url)
        self._parse_robots(self.robotsdata)

# retrieves text from robots.txt file
    def _retrieve_robots(self, url):
        response = requests.get(url + '/robots.txt')
        if response.status_code == 200:
            self.robotsdata = response.text
        else:
            self.robotsdata = None

# parses the robots.txt list into allowed and disallowed links
    def _parse_robots(self, robotsdata):
        if robotsdata == None:
            self.allowed_links = None
            self.disallowed_links = None
        else:
            self.allowed_links, self.disallowed_links = list(), list()
            pay_attention = False
            for line in robotsdata.splitlines():
                if line.lower().startswith('user-agent: *'):
                    pay_attention = True
                    continue
                if len(line) == 0:
                    pay_attention = False
                if pay_attention:
                    link = line.split(':', 1)[1].strip()
                    if line.lower().startswith('allow'):
                        self.allowed_links.append(link)
                    elif line.lower().startswith('disallow'):
                        self.disallowed_links.append(link)

class ParseHTML(object):
    def __init__(self, url):
        self.url = url
        self._retrieve_html(self.url)
        self._isolate_links(self.html_data)

# retrieves html data and parses it using BeautifulSoup
    def _retrieve_html(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = response.text
            self.html_data = BeautifulSoup(soup, 'html.parser')

# isolates external and internal links from the html data
    def _isolate_links(self, html_data):
        raw_links = html_data.find_all('a')
        raw_links = set(link.get('href') for link in raw_links)
        self.external_links, self.internal_links = set(), set()
        for i in raw_links:
            if i.startswith(self.url) or i.startswith('/'):
                self.internal_links.add(i)
            else:
                self.external_links.add(i)

def map_website(url):
    homepage = ParseHTML(url)
    links_found = homepage.internal_links
    links_new = set()
    links_searched = set(url)
    for i in links_found:
        j = i if i.startswith(url) else url + i
        subpage = ParseHTML(j)
        links_searched.add(j)
        links_new.update(subpage.internal_links)
        print(j)
    links_found.update(links_new)
    for i in links_found:
        print(i)

test_url = 'https://quotes.toscrape.com'

map_website(test_url)