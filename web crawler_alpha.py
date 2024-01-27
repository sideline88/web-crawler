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
            self.entries = None
        else:
            self.allowed_links, self.disallowed_links = list(), list()
            pay_attention = False
            for line in robotsdata.splitlines():
                if line.lower().startswith('user-agent: *'):
                    pay_attention = True
                    continue
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
        self.external_links, self.internal_links = list(), list()
        for i in raw_links:
            if i.startswith('https://'):
                self.external_links.append(i)
            else:
                self.internal_links.append(i)

'''
Iterate links to a certain depth (or entire website)
Prune links already visited
Ignore external links
Logger
Final report
'''

test_url = 'https://www.reddit.com'

data = ParseRobots(test_url)

print('ALLOWED LINKS:')
for i in data.allowed_links:
    print(i)
print('\nDISALLOWED LINKS:')
for i in data.disallowed_links:
    print(i)