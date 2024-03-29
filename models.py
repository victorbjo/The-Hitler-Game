#import named tuple 
from collections import namedtuple
class Link():
    def __init__(self, link : str = "", link_list = "") -> None:
        self.link = link
        self.link_list = link_list
        if type(link) != str:
            self._list_to_string()
        self.dist = None
        self.next = None
        self.prev = None
        self.id = None
    def _list_to_string(self):
        empty_str = ""
        for x in self.link_list:
            empty_str += f"{str(x)},"
        self.link_list = empty_str

    def get_list(self):
        #_list = self.link_list.replace(",", "/,/")
        _list = self.link_list.split("\n")
        return [x.strip() for x in _list]

    def load_from_db(self, db_link):
        self.link = db_link[1]
        self.dist = db_link[2]
        self.next = db_link[3]
        self.link_list = db_link[4]
    
    def __repr__(self) -> str:
        return f"Link(link={self.link}, link_list={self.link_list.count(',')+1})" 
Link_Tuple : namedtuple = namedtuple("Link_Tuple",["link", "prev"])#Fix named tuples
#First tuple will have cost 1, second will have cost 2 unless it is known it points to hitler. In that case 

if __name__ == "__main__":
    pass
    print(Link_Tuple(3,"germany","germans"))
    #print(Link_Tuple(2,1,"europe","germany"))
    #print(Link_Tuple(2,0,"world","europe"))
    #print(heapq.heappop(q