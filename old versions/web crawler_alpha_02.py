import requests

class RobotsParser(object):
    def __init__(self, url):
        self.url = url
        self._retrieve_robots(self.url)
        self._parse_robots(self.robotsdata)

    def _retrieve_robots(self, url):
        response = requests.get(url + '/robots.txt')
        if response.status_code == 200:
            self.robotsdata = response.text
        else:
            self.robotsdata = None

    def _parse_robots(self, robotsdata):
        self.entries = list()
        for line in robotsdata.splitlines():
            if len(line.strip()) != 0:
                   if line.startswith('#'):
                       content = line.lstrip('#').strip()
                       self.entries.append({"type": "commentary", "content": content, "raw": line})
                   elif line.lower().startswith('allow'):
                       content = line.split(':', 1)[1].strip()
                       self.entries.append({"type": "allow", "content": content, "raw": line})
                   elif line.lower().startswith('disallow'):
                       content = line.split(':', 1)[1].strip()
                       self.entries.append({"type": "disallow", "content": content, "raw": line})

data = RobotsParser('https://www.twitter.com')

for i in data.entries:
    print(i)
