"""Altered to collet the time finished with the node"""
from adjGraph import Graph
class DFSGraph(Graph):
    def __init__(self):
        super().__init__()
        self.time = 0
        self.topoArray = []

    def dfs(self):
        for aVertex in self:
            aVertex.setColor('white')
            aVertex.setPred(-1)
        for aVertex in self:
            if aVertex.getColor() == 'white':
                self.dfsvisit(aVertex)
        self.topoArray.sort(key=lambda x: x[1])
        self.topoArray.reverse()
        

    def dfsvisit(self,startVertex):
        startVertex.setColor('gray')
        self.time += 1
        startVertex.setDiscovery(self.time)
        for nextVertex in startVertex.getConnections():
            if nextVertex.getColor() == 'white':
                nextVertex.setPred(startVertex)
                self.dfsvisit(nextVertex)
        startVertex.setColor('black')
        self.time += 1
        startVertex.setFinish(self.time)
        self.topoArray.append([startVertex.getId(),startVertex.getFinish()])
