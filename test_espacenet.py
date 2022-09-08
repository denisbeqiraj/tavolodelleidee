import json

import requests
import xml.etree.ElementTree as ET

# request access token
header_access = {
    'Authorization': 'Basic QVJLOWdVYnVLWUQzaEpsbU9lRmdmRm94cXRNNXRyRkc6S1Q0dHhpc0F3VkpFOUVmOA==',
    'Content-Type': 'application/x-www-form-urlencoded',
}
param = {'grant_type': 'client_credentials'}

url_access = 'https://ops.epo.org/3.2/auth/accesstoken'
info = requests.post(url_access, headers=header_access, data=param)
data_access = json.loads(info.text) # data_access['access_token'] is the authorization
auth = data_access['access_token']

# search publication data
keyword = 'tavolo'
url = 'http://ops.epo.org/3.2/rest-services/published-data/search?Range=1-5&q=ti%3D' + keyword
header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'it-IT',
    'Authorization': 'Bearer ' + auth,
    'Host': 'ops.epo.org',
    'sec-ch-ua': 'Chromium";v="104',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML',
    'X-Forwarded-Port': '443',
    'X-Forwarded-Proto': 'https',
}

data = requests.get(url, headers=header)

link_espacenet = []

root = ET.fromstring(data.text)
for elem in root.iter("{http://ops.epo.org}publication-reference"):
    family_id = elem.attrib["family-id"]
    country = elem.find("./{http://www.epo.org/exchange}document-id/{http://www.epo.org/exchange}country").text
    doc_number = elem.find("./{http://www.epo.org/exchange}document-id/{http://www.epo.org/exchange}doc-number").text
    kind = elem.find("./{http://www.epo.org/exchange}document-id/{http://www.epo.org/exchange}kind").text
    doc_id = country + doc_number + kind
    link = "https://worldwide.espacenet.com/patent/search/family/" + family_id + "/publication/" + doc_id + "?q="+ doc_id
    #link_espacenet.append(link)
    doc_id2 = country + doc_number + "." + kind
    url2 = "http://ops.epo.org/3.2/rest-services/published-data/publication/epodoc/" + doc_id2 + "/biblio"
    data2 = requests.get(url2, headers=header)
    root2 = ET.fromstring(data2.text)
    title = root2.find("./{http://www.epo.org/exchange}exchange-documents/{http://www.epo.org/exchange}exchange-document/{http://www.epo.org/exchange}bibliographic-data/{http://www.epo.org/exchange}invention-title").text
    link_and_title = (title, link)
    link_espacenet.append(link_and_title)
print(link_espacenet)
