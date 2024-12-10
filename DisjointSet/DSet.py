class DisjointSetNode:
    def __init__(self, key):
        self.key = key
        self.parent = self
        self.rank = 0

def make_set(key):
    return DisjointSetNode(key)

def find_set(x):
    path = [x]
    if x != x.parent:
        current = x
        while current != current.parent:
            current = current.parent
            path.append(current)
        for node in path:
            node.parent = current  
    return x.parent, path

def union(tuple_x, tuple_y):
    x_root, _ = tuple_x
    y_root, _ = tuple_y
    
    if x_root.rank < y_root.rank:
        x_root.parent = y_root
    elif x_root.rank > y_root.rank:
        y_root.parent = x_root
    else:
        y_root.parent = x_root
        x_root.rank += 1


def kruskal(graph):
    minimum_spanning_tree = []
    graph.sort(key=lambda x: x[2]) 
    vertices = set()
    
    for edge in graph:
        u, v, weight = edge
        vertices.add(u)
        vertices.add(v)
    
    sets = {vertex: make_set(vertex) for vertex in vertices}
    
    for edge in graph:
        u, v, weight = edge
        u_root, _ = find_set(sets[u])
        v_root, _ = find_set(sets[v])
        if u_root != v_root:
            minimum_spanning_tree.append((u, v, weight))
            union((u_root, None), (v_root, None)) 
    
    return minimum_spanning_tree


graph = [
    ('A', 'B', 4),
    ('A', 'H', 8),
    ('B', 'C', 8),
    ('B', 'H', 11),
    ('C', 'I', 2),
    ('C', 'D', 7),
    ('C', 'F', 4),
    ('D', 'E', 9),
    ('D', 'F', 14),
    ('E', 'F', 10),
    ('F', 'G', 2),
    ('G', 'I', 6),
    ('G', 'H', 1),
    ('H', 'I', 7)
]

minimum_spanning_tree = kruskal(graph)
for edge in minimum_spanning_tree:
    print(f"Edge: {edge[0]}-{edge[1]}, Weight: {edge[2]}")



Z = []
for i in range(1, 11):
    Z.append(make_set(i))


union(find_set(Z[0]),find_set(Z[1]))
union(find_set(Z[2]),find_set(Z[3]))
union(find_set(Z[4]),find_set(Z[3]))
union(find_set(Z[0]),find_set(Z[4]))
union(find_set(Z[5]) ,find_set(Z[6]) )
union(find_set(Z[7]) ,find_set(Z[8]) )
union(find_set(Z[5]) ,find_set(Z[7]) )
union( find_set(Z[6]) , find_set(Z[3]) )




for i in range(9):
    root, path = find_set(Z[i])
    print(f"Klucz {Z[i].key} nalezy do zbioru o reprezentancie {root.key} i sciezka do korzenia: {[node.key for node in path]}")