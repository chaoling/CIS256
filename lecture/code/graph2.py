'''
Nodes, Edges

Graph->Tree->Binary Tree->BST->Linked List
'''

'''
edge list:
[
    [0,1], [1,2],[1,3],[2,3]
]

adj list:
{
    a: [b,c],
    b: [d],
    c: [e],
    d: [],
    e: [b]
}
'''
import sys
from operator import ne
from typing import List


class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)

    def construct_graph(self, nodes, init_graph):
        '''
        This method makes sure that the graph is symmetrical. In other words, if there's a path from node A to B with a value V, there needs to be a path from node B to node A with a value V.
        '''
        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value

        return graph

    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes

    def get_neighbors(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections

    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]



def buildGraph(edges: List) -> dict:
    '''
    convert edge list to adj list
    for undirected graph
    edges = [
        ['i','j'],
        ['k','i'],
        ['m','k'],
        ['k','l'],
        ['o','n'],
    ]
    '''
    graph = {}
    for edge in edges:
        a,b = edge[0],edge[1]
        if not a in graph: #or we can use defaultdict(list) here to avoid this.
            graph[a] = []
        if not b in graph:
            graph[b] = []
        graph[a].append(b)
        graph[b].append(a)
    return graph

'''
ex1: undirected path
Write a function, undirectedPath, that takes in an array of edges from an undirected graph and two nodes (nodeA, nodeB)
The function should return a boolean indicating whether or not there exists a path between nodeA and nodeB
'''
def undirectedPath(edges: List[List], nodeA: str, nodeB: str) -> bool:
    def dfs(adj, src, dst, visited):
        if src == dst:
            return True
        for node in adj[src]:
            if not (node in visited):
                visited.add(node) #avoid cycles in the graph
                if dfs(adj, node, nodeB, visited): #think about: why this is wrong: return dfs(...)
                    return True

        return False #only when you have exhausted all pathes should you conclude and return False

    adj = buildGraph(edges)
    assert nodeA in adj
    visited = set(nodeA)
    return dfs(adj, nodeA, nodeB, visited)
  
'''
Ex2: connected component count
Write a function, connetedComponentsCount, that takes in the adj list of an undirected graph.
it should return the number of connected components within the graph
e.g:
connectedComponentsCount({
    0: [8,1,5],
    1: [0],
    5: [0,8],
    8: [0,5],
    2: [3,4],
    3: [2,4],
    4: [3,2]
})
ans: 2
also remember union find can also count number of connected components
'''
def connectedComponentsCount(adj: dict) -> int:
    def explore(adj, src, visited) -> bool:
        assert src in adj
        if src in visited:
            return False

        visited.add(src)
        for neighbor in adj[src]:
            explore(adj, neighbor,visited)
        return True #explore this component as far as possible

    count = 0
    visited = set()
    for node in adj:
        if  explore(adj, node, visited):
            count += 1

    return count


'''
Ex3: largest component
Write a function, largestComponent, that takes in the adj list of an undirected graph.
it should return the size of largest connected components within the graph
e.g:
connectedComponentsCount({
    0: [8,1,5],
    1: [0],
    5: [0,8],
    8: [0,5],
    2: [3,4],
    3: [2,4],
    4: [3,2]
})
ans: 4
'''

def largestComponents(adj: dict) -> int:
    def explore(adj, src, visited) -> int:
        assert src in adj
        count = 0
        if src in visited:
            return count

        visited.add(src)
        count += 1
        for neighbor in adj[src]:
            count += explore(adj, neighbor, visited)
        return count  # explore this component as far as possible

    maxSize = 0
    visited = set()
    for node in adj:
        size = explore(adj, node, visited)
        if size > maxSize:
            maxSize = size

    return maxSize

