from urllib.parse import urljoin, urlsplit

import urllib.robotparser

from Daddy.LongLegsHTML import ParseHTML

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
