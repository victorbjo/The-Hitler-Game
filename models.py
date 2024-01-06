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
        return self.link_list.split(",")

    def load_from_db(self, db_link):
        self.link = db_link[1]
        self.dist = db_link[2]
        self.next = db_link[3]
        self.link_list = db_link[4]
    
    def __repr__(self) -> str:
        return f"Link(link={self.link}, link_list={self.link_list.count(',')+1})" 