import sys
from collections import deque

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file, encoding='utf-8') as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        self.title_to_id = {title: id for id, title in self.titles.items()}


        # Read the links file into self.links.
        with open(links_file, encoding='utf-8') as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        # 辞書を使ってstartとgoalをO(1)で見つける
        start_id = self.title_to_id.get(start)
        goal_id = self.title_to_id.get(goal)

        if start_id == goal_id:
                return print(self.titles[start_id])   
         
        queue = deque([start_id]) #startのみをqueueに入れる
        visited = set() #visitedのリストの用意
        prev = {start_id: None}

        while queue: #queueのからpopしてくる言葉に関して
            current = queue.popleft() #queueの出口に一番近い言葉を出す
            #print(current)
            if current in visited:
                continue  # 無限ループ防げる
            visited.add(current)
            
            if current == goal_id: #もしcurrentが目的地の言葉だったら
                path = []
                while current is not None:
                    path.append(self.titles[current])
                    current = prev[current]
                path.reverse()
                print(path)
                return path
                       
            for neighbor in self.links.get(current, []): #currentからリンクされてる言葉に対して
                if neighbor not in visited and neighbor not in prev: #訪問済みリストに言葉が入っていないなら
                    prev[neighbor] = current #今までの経路をnew_pathに代入
                    queue.append(neighbor) #neighborをqueueの入り口に追加
                    visited.add(neighbor)

        print("could not find shortest path") #経路が見つからなかったことを知らせる
        return None 

    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        self.pagerank = {id: 1.0 for id in self.titles}
        delta = sum((new_pagerank[id]- self.pagerank[id]) ** 2 for id in self.titles)
        self.pagerank = new_pagerank

        while True:
            total_no_link = sum(self.pagerank[id] for id in self.titles if not self.links.get(id))
            new_pagerank = {id:0.0 for id in self.titles}

            for id in self.titles:
                neighbors = self.links.get(id,[])
                if not neighbors:
                    continue
                distributed = self.pagerank[id] / len(neighbors)
                for neighbor in neighbors:
                    new_pagerank[neighbor] += distributed

            for id in self.titles:
                new_pagerank[id] += 0.15 / len(self.titles)
                new_pagerank[id] += 0.85 * total_no_link / len(self.titles)           

            delta = sum((new_pagerank[id]- self.pagerank[id]) ** 2 for id in self.titles)
            print(delta) #deltaがどう少なくなっていっているか確認するため
            if delta < 0.01:
                break 
            self.pagerank = new_pagerank

        most_popular_pages = sorted(self.pagerank.items(), key=lambda x: x[1], reverse=True)[:10]
        for page_id, score in most_popular_pages:
            print(self.titles[page_id], self.pagerank[page_id])

    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal 
    #page.
    def find_longest_path(self, start, goal):
        #------------------------# shortest pathの逆をやればよい！大きい値を残して小さいのを消す、みたいな。
        # Write your code here!  #
        #------------------------#
        pass

    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("usage: %s pages_file links_file" % sys.argv[0])
    #     exit(1)
    pages_file = "pages_medium.txt"
    links_file = "links_medium.txt"

    wikipedia = Wikipedia(pages_file, links_file)
    # Example
    # wikipedia.find_longest_titles()
    # Example
    # wikipedia.find_most_linked_pages()
    # Homework #1
    # wikipedia.find_shortest_path("A", "B")

    # wikipedia.find_shortest_path("渋谷", "パレートの法則")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    # wikipedia.find_longest_path("渋谷", "池袋")

    # the concept of iterations...