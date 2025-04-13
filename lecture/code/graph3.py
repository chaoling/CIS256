from typing import List
'''
Top 5 graph algorithms :
1. DFS
2. BFS
3. Union Find:*Forest of Trees e.g: Number of Connected Components in undirectly graph LC 323
4. Topological Sort (DAG) e.g: Alien Dictionary O(N) LC 269, LC 207 (medium) course schedule
5. Dijkstra's shortest path algorithm O(ElogV), heap or priority queue , hashset. e.g: Network delay time LC743
'''
'''
6. Prims or Kruskal's MST LC 1584 Min Cost to Connect All Points
7. Bellman Ford
8. Floyed Warshall's Algorithms
'''

'''
example 1:
LC 953: Verifying an Alien Dictionary
In an alien language, surprisingly, they also use English lowercase letters, but possibly in a different order. The order of the alphabet is some permutation of lowercase letters.

Given a sequence of words written in the alien language, and the order of the alphabet, return true if and only if the given words are sorted lexicographically in this alien language.

 

Example 1: easy

Input: words = ["hello","leetcode"], order = "hlabcdefgijkmnopqrstuvwxyz"
Output: true
Explanation: As 'h' comes before 'l' in this language, then the sequence is sorted.
Example 2:

Input: words = ["word","world","row"], order = "worldabcefghijkmnpqstuvxyz"
Output: false
Explanation: As 'd' comes after 'l' in this language, then words[0] > words[1], hence the sequence is unsorted.
Example 3:

Input: words = ["apple","app"], order = "abcdefghijklmnopqrstuvwxyz"
Output: false
Explanation: The first three characters "app" match, and the second string is shorter (in size.) According to lexicographical rules "apple" > "app", because 'l' > '∅', where '∅' is defined as the blank character which is less than any other character (More info).
'''


def isAlienSorted(words: List[str], order: str) -> bool:
      #pair-wise compare in order it was received in the original words list, if there is any contradiction, return false
      #first diff char
      #if word A is prefix of word B, word B must be AFTER word A
    orderIndex = {c:i for i,c in enumerate(order)} 
    print(orderIndex)
    for i in range(len(words)-1):
        w1, w2 = words[i], words[i+1]
        #minLen = min(len(w1), len(w2))
        for j in range(len(w1)):
            if j == len(w2):
                return False
            if w1[j] != w2[j]:
                #first char that differs
                if orderIndex[w1[j]] > orderIndex[w2[j]]:
                    return False
                break  # early break, this pair is in order

        #else:
        #    if len(w1) > len(w2) and w1[:minLen] == w2[:minLen]:
        #        return False
    return True
'''
example 2: alien dictionary (LC269) hard

There is a new alien language that uses the English alpahbet. However, the order among the letters is unknown to you
 You are given a list of strings words from the alien language's dictionary, where the strings 
 in words are sorted lexicographically by the rules of this new language.

 Return a string of the unique letters in the new alien language sorted in lexicographically increasing order
 by the new languages's rules. If there is no solution, return "".
 If there are multiple solutions, return any of them

 A string s is lexcographically smaller than a string t if at the first letter where they differ, the letter in s comes efore the letter in t in the alien language.
 If the first min(s.length, t.length) letters are the same, then s is smaller if and only if s.length < t.length.
 (prefix always smaller ) . ape < apes

chars of a word not in order, the words are in order, 
find adjacency list of each unique char by iterating through adjacent words 
and finding first chars that are different, 
run topsort on graph and do loop detection;

e.g:
words: = ['wrt','wrf','er','ett','rftt']
ans: w,e,r,t,f

compare pair-wise of words in the list
t->f w->e, r->t, e->r ==> w->e->r->t->f (it is already sorted topologically!!!)
no-cycles! otherwise contradition! 

another case: multiple solutions, delete last word in words
r->t->f
w->e
order: r->t->f w->e
    or: rw te f

another example:
A
BA
BC
C
A->B->C or A->C->B?
dfs don't work here, unless it is Post order dfs, aka do the leaf nodes first then root, 
build it in reverse order!
CBA->ABC

also visit: -> false to start
     path: current visiting
'''

