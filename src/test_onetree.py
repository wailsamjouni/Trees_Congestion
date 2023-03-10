import networkx as nx
import matplotlib.pyplot as plt
from GraphStructure import GraphStructure
from Graph import Graph
from Build import Build
import random
from collections import defaultdict

generate_graph = Graph(11, 13, filename='graph1113.pkl')
# generate_graph.save_to_file('graph1113.pkl')
# generate_graph = Graph(12, 9, filename='graph1211.pkl')  # test2
# generate_graph = Graph(17, 20, filename='graph1720.pkl')  # test3 gggg
# generate_graph = Graph(8, 8, filename='graph88.pkl') #test1
# generate_graph = Graph(8, 8, filename='graph1110.pkl')  # Important

g_copy = GraphStructure(generate_graph.get_graph(),
                        0, 5)

# g_copy.build(0.4, "onetree")

network = Build(g_copy)
network.build(0.4, "onetree")


graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"]
}

# destination_neighbors = ["C", "E", "F", "L"]
destination_neighbors = [0, 3, 2]


def search_path(graph, node, destination_neighbors, path, destination):
    path += [node]
    if node in destination_neighbors:
        return path
    for neighbor in graph[node]:
        if neighbor not in path:
            new_path = search_path(
                graph, neighbor, destination_neighbors, path, destination)
            if new_path:
                new_path.append(destination)
                return new_path
    return None


# graph = g_copy.buildone()

# path = search_path(graph, 1, destination_neighbors, [], 7)
# print(f"Path is {path}")

# pos = nx.circular_layout(graph)
# nx.draw(graph, with_labels=True, pos=pos)
# plt.show()