'''
Ex4: shortest path
Write a function, shortestPath, that takes in an array of edges for an undirected graph and two nodes (A,B)
it should return the length of the shortest path betwewen A and B, len is the number of edges in the path, 
not the number of nodes. return -1 is A->B does not exists a path
e.g:
edges: [
    ['w','x'],
    ['x','y'],
    ['z','y'],
    ['z','v'],
    ['w','v']
]
shortestPath(edges, 'w','z') -> 2
'''
from collections import deque
def shortestPath(edges: List[List], src, dst) -> int:
    graph = buildGraph(edges)
    visited = set(src) #to prevent cycle
    #use a queue to do bfs
    q = deque()
    q.append((src,0)) #distance to src is 0
    while len(q) > 0:
        node,distance = q.popleft()
        #check if we've reached destination or not
        if node == dst:
            return distance
        for neighbor in graph[node]:
            if not (neighbor in visited): #prevent cycle
                visited.add(neighbor)
                q.append((neighbor,distance+1)) #each neighbor added one distance to the src
    
    #don't forget the path does not exists case
    return -1


'''
Ex 5: 2D count island
island count
Write a function, islandCount, that takes in a grid containing Ws and Ls. 
W represents water and L represents land. The function should return the number of islands on the grid. 
An island is a vertically or horizontally connected region of land.
grid = [
  ['W', 'L', 'W', 'W', 'W'],
  ['W', 'L', 'W', 'W', 'W'],
  ['W', 'W', 'W', 'L', 'W'],
  ['W', 'W', 'L', 'L', 'W'],
  ['L', 'W', 'W', 'L', 'L'],
  ['L', 'L', 'W', 'W', 'W'],
]

island_count(grid) # -> 3
'''
def island_count(grid: List[List]) -> int:
    # this is the same as connected component problem
    # your adjacency list is bascically build on the run, aka four directions
    # need to check boundary conditions
    def explore(grid, r, c,visited) -> bool:
        #navigate the grid from the point(r,c), use dfs to touch every land in a connected component fashion
        #case 0: check the boundary:
        row = len(grid)
        col = len(grid[0])
        if r >= row or c >= col or r < 0 or c < 0:
            return False
        #case 1: if it is a water or already visited node, just return false
        
        if grid[r][c] == 'W' or f'{r},{c}' in visited:
            #print(f"water or already visited {r},{c}: {grid[r][c]}")
            return False

        visited.add(f'{r},{c}')
        #print(f"now processing...{r},{c}")

        for (dr, dc) in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            explore(grid, r+dr, c+dc, visited)

        return True  # I have at least one new land to explore

    #set up the way to navigate the grid
    count = 0
    visited = set()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if explore(grid, row, col, visited):
                count += 1
    return count
'''
minimum island
Write a function, minimum_island, that takes in a grid containing Ws and Ls. W represents water and L represents land. 
The function should return the size of the smallest island. An island is a vertically or horizontally connected region of land.

You may assume that the grid contains at least one island.
'''
def min_island(grid: List[List]) -> int:
    # this is the same as connected component problem
    # your adjacency list is bascically build on the run, aka four directions
    # need to check boundary conditions
    def explore(grid, r, c, visited) -> int:
        #navigate the grid from the point(r,c), use dfs to touch every land in a connected component fashion
        #case 0: check the boundary:
        row = len(grid)
        col = len(grid[0])
        if r >= row or c >= col or r < 0 or c < 0:
            return 0
        #case 1: if it is a water or already visited node, just return false

        if grid[r][c] == 'W' or f'{r},{c}' in visited:
            return 0

        visited.add(f'{r},{c}')
        size = 1  # count myself in first

        for (dr, dc) in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            size += explore(grid, r+dr, c+dc, visited)

        return size

    #set up the way to navigate the grid
    minSize = len(grid)*len(grid[0]) #sys.maxsize  # or the size of the grid
    visited = set()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            size = explore(grid, row, col, visited)
            if size != 0 and size < minSize:  # why size != 0?
                minSize = size

    return minSize
#dfs on graphs: use stack or recursion
#bfs: use queue
#review python inplementation of stack vs queue
from collections import deque

'''
stk = []
stk.append('a')
stk.pop()

q = deque()
q.append('b')
q.popleft()
'''
'''
n-> number of nodes
e-> number of edges (or n^2 for worse case, why?)
Time: O(e)
space: O(n)

'''

