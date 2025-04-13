#https: // leetcode.com/problems/is-graph-bipartite/discuss/1790276/graph-dfs
from typing import List
from collections import defaultdict, deque

class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        visited = set()
        # true means one color, false means another color
        color = defaultdict(bool)
        self.ans = True

        def bfs(n: int) -> None:
            visited.add(n)
            q = deque()
            q.append(n)
            while q and self.ans:
                v = q.popleft()
                for w in graph[v]:
                    if w not in visited:
                        color[w] = not color[v]
                        visited.add(w)
                        q.append(w)
                    else:
                        if color[w] == color[v]:
                            self.ans = False
                            return

        def dfs(n: int) -> None:
            if not self.ans:
                return  # already not a bipartite, no need to go further
            visited.add(n)
            for w in graph[n]:
                if w in visited:
                    # check if n and its neighbour are of the same color or not, check bipartite
                    if color[w] == color[n]:
                        self.ans = False
                else:
                    #update the visited set
                    visited.add(w)
                    #make sure you color it differently than the parent node
                    color[w] = not color[n]
                    # depth first search
                    dfs(w)
            return

        n = len(graph)

        for i in range(n):
            if i not in visited and self.ans:
                bfs(i)

        return self.ans

sol = Solution()
graph = [[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]
graph2 = [[1, 3], [0, 2], [1, 3], [0, 2]]
assert(sol.isBipartite(graph) == False)
assert(sol.isBipartite(graph2) == True)

#https://leetcode.com/problems/possible-bipartition/discuss/1790334/bipartie

'''
convert in to a bipartie problem, also notice the node # start at 1
'''
class Solution:

  def possibleBipartition(self, n: int, dislikes: List[List[int]]) -> bool:
       def buildGraph(n: int, dislikes: List[List[int]]) -> List[List[int]]:
            ans = [[] for _ in range(n+1)]  # node number start with 1

            for fr, to in dislikes:
                ans[fr].append(to)
                ans[to].append(fr)
            return ans

        def isBipartie(n: int, graph: List[List[int]]) -> bool:
            self.ok = True
            visited = set()
            color = defaultdict(bool)

            def dfs(v):
                visited.add(v)
                for w in graph[v]:
                    if w not in visited:
                        visited.add(w)
                        color[w] = not color[v]
                        dfs(w)
                    else:
                        if color[w] == color[v]:
                            self.ok = False
                            return

            for i in range(1, n+1):
                if i not in visited:
                    dfs(i)
            return self.ok

        graph = buildGraph(n, dislikes)

        return isBipartie(n, graph)
