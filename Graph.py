class Graph:
    def __init__(self, vertices = 0, edges = [], directed = False):      
        self.vertices = set()
        if type(vertices) is int:
            self.vertices = set(range(vertices))
        elif type(vertices) is list:
            self.vertices = set(vertices)
        
        if not type(edges) is list:
            raise TypeError("'edges' should be a list")
        self.edges = {}
        self.directed = directed
        for v in self.vertices:
            self.edges[v] = {}
        for (v1, v2, w) in edges:
            if v1 == v2:
                continue
            self.edges[v1][v2] = w
            if (not directed):
                self.edges[v2][v1] = w
                
    def neighbours(self, v):
        if self.directed:
            neighbours = self.out_neighbours(v)
            neighbours.update(self.in_neighbours(v))
            return neighbours
        else:
            return self.out_neighbours(v)
        
    def out_neighbours(self, v):
        return set([v2 for (v2, w) in self.edges[v].items()])
    
    def in_neighbours(self, v):
        neighbours = set()
        for (k, edges) in self.edges.items():
            if k != v and v in edges:
                neighbours.add(k)
        return neighbours
    
    def order(self, v):
        return len(self.neighbours(v))
    
    def add_vertex(self, v):
        if v not in self.vertices:
            self.vertices.add(v)
            self.edges[v] = {}
            
    def add_vertices(self, vertices):
        for v in vertices:
            self.add_vertex(v)
            
    def remove_vertex(self, v):
        if v in self.vertices:
            self.vertices.discard(v)
            del self.edges[v]
            for (k, edges) in self.edges.items():
                edges.pop(v, None)
    
    def remove_vertices(self, vertices):
        for v in vertices:
            self.remove_vertex(v)
                
    def add_edge(self, e):
        (v1, v2, w) = e
        if v1 not in self.vertices:
            raise ValueError("Vertex {} is not in the graph".format(v1))
        if v2 not in self.vertices:
            raise ValueError("Vertex {} is not in the graph".format(v2))
        self.edges[v1][v2] = w
        if (not self.directed):
            self.edges[v2][v1] = w
    
    def add_edges(self, edges):
        for e in edges:
            self.add_edge(e)
            
    def remove_edge(self, e):
        (v1, v2) = e
        if v1 not in self.vertices:
            raise ValueError("Vertex {} is not in the graph".format(v1))
        if v2 not in self.vertices:
            raise ValueError("Vertex {} is not in the graph".format(v2))
        self.edges[v1].pop(v2, None)
        if (not self.directed):
            self.edges[v2].pop(v1, None)
            
    def remove_edges(self, edges):
        for e in edges:
            self.remove_edge(e)
            
    def is_bipartite(self):
        assignments = {}
        done = set()
        working_list = list(self.vertices)
        while len(working_list) != 0:
            cur = working_list.pop()
            if cur in done:
                continue
            done.add(cur)
            if cur not in assignments:
                assignments[cur] = 1
            assignment = assignments[cur]
            for v in self.neighbours(cur):
                if v in assignments and assignments[v] == assignment:
                    return False
                assignments[v] = 3 - assignment
                working_list.append(v)
        return True
    
    def get_components(self):  
        components = []
        vertices_left = set(self.vertices)
        while vertices_left:
            cur = vertices_left.pop()
            component = set()
            working_set = set([cur])
            while working_set:
                cur_2 = working_set.pop()
                if cur_2 not in component:
                    component.add(cur_2)
                    vertices_left.discard(cur_2)
                    working_set.update(self.neighbours(cur_2))
            components.append(component)
        return components