import requests
from bs4 import BeautifulSoup
import time
import cchardet
from models import Link
from models import Link_Tuple
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
        return None
        html_content = response.status_code
    time_request = time_request + time.time() - now
    return html_content

def get_links(html, current_link : Link_Tuple):
    global time_parse
    now = time.time()
    soup = BeautifulSoup(html, 'lxml')
    container = soup.find('div', {'id': 'bodyContent'})
    if container is None:
        return []
    links = container.find_all('a')
    links_list = []
    tuple_list = []
    for link in links:
        if link.get('href') is None:
            continue
        if link.get('href').startswith('/wiki/') and ":" not in link.get('href'):
            temp_link = link.get('href')
            tuple_list.append(Link_Tuple(temp_link, current_link.link))
            links_list.append(temp_link)
    time_parse = time_parse + time.time() - now
    return tuple_list, links_list


count = 0
def list_to_str(list):
    string = ""
    for item in list:
        string = string + item + "\n"
    return string

def list_to_tuplelist(list, current_tuple : Link_Tuple):
    tuple_list = []
    for item in list:
        tuple_list.append(Link_Tuple(item, current_tuple.link))
    return tuple_list

def find_specific_link(link, list):
    for item in list:
        if item.link == link:
            return item
    return None


def find_path(visited):
    path = []
    last = visited[-1]
    while last is not None:
        path.append(last)
        last = find_specific_link(last.prev, visited)
    return path[::-1]

db_time = time.time()

async def main():
    global db_time
    global count

    success : bool = False
    start_link = "/wiki/Blackzilians"#"/wiki/Peter_Sitsen"
    goal = "/wiki/Adolf_Hitler"
    wiki = "https://en.wikipedia.org"
    html = get_html(wiki+start_link)
    start_link_tuple : Link_Tuple = Link_Tuple(start_link, None)
    links , trash = get_links(html, start_link_tuple)
    visited = [start_link_tuple]

    #BFS
    while links:
        if "_lists" in links:
            print("WTF")
            break
        current_tuple = links.pop(0)
        current_link = current_tuple.link
        if current_link in visited:
            continue
        visited.append(current_tuple)
        if current_link == goal:
            print("Found!")
            break
        else:
            #print("Not yet!", current_link)
            link_db : Link = await db.get_link(current_link)
            if link_db is not None and link_db != False:
                #temp_links = link_db.get_list()
                #links = links + list_to_tuplelist(temp_links, current_tuple)
                '''if goal in temp_links:
                    hitler_tuple = Link_Tuple(goal, current_link)
                    visited.append(hitler_tuple)
                    print("Found!", current_link)
                    success = True
                    break'''
                #print(count)
                #count += 1
                continue
            print(count, current_link)
            html = get_html(wiki + current_link)
            count += 1
            if html is None:
                continue
            
            new_links_tuples, new_links = get_links(html, current_tuple)
            temp = time.time()
            await db.create_link(current_link, list_to_str(new_links))
            db_time = db_time + (time.time() - temp)
            links = links + list_to_tuplelist(new_links, current_tuple)
            '''if goal in new_links:
                    hitler_tuple = Link_Tuple(goal, current_link)
                    visited.append(hitler_tuple)
                    print("Found!", current_link)
                    success = True
                    break'''

    print(find_path(visited))
    print(len(find_path(visited))-1, "clicks to reach Hitler's wiki page")

time_now = time.time()
asyncio.run(main())
print("Request time: ", time_request)
print("Parse time: ", time_parse)
print("Count: ", count)
print("Total time: ", time.time() - time_now)
print("Function times", time_request + time_parse)
print("DB time: ", db_time)