from graph import Graph
from vertex import Vertex
from collections import deque


def bfs(g: Graph, start: Vertex):
  start.setDistance(0)
  start.setPred(None)
  vertQueue = deque()
  vertQueue.append(start)
  while (vertQueue.size() > 0):
    currentVert = vertQueue.popleft()
    for nbr in currentVert.getConnections():
      if (nbr.getColor() == 'white'):
        nbr.setColor('gray')
        nbr.setDistance(currentVert.getDistance() + 1)
        nbr.setPred(currentVert)
        vertQueue.append(nbr)
    currentVert.setColor('black')
