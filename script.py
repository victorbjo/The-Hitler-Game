import requests
from bs4 import BeautifulSoup
import time
import cchardet
time_request = 0
time_parse = 0
count = 0
session = requests.Session()
def get_html(URL):
    global time_request
    now = time.time()
    response = session.get(URL)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print("Failed to retrieve content. Status code:", response.status_code)
        html_content = response.status_code
    time_request = time_request + time.time() - now
    return html_content

def get_links(html):
    global time_parse
    now = time.time()
    soup = BeautifulSoup(html, 'lxml')
    container = soup.find('div', {'id': 'bodyContent'})
    if container is None:
        return []
    links = container.find_all('a')
    links_list = []
    for link in links:
        if link.get('href') is None:
            continue
        if link.get('href').startswith('/wiki/'):
            links_list.append(link.get('href'))
    time_parse = time_parse + time.time() - now
    return links_list

html = get_html("https://en.wikipedia.org/wiki/Modulo")
#
goal = "/wiki/Germans"
wiki = "https://en.wikipedia.org"
links = get_links(html)
time_now = time.time()
visited = []
while links:
    print(count)
    current_link = links.pop(0)
    if current_link in visited:
        continue
    visited.append(current_link)
    if current_link == goal:
        #print("Found!")
        break
    else:
        #print("Not yet!", current_link)
        html = get_html(wiki + current_link)
        count += 1
        new_links = get_links(html)
        links = links + new_links
        #Remove duplicates
        #links = list(set(links))
#print(html)
print("Request time: ", time_request)
print("Parse time: ", time_parse)
print("Count: ", count)
print("Total time: ", time.time() - time_now)
print("Function times", time_request + time_parse)