'''
Nodes, Edges

Graph->Tree->Binary Tree->BST->Linked List
'''

'''
Directions and Cycles
Directed Graph,
DAG-> Directed Acyclic Graph
Connectivity: minimum number of nodes that can be removed before the graph becomes disconnected
question: which graph has stronger connectivity?
Disconnected
Disconnected graphs are very similar whether the graph's directed or undirected—there is some vertex or group of vertices that have no connection with the rest of the graph.

Weakly Connected
A directed graph is weakly connected when only replacing all of the directed edges with undirected edges can cause it to be connected. 
Imagine that your graph has several vertices with one outbound edge, meaning an edge that points from it to some other vertex in the graph. 
There's no way to reach all of those vertices from any other vertex in the graph, but if those edges were changed to be undirected all vertices would be easily accessible.

Connected
Here we only use "connected graph" to refer to undirected graphs. In a connected graph, there is some path between one vertex and every other vertex.

Strongly Connected
Strongly connected directed graphs must have a path from every node and every other node. So, there must be a path from A to B AND B to A.
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
#dfs on graphs: use stack or recursion
#bfs: use queue
#review python inplementation of stack vs queue
from collections import deque

from numpy import True_
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

def dfsPrint(graph: dict, source):
    #iteratively
    stk = [source]
    while len(stk) > 0:
        current = stk.pop()
        print(current)

        for neighbor in graph[current]:
            stk.append(neighbor)


def dfsPrintRecursion(graph: dict, source):
    #recursively
    print(source)
    for neighbor in graph[source]:
        dfsPrintRecursion(graph, neighbor) #notice the order is different than that in dfsPrint iteratively
   #this is because in recursive fashion, b is dealt with first in [b,c], in stack fashion,
   # c is dealt with fist in [b,c] push to stack, LIFO 

def bfsPrint(graph: dict, source):
    #always in iterative code
    q = deque(source)
    while len(q) > 0:
        current = q.popleft()
        print(current)
        for neighbor in graph[current]:
            q.append(neighbor)

def hasPathRecursive(graph: dict, src, dst) -> bool:
    #assume no cycle, if it does , need to use visited[] to avoid repetition
    if src == dst:
        return True
    for neighbor in graph[src]:
        if hasPathRecursive(graph, neighbor, dst):
            return True
    else:
        return False #pay attention to where you return False...  


def hasPathbfs(graph: dict, src, dst) -> bool:
    #assume no cycle, if it does , need to use visited[] to avoid repetition
    q = [src]

    while len(q) > 0:
        current = q.pop(0)
        if current == dst:
            return True
        for neighbor in graph[current]:
            q.append(neighbor)
        
    return False



def main():
    graph = {
        'a': ['b','c'], #put the next node at the end for stk, it will pick in reverse order it was received, ie, LIFO
        'b': ['d'],
        'c': ['e'],
        'd': ['f'],
        'e': [],
        'f': []
    }
    dfsPrint(graph, 'a')
    print("-----------")
    dfsPrintRecursion(graph, 'a')
    print("-----------")
    bfsPrint(graph, 'a')
    print("-----------")
    print(hasPathbfs(graph, 'e', 'a'))
    print(hasPathRecursive(graph, 'a', 'f'))


if __name__ == "__main__":
    main()
