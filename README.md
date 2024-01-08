# The-Hitler-Game
A fun project in Python, implementing The Wikipedia Hitler game using BFS.

### V1:
BFS works,  
https://en.wikipedia.org/wiki/Modulo -> https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss  
(2 links deep, 260 links visited ~23sec)  
### V1.1:  
SQL caching of links to save on request and parsing time  
https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss - > /wiki/Adolf_Hitler  
(3 links deep, 1156 links visited ~150sec)@nocache  
(3 links deep, 1156? links visited ~8sec)@cache  


## TODO
- [X] Implement DB caching of links to save time on requests and parsing
- [ ] Implement some node pathplanning like properties, e.g., Min heap(Based on current cost and cost to hitler(CTH))
- [ ] Create web interface to visualize the "Wiki crawl"
