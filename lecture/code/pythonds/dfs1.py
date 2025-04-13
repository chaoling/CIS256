'''
Write a function, undirectedPath() that takes in an array of edges from an undirected graph and two nodes (nodeA, nodeB)

The function should return a boolean indicating whether or not there exists a path between nodeA and nodeB

'''
from collections import defaultdict,List

'''
convert edge list to adj list for undirected graph
    edges = [
        ['i','j'],
        ['k','i'],
        ['m','k'],
        ['k','l'],
        ['o','n'],
    ]
'''
def buildGraph(edges: List) -> dict:
    graph = defaultdict(list)
    for edge in edges:
        a,b = edge[0],edge[1]
        graph[a].append(b)
        graph[b].append(a)
    return graph

def underectedPath(edges: List[List], nodeA: str, nodeB: str) -> bool:
    def dfs(adj, src, dst, visited):
        if src == dst:
            return True
        for node in adj[src]:
            if not (node in visited):
                visited.add(node) #avoid cycles in the graph
                if dfs(adj, node, nodeB, visited):
                    return True
        return False #only when you have exhausted all should you conclude and return False
    adj = buildGraph(edges)
    assert nodeA in adj
    visited = set(nodeA)
    return dfs(adj, nodeA, nodeB, visited)
