class Vertex:
    def __init__(self,node):
        self.id= node
        self.visited = False

    def addNeighbor(self,neighbor,G):
        G.addEdge(self.id,neighbor)

    def getConnections(self,G):
        return G.adjMatrix[self.id]

    def getVertexID(self):
        return self.id

    def setVertexID(self,id):
        self.id= id

    def setVisited(self):
        self.visited = True

    def __str__(self):
        return str(self.id)