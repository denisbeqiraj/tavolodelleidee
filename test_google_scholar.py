import re

import requests
from bs4 import BeautifulSoup

keyword = 'Libro'
url = 'https://scholar.google.com/scholar?hl=it&q=allintitle%3A+' + keyword
data = requests.get(url)

link_scholar = []

html = BeautifulSoup(data.text, 'html.parser')
results = html.select('.gs_r')

for result in results:
    link = result.select('.gs_or_ggsm')
    if len(link) > 0:
        link = re.search('href=\"(.+?)\">', str(link[0].find('a'))).group(1)
        link_scholar.append(link)

print(link_scholar)