#topsort: post order dfs + cycle detection + reverse
def alien_dictionary(words: List[str]) -> str:
    #1st: build up the adjacency list
    adj = {
        c:set() for w in words for c in w
    }
    #print(adj)
    for i in range(len(words)-1):
        w1, w2 = words[i], words[i+1]
        minLen = min(len(w1),len(w2))
        #check invalid case
        if len(w1) > len(w2) and w1[:minLen] == w2[:minLen]:
            return ""
        #find the first different char
        for j in range(minLen):
            if w1[j] != w2[j]:
                adj[w1[j]].add(w2[j]) #build up the adj list by adding second char to the set keyed by first char
                break

    # now do dfs search to do topological sort
    visiting = dict() # False means not in the current path, but touched, True means visiting (aka, current path)
    res = [] #contains the list of nodes sorted topologically in reverse order due to post order dfs, aka, handle the node when leaving the node
    def topSort(c,visiting:dict)->bool:
        #post order traversal of the adj list
        if c in visiting:
            return visiting[c] #if returns a true, means you saw this node twice! loop detected
        visiting[c] = True
        for neighbor in adj[c]:
            if topSort(neighbor,visiting):
                return True #detected a loop, return immediately!!!

        visiting[c] = False #post order, don't forget to do this step to backtrack
        res.append(c) #post order, end results in reverse order
    
    for c in adj: #doesn't matter which node to start first
        if topSort(c,visiting):
            return "" #loop detected!
    print(res)
    res.reverse() #don't forget to reverse the result list
    return "".join(res)

'''
There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
Return true if you can finish all courses. Otherwise, return false.

also see: Course schedule II (LC 210)

Example 1:

Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: There are a total of 2 courses to take. 
To take course 1 you should have finished course 0. So it is possible.
Example 2:

Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: There are a total of 2 courses to take. 
To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.

prereq =[
    [0,1],
    [0,2],
    [1,3],
    [1,4],
    [3,4]
]
''' 


class Solution:
    from collections import defaultdict

    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        '''
        pre: List([ai,bi]) aka: bi->ai
        O(n+p), n is the number of courses, p is the prerequisites
        
        '''
        #build the adj list
        #adj = defaultdict(list)
        adj = {i:[] for i in range(numCourses)}

        for course, pre in prerequisites:
            #or the other way around: course -> list of prerequisites
            adj[course].append(pre)
            #adj[i[1]].append(i[0])  # directed graph

        #course_schedule = [] if you want to also track the actual schedule of course
        visiting = set()
        #do topologial sort using dfs

        def dfs(course: int) -> bool:
            if course in visiting:
                return False #cycle detected!
            if adj[course] == [] #no prerequisite for this one
                return True
            visiting.add(course)
            for pre in adj[course]:
                if not dfs(pre):
                    return False  # cycle detected, return immediately!

            # post order traversal, leaving the node, mark it not in current path and put it onto the schedule
            visiting.remove(course)
            #course_schedule.append(course)
            return True

        for i in range(numCourses):
            if not dfs(i, visiting):
                return False  # cycle detected, not able to do the schedule DAG

        return True

        '''
        Course schedule II:
        '''
        #do topologial sort using dfs
    def course_schedule2(self, numCourses: int, prerequisite: List[List[int]]) -> List[int]:
        #build adj list of prerequites:
        prereq = { c:[] for c in range(numCourses)}
        for crs, pre in prerequisite:
            prereq[crs].append(pre)
        # a course has 3 possible states:
        # visited -> crs has been added to output
        # visiting -> crs not added to output, but added to cycle
        # unvisited -> crs not added to output or cycle
        output = []
        visited, cycle = set(), set()
        def dfs(course: int) -> bool:
            if course in cycle:
                # if True , means you have already encounted this node twice! cycle detected
                return False
            if course in visited:
                return True # this is already visited and added to the output

            cycle.add(course)
            for pre in prereq[course]:
                if dfs(pre) == False:
                    return False  # cycle detected, return immediately!

            # post order traversal, leaving the node, mark it not in current path and put it onto the schedule
            cycle.remove(course)
            visited.add(course)
            output.append(course)
            
        for c in range(numCourses):
            if dfs(c) == False:
                return []

        return output
