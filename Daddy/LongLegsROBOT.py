from urllib.parse import urljoin

import urllib.robotparser

class ParseROBOT(object):
    def __init__(self, url, user_agent):
        self.droid = urllib.robotparser.RobotFileParser()
        self.droid.set_url(urljoin(url, '/robots.txt'))
        self.droid.read()