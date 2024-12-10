import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def read_graph_from_file(filename):
    with open(filename, 'r') as file:
        N = int(file.readline().strip())
        
        adjacency_matrix = []
        
        for _ in range(N):
            line = file.readline().strip()
            row = list(map(int, line.split()))
            adjacency_matrix.append(row)
            
    return N, adjacency_matrix



class Graph:
    def __init__(self, filename):
        self.N, self.adj  = read_graph_from_file(filename)
        self.visited = [False] * self.N
        self.traversal_order = []
        self.spanning_tree_edges = []

    def dfs(self, start):
        self.visited[start] = True
        self.traversal_order.append(start)

        for i in range(self.N):
            if self.adj[start][i] == 1 and not self.visited[i]:
                self.spanning_tree_edges.append((start, i))
                self.dfs(i)

    def dfs_traversal(self, start):
        self.visited = [False] * self.N
        self.traversal_order = []
        self.spanning_tree_edges = []
        self.dfs(start)
        print("dfs Traversal order:", self.traversal_order)
        print("Spanning tree edges:", self.spanning_tree_edges)

    def bfs(self, start):
        queue = deque([start])
        self.visited[start] = True

        while queue:
            vertex = queue.popleft()
            self.traversal_order.append(vertex)
            for i in range(self.N):
                if self.adj[vertex][i] == 1 and not self.visited[i]:
                    queue.append(i)
                    self.visited[i] = True
                    self.spanning_tree_edges.append((vertex, i))

    def bfs_traversal(self, start):
        self.visited = [False] * self.N  
        self.traversal_order = []  
        self.spanning_tree_edges = []  
        self.bfs(start)
        print("BFS Traversal order:", self.traversal_order)
        print("BFS Spanning tree edges:", self.spanning_tree_edges)


    def visualize_graph(self):
        G = nx.DiGraph()
        for i in range(self.N):
            for j in range(self.N):
                if self.adj[i][j] == 1:
                    G.add_edge(i, j)

        pos = nx.spring_layout(G)
        plt.figure(figsize=(12, 10))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=3000, arrowsize=20)
        plt.title("Graph Visualization")
        plt.show()

    def visualize_spanning_tree(self):
        G = nx.DiGraph()
        G.add_edges_from(self.spanning_tree_edges)

        pos = nx.spring_layout(G)
        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=3000, arrowsize=20)
        plt.title("Spanning tree visualization")
        plt.show()

def main():
    filename = 'input2.in'

    graph = Graph(filename)
    graph.visualize_graph()

    graph.dfs_traversal(0)
    graph.visualize_spanning_tree()

    graph.bfs_traversal(0)
    graph.visualize_spanning_tree()

if __name__ == '__main__':
    main()