'''
similar problem: LC457
Example 3: number of connected components in an Undirected Graph
[Medium]
You have a graph of n nodes. You are given an integer and an array edges where
edges[i] = [ai,bi] indicates that there is an edge between ai and bi in the graph

return the number of connected components in the graph
e.g: input: n = 5, edges = [
    [0,1],
    [1,2],
    [3,4]
]
output: 2
Union Find: forest of trees

parent[0,1,2,3,4] : each index represents the node index
rank[1,1,1,1,1] : size of each node if it is the parent

initially, each node is its own parents
then merge nodes and update parents, always add to the root parents hence minimize the root of tree
every time a union action, decrement the number of isolated components by 1
return immediately when they have the same parents
'''  
def countComponentsUnionFind(n: int, edges: List[List[int]]) -> int:
    #initially, each node is treated as isolated, and it's parent is it self.
    parent = [i for i in range(n)]
    rank = [1] * n #each node has rank 1, aka, only one node

    def find(node): # find the root parent of the node
        res = node
        while res != parent[res]: #stop when the parent of the node is itself, aka the root parent
            parent[res] = parent[parent[res]] #path compression, optimization step
            res = parent[res]
        return res

    def union(n1,n2):
        p1,p2 = find(n1), find(n2)
        if p1 == p2:
            return 0 #already unioned, return without doing anything more
        if rank[p2] > rank[p1]:
            parent[p1] == p2
            rank[p2] += rank[p1]
        else:
            parent[p2] = p1
            rank[p1] += rank[p2]
        return 1
    
    res = n
    for n1, n2 in edges:
        res -= union(n1,n2)
    return res

'''
LC684 Redundant Connection
a tree is an undirected graph that is connected and has no cycles
you are given a graph that started as a tree with n nodes labeled from 1 to n, with one additional edge aded. 
The added edge has two different vertices chosen from 1 to n, and was not an edge that already existed. 
The graph is represented as an array edges of length n where edges[i] = [ai,bi] indicates there is an edge between 
nodes ai and bi in the graph

Return an edge that can be removed so that the resuting graph is a tree of n nodes.
If there are multiple answers, return the answer that occurs last in the input
e.g: 1->2->3->1
input edges = [
    [1,2],
    [1,3],
    [2,3]
]
answer [2,3]
first edge in the input array edges that cause a cycle (redundant edge) is the answer, why?
to find the redundant edge, use union-find algorithm, if two nodes has the same parent, 
the edge is redundant
'''
def findRedundantConnection(edges: List[List[int]]) -> List[int]:
    parent = [i for i in range(len(edges) +1)] #initially, each node has itself as its own parent
    rank = [1] * (len(edges)+1) #each node has rank 1 #of nodes = edges +1 

    def find(n): #find the common parent of two nodes if possible
        p = parent[n]

        while p != parent[p]: #keep looking up for ancessestor until #1
            parent[p] = parent[parent[p]] #path compression to find the grandgrand parent 2xfaster
            p = parent[p]
        return p
    
    def union(n1, n2):
        p1, p2 = find(n1), find(n2)
        if p1 == p2:
            return False #redundant connection found, end of game!
        #union n1 and n2 by setting the parent of child node to another node
        #also update the rank of new parent node 
        if rank[p1] > rank[p2]: #make p2 child of p1
            parent[p2] = p1
            rank[p1] += rank[p2]
        else:
            parent[p1] = p2
            rank[p2] += rank[p1]
        return True

    for n1, n2 in edges:
        if not union(n1, n2):
            return [n1,n2]


'''
LC 743. Network Delay Time (medium)
You are given a network of n nodes, labeled from 1 to n. You are also given times, a list of travel times as directed edges
times[i] = (ui, vi, wi) where ui is the source node, vi is the target node, and wi is teh time it takes for a signal to travel from source to target

we will send a signal from a given node k. Return the time it takes for all the n nodes to receive the signal if it is impossible for all the n nodes
to recieve the signal, return -1

Input: times =[
    [2,1,1],
    [2,3,1],
    [3,4,1],
]
n = 4, k=2
Output: 2



BFS using minHeap or priority queue (pathLen, node) (0,1)(1,3)(4,2)....
dijkstra shortest path algorithms
O(ElogV)
'''
from collections import defaultdict, deque
import heapq
def networkDelayTime(times: List[List[int]], n: int, k: int) -> int:
    #build adj list from edges
    edges = defaultdict(list)
    for u,v,w in times:
        edges[u].append((v,w))
    '''
    def build_adj(edges:List[List[int]])->dict: #return dict of src->[dst, weight]
        res = defaultdict(list)
        for edge in edges:
            src,dst,weight = edge[0], edge[1], edge[2]
            res[src].append((dst,weight))
        return res
    '''
    minHeap =[(0,k)] #use list of nodes first, then heapify
    visited = set()
    t = 0
    while minHeap:
        w1, n1 = heapq.heappop(minHeap)
        if n1 in visited:
            continue
        visited.add(n1)
        t = max(t, w1)
        for n2,w2 in edges[n1]:
            if n2 not in visited:
                heapq.heappush(minHeap, (w2+w1,n2))

        return t if len(visited) == n else -1
        #we've visited every single node 

