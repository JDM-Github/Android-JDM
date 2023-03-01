class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.adj = [[] for i in range(vertices)]
    
    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)
    
    def print_graph(self):
        for i in range(self.V):
            print("Vertex", i, ": ", end="")
            for j in self.adj[i]:
                print(j, end=" ")
            print()
