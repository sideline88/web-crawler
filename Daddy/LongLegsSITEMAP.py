import requests
import xml.etree.ElementTree

class ParseSITEMAP(object):
    def __init__(self, url):
        self.url = url
        self.map_xml = set()
        self.map_gz = set()
        self.map_link = set()
        self._xml_recursion()

# harvests links from a .xml page
    def _mine_xml(self, url):
        url_set = set()
        data = requests.get(url).text
        for i in data.splitlines():
            if 'https://' in i:
                url = 'https://' + i.split('https://', 1)[1]
                url = url.split('<', 1)[0]
                url_set.add(url)
        return url_set

# crawls through sitemap .xml urls (does not open .xml.gz currently)
    def _xml_recursion(self, url = None):
        if url == None:
            url = self.url
        if url not in self.map_xml and \
            url not in self.map_gz and \
            url not in self.map_link:
            if url.endswith('.xml'):
                self.map_xml.add(url)
                data = self._mine_xml(url)
                for i in data:
                    self._xml_recursion(i)
            elif url.endswith('.xml.gz'):
                self.map_gz.add(url)
            else:
                self.map_link.add(url)