'''
MST: LC1584. Min Cost to to Connect All Points
Prim's algorithm
You are givan an array points represting integer coordinates of some points on a 2D-plane, 
where point[i] = [xi, yi]
the cost of connecting two points [xi, yi] and [xj, yj] is the manhattan distance between them:
abs(xi-xj) + abs(yi-yj), 

return the minimum cost to make all points conneted (MST), all poins are connected if there is exactly one simple path
between any two points

O(n2logn) we can add each node n times, thus n^2 part
Input: points = [
    [0,0],
    [2,2],
    [3,10],
    [5,2],
    []
]

dsA: visit(hashset) to avoid cycle, minHeap as frontier ([weight, node])
if len of visit nodes is equal to total number of nodes (all nodes visited in the path), we can stop
'''
def mst(points: List[List[int]]) -> int:
    res = 0
    N = len(points)
    adj = {i:[] for i in range (N)} #i: lit of [cost, node]
    for i in range(N):
        x1, y1 = points[i]
        for j in range (i+1,N):
            x2, y2 = points[j]
            dist = abs(x1-x2) +abs(y1-y2)
            adj[i].append([dist,j])
            adj[j].append([dist,i]) #two ways as it is undirected graph

    #prim's
    visit = set()
    minHeap = [[0,0]] #cost, point
    while len(visit) < N:
        cost, i = heapq.heappop(minHeap)
        if i in visit:
            continue
        res += cost
        visit.add(i)
        for neiCost, nei in adj[i]:
            if nei not in visit:
                heapq.heappush(minHeap, [neiCost,nei])
    return res

'''
Bellman Ford: O(E*V) [where you can stop at k stop, hence the O(E*K)]
adv: can deal with negative weights, abritraige
BFS 
LC 787 Cheapest Flights Within K Stops, 
There are n cities connected by some number of flights. 
You are given an array flights where flights[i] = [fromi, toi, pricei] 
indicates that there is a flight from city fromi to city toi with cost pricei.
You are also given three integers src, dst, and k, 
return the cheapest price from src to dst with at most k stops. If there is no such route, return -1.

Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 1
Output: 200
Explanation: The graph is shown.
The cheapest price from city 0 to city 2 with at most 1 stop costs 200, as marked red in the picture.
 
e.g 2:
Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 0
Output: 500
Explanation: The graph is shown.
The cheapest price from city 0 to city 2 with at most 0 stop costs 500, as marked blue in the picture.
'''
import sys
def findCheapestPrice(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    #from src (A), do BFS, for each node, track the minimum weight to each dst within k stop, 
    # aka doing k+1 layer of BFS
    #prices: A(0)  B(1)   C(2)
    # .      0 inf inf
    #tmp:    A . B . C
    # .      0   100 500
    prices = [sys.maxsize] * n #initialize to infinity float("inf") except the src
    prices[src] = 0
    #at most k+1 layers since k stop:
    for _ in range(k + 1):
        tmpPrices = prices[:]
        for s,d,p in flights: #src, dst, price
            if prices[s] == sys.maxsize:
                continue
            if prices[s] + p < tmpPrices[d]: #update the table
                tmpPrices[d] = prices[s] + p
        prices = tmpPrices

    return -1 if prices[dst] == sys.maxsize else prices[dst]



def main():
    words = ['wrt', 'wrf', 'er', 'ett', 'rftt']
    order = "hlabcdefgijkmnopqrstuvwxyz"
    edges = [
        [0, 1],
        [1, 2],
        [3, 4]
    ]
    alien_dictionary(words)
    print(isAlienSorted(words,order))
    print(countComponentsUnionFind(5,edges))
    flights = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
    src = 0
    dst = 2
    k = 0
    n = 3
    findCheapestPrice(n, flights,src,dst,k)


if __name__ == "__main__":
    main()

