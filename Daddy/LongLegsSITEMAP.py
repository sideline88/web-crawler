import requests
import xml.etree.ElementTree

class ParseSITEMAP(object):
    def __init__(self, url):
        self.url = url
        self.xml_links = set()
        self.xml_gz_links = set()
        self.links = set()
        self._xml_recursion()

# harvests links from a .xml page
    def _harvest_links(self, url):
        link_set = set()
        data = requests.get(url).text
        for entry in data.splitlines():
            if 'https://' in entry:
                link = 'https://' + entry.split('https://', 1)[1]
                link = link.split('<', 1)[0]
                link_set.add(link)
        return link_set

# crawls through sitemap .xml urls (does not open .xml.gz currently)
    def _xml_recursion(self, url = None):
        if url == None:
            url = self.url
        if url not in self.xml_links and \
            url not in self.xml_gz_links and \
            url not in self.links:
            if url.endswith('.xml'):
                self.xml_links.add(url)
                new_links = self._harvest_links(url)
                for link in new_links:
                    self._xml_recursion(link)
            elif url.endswith('.xml.gz'):
                self.xml_gz_links.add(url)
            else:
                self.links.add(url)