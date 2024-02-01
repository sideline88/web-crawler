from urllib.parse import urljoin, urlsplit
import urllib.robotparser
from Daddy.LongLegsHTML import ParseHTML
from Daddy.LongLegsSITEMAP import ParseSITEMAP

class CrawlSite(object):
    def __init__(self, url, polite = True):
        self.url = url
        self.polite = polite
        self._base_url()
        self._parse_robots()
        print('Robots.txt Loaded')
        self.link_map = set()
        self._parse_sitemap()
        print('Sitemap Loaded')
        # self.found_external_links = set()
        # self.found_internal_links = set()
        # self._link_recursion()
        self._dumpdata()

# defines base url of the website
    def _base_url(self):
        url_parts = urlsplit(self.url)
        self.base_url = url_parts.scheme + '://' + url_parts.netloc

# defines robots.txt
    def _parse_robots(self):
        self.droid = urllib.robotparser.RobotFileParser()
        self.droid.set_url(urljoin(self.base_url, '/robots.txt'))
        self.droid.read()
    
    def _parse_sitemap(self):
        sitemaps = self.droid.site_maps()
        for i in sitemaps:
            data = ParseSITEMAP(i)
            self.link_map.update(data.links)

# crawls through all the internal links of a website
    def _link_recursion(self, url = None):
        if url == None:
            url = self.url
        if self.droid.can_fetch('*', url) or self.polite == False:
            if url not in self.found_internal_links:
                print(url)
                self.found_internal_links.add(url)
                page = ParseHTML(url, self.base_url)
                try:
                    new_links = page.internal_links
                    self.found_external_links.update(page.external_links)
                    for link in new_links:
                        if link.startswith(url):
                            next_url = link
                        else:
                            next_url = urljoin(url, link)
                        self._link_recursion(next_url)
                except:
                    pass 

# outputs data to a .txt file
    def _dumpdata(self):
        with open('output.txt', 'w') as f:
            f.write(f'DATA OUTPUT for {self.url}\n\n')
            f.write('LINKS FOUND:\n\n')
            sorted_links = sorted(self.link_map)
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
- user_agent

QUIET
- IP rotation
- Fingerprinting
- Traps and Tarpits

ROBOTS.TXT
- Error: No robots.txt
- Get Sitemap data
- Review XML vulnerabilities
- http vs https in sitemap extraction
- deal wiht .xml.gz
'''

test_url = str(input('Website to Analyse: '))

data = CrawlSite(test_url)

input('Press any key to continue')
