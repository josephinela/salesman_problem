from vertex import Vertex

class Graph:
    def __init__(self,num_vertices, directed=False):
        self.adjMatrix= [[0]*num_vertices for _ in range(num_vertices)]
        self.num_vertices = num_vertices
        self.vertices = []
        for i in range(num_vertices):
            newVertex = Vertex(i)
            self.vertices.append(newVertex)
        self.directed= directed
        self.vtx = 0

    def addVertex(self,id):
        if self.vtx<self.num_vertices:
            self.vertices[self.vtx].setVertexID(id)
            self.vtx +=1

    def getVertex(self,n):
        for vertexin in range(0,self.num_vertices):
            if n == self.vertices[vertexin].getVertexID():
                return vertexin
        return -1

    def addEdge(self,frm,to,cost):
        if self.getVertex(frm)!= -1 and self.getVertex(to) != -1:
            self.adjMatrix[self.getVertex(frm)][self.getVertex(to)] = cost
            if not self.directed:
                self.adjMatrix[self.getVertex(to)][self.getVertex(frm)]= cost

    def getVertices(self):
        vertices = []
        for vertexin in range(0,self.num_vertices):
            vertices.append(self.vertices[vertexin].getVertexID())
        return vertices

    def printMatrix(self):
        for u in range(0,self.num_vertices):
            row = []
            for v in range(0,self.num_vertices):
                row.append(self.adjMatrix[u][v])
            print('row', u ,':', row)

    def getEdges(self):
        edges = []
        for u in range(0,self.num_vertices):
            for v in range(0,self.num_vertices):
                if self.adjMatrix[u][v] != -1:
                    uid = self.vertices[u].getVertexID()
                    vid = self.vertices[v].getVertexID()
                    edges.append((uid,vid,self.adjMatrix[u][v]))
        return edges
