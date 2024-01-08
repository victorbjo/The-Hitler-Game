import requests
from bs4 import BeautifulSoup
import time
import cchardet
from models import Link
import asyncio
import db
time_request = 0
time_parse = 0
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
        if link.get('href').startswith('/wiki/') and ":" not in link.get('href'):
            links_list.append(link.get('href'))
    time_parse = time_parse + time.time() - now
    return links_list
count = 0
def list_to_str(list):
    string = ""
    for item in list:
        string = string + item + "\n"
    return string
db_time = time.time()
async def main():
    global db_time
    global count
    html = get_html("https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss")
    #html = get_html("https://en.wikipedia.org/wiki/Germans")
    #/wiki/Adolf_Hitler
    #https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss
    goal = "/wiki/Adolf_Hitler"
    wiki = "https://en.wikipedia.org"
    links = get_links(html)
    visited = []
    while links:
        if "_lists" in links:
            print("WTF")
            break
        #print(count)
        current_link = links.pop(0)
        if current_link in visited:
            continue
        #print(current_link)
        visited.append(current_link)
        if current_link == goal:
            print("Found!")
            break
        else:
            #print("Not yet!", current_link)
            link_db : Link = await db.get_link(current_link)
            if link_db is not None and link_db != False:
                links = links + link_db.get_list()
                count += 1
                continue
                pass
                #continue
                #break
            print(wiki, current_link)
            html = get_html(wiki + current_link)
            
            count += 1
            new_links = get_links(html)
            temp = time.time()
            await db.create_link(current_link, list_to_str(new_links))
            db_time = db_time + (time.time() - temp)
            links = links + new_links
            #Remove duplicates
            #links = list(set(links))
    #print(html)
time_now = time.time()
asyncio.run(main())
print("Request time: ", time_request)
print("Parse time: ", time_parse)
print("Count: ", count)
print("Total time: ", time.time() - time_now)
print("Function times", time_request + time_parse)
print("DB time: ", db_time)