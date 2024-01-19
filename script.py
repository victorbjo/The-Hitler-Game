import requests
from bs4 import BeautifulSoup
import time
import cchardet
from models import Link
from models import Link_Tuple
import asyncio
import db
import json
session = requests.Session()
def get_html(URL):
    response = session.get(URL)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print("Failed to retrieve content. Status code:", response.status_code)
        return None
        html_content = response.status_code
    return html_content

def get_links(html, current_link : Link_Tuple):
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
        path.append(last.link) if last.prev is not None else None
        last = find_specific_link(last.prev, visited)
    return path[::-1][:-1]

async def find_goal(start_link, goal = "/wiki/Adolf_Hitler"):
    success : bool = False
    wiki = "https://en.wikipedia.org"
    count_from_cache = 0
    count_from_web = 0
    html = get_html(wiki+start_link)
    start_link_tuple : Link_Tuple = Link_Tuple(start_link, None)
    links , trash = get_links(html, start_link_tuple)
    visited = [start_link_tuple]
    count = 0
    #BFS
    while links:
        if "_lists" in links: 
            break
        current_tuple = links.pop(0)
        current_link = current_tuple.link
        if current_link in visited:
            continue
        visited.append(current_tuple)
        if current_link == goal:
            break
        else:
            #print("Not yet!", current_link)
            link_db : Link = await db.get_link(current_link)
            if link_db is not None and link_db != False:
                temp_links = link_db.get_list()
                links = links + list_to_tuplelist(temp_links, current_tuple)
                if goal in temp_links:
                    hitler_tuple = Link_Tuple(goal, current_link)
                    visited.append(hitler_tuple)
                    success = True
                    break
                count += 1
                count_from_cache += 1
                continue
            html = get_html(wiki + current_link)
            count += 1
            count_from_web += 1
            if html is None:
                continue
            
            new_links_tuples, new_links = get_links(html, current_tuple)
            await db.create_link(current_link, list_to_str(new_links)) #Cache it
            links = links + list_to_tuplelist(new_links, current_tuple)
            if goal in new_links:
                    hitler_tuple = Link_Tuple(goal, current_link)
                    visited.append(hitler_tuple)
                    success = True
                    break
            
    path  = [start_link] + find_path(visited) + [goal]
    dict_to_return = {"path": path, "count": len(find_path(visited)), "count_from_cache": count_from_cache, "count_from_web": count_from_web}
    return dict_to_return

async def main():
    start_link = "/wiki/Blackzilians"#"/wiki/Peter_Sitsen"
    goal = "/wiki/Adolf_Hitler"
    start_time = time.time()
    request_dict = await find_goal(start_link, goal)
    request_dict["time"] = round(time.time() - start_time, 3)
    request_json = json.dumps(request_dict)
    print(request_json)


if __name__ == "__main__":
    asyncio.run(main())