'''
dijstra's shortest path algorithm:
'''
def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    # Add the start node manually
    path.append(start_node)

    print("We found the following best path with a value of {}.".format(
        shortest_path[target_node]))
    print(" -> ".join(reversed(path)))


def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
 
    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph   
    shortest_path = {}
 
    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}
 
    # We'll use max_value to initialize the "infinity" value of the unvisited nodes   
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # However, we initialize the starting node's value with 0   
    shortest_path[start_node] = 0
    
    # The algorithm executes until we visit all nodes
    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes: # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
                
        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = graph.get_neighbors(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node
 
        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path


def heap_dijkstras(graph, root): #using priority queue or heapq
    import heapq


    # create our graph using an adjacency list representation
    # each "node" in our list should be a node name and a distance
    graph = {
        0: [(1, 1)],
        1: [(0, 1), (2, 2), (3, 3)],
        2: [(1, 2), (3, 1), (4, 5)],
        3: [(1, 3), (2, 1), (4, 1)],
        4: [(2, 5), (3, 1)]
    }
    n = len(graph)
    # set up "inf" distances
    dist = [sys.maxsize for _ in range(n)]
    # set up root distance
    dist[root] = 0
    # set up visited node list
    visited = [False for _ in range(n)]
    # set up priority queue
    pq = [(0, root)]
    # while there are nodes to process
    while len(pq) > 0:
        # get the root, discard current distance
        _, u = heapq.heappop(pq)
        # if the node is visited, skip
        if visited[u]:
            continue
        # set the node to visited
        visited[u] = True
        # check the distance and node and distance
        for v, l in graph[u]:
            # if the current node's distance + distance to the node we're visiting
            # is less than the distance of the node we're visiting on file
            # replace that distance and push the node we're visiting into the priority queue
            if dist[u] + l < dist[v]:
                dist[v] = dist[u] + l
                heapq.heappush(pq, (dist[v], v))
    return dist


def main():
    graph = {
        'a': ['b','c'], #put the next node at the end for stk, it will pick in reverse order it was received, ie, LIFO
        'b': ['d'],
        'c': ['e'],
        'd': ['f'],
        'e': [],
        'f': []
    }
    edges = [
        ['i', 'j'],
        ['k', 'i'],
        ['m', 'k'],
        ['k', 'l'],
        ['o', 'n'],
    ]
    adj2 = {
        0: [8, 1, 5],
        1: [0],
        5: [0, 8],
        8: [0, 5],
        2: [3, 4],
        3: [2, 4],
        4: [3, 2]
    }
    grid = [
        ['W', 'L', 'W', 'W', 'W'],
        ['W', 'L', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'L', 'W'],
        ['W', 'W', 'L', 'L', 'W'],
        ['L', 'W', 'W', 'L', 'L'],
        ['L', 'L', 'W', 'W', 'W'],
    ]
    print(connectedComponentsCount(adj2))
    print(largestComponents(adj2))
    print(shortestPath(edges, 'i','m'))
    print(island_count(grid))
    print(min_island(grid))
    #print(buildGraph(edges))
    #print(underictedPath(edges,'i','k'))
    nodes = ["Reykjavik", "Oslo", "Moscow", "London",
             "Rome", "Berlin", "Belgrade", "Athens"]

    init_graph = {}
    for node in nodes:
        init_graph[node] = {}

    init_graph["Reykjavik"]["Oslo"] = 5
    init_graph["Reykjavik"]["London"] = 4
    init_graph["Oslo"]["Berlin"] = 1
    init_graph["Oslo"]["Moscow"] = 3
    init_graph["Moscow"]["Belgrade"] = 5
    init_graph["Moscow"]["Athens"] = 4
    init_graph["Athens"]["Belgrade"] = 1
    init_graph["Rome"]["Berlin"] = 2
    init_graph["Rome"]["Athens"] = 2

    graph = Graph(nodes, init_graph)
    previous_nodes, shortest_path = dijkstra_algorithm(
        graph=graph, start_node="Reykjavik")
    print_result(previous_nodes, shortest_path,
                 start_node="Reykjavik", target_node="Belgrade")


if __name__ == "__main__":
    main()
