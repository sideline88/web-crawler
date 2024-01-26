import requests
from urllib import robotparser

# retrieve robots.txt data
def get_robots_txt(url):
    response = requests.get(url + '/robots.txt')
    if response.status_code == 200:
        return response.text
    else:
        return None

# parse_robots_txt
def parse_robots_txt(robots_txt_content, user_agent):
    rp = robotparser.RobotFileParser()
    rp.parse(robots_txt_content.splitlines())
    rp.set_url(user_agent)
    return rp

# check a specific path in a robots.txt file for a specific user
def check_path(url, user_agent, path):
    robots_txt_content = get_robots_txt(url)
    if robots_txt_content:
        rp = parse_robots_txt(robots_txt_content, user_agent)
        if rp.can_fetch('*', path):
            print(f'The user agent "*" is allowed to access: {path}')
        else:
            print(f'The user agent "*" is not allowed to access: {path}')
    else:
        print('Failed to fetch robots.txt content.')

check_path('https://www.reddit.com', '*', '/submit')
