#################################################################################################
####################################################Bibliotheken#############################
#################################################################################################
import networkx as nx
import matplotlib.pyplot as plt
import copy
from timeit import default_timer as timer
from GraphStructure import GraphStructure
from Graph import Graph
# from TreesAlgorithms import TreesAlgorithms
from networkx.algorithms.traversal.depth_first_search import dfs_tree
from networkx.algorithms.simple_paths import all_simple_paths
from Build import Build


#########################################################################################
#############################Each EDP belong to a Structure##################################################


def build_structure_of_edps(g, source, destination):
    g_copy = copy.deepcopy(g)
    nx.set_edge_attributes(g_copy, "0", "attr")
    try:
        edps = list(nx.edge_disjoint_paths(g_copy, source, destination))
        edps.sort(key=lambda x: len(x), reverse=False)
    except:
        return (True, 0, 0, [])

    path_number = 1
    edps_attributes = []
    for edp in edps:
        for i in range(0, len(edp) - 1):
            g_copy[edp[i]][edp[i+1]]["attr"] = str(path_number)
            if str(path_number) not in edps_attributes:
                edps_attributes.append(str(path_number))


##############################################
G = nx.Graph()

G.add_node("s")
G.add_node("a")
G.add_node("b")
G.add_node("c")
G.add_node("e")
G.add_node("f")
G.add_node("g")
G.add_node("h")
G.add_node("i")
G.add_node("j")
G.add_node("k")
G.add_node("l")
G.add_node("d")
G.add_node("x")
G.add_node("y")
G.add_node("z")


# G.add_edges_from([("s", "a")])
G.add_edges_from([("s", "a"), ("s", "b")])
G.add_edges_from([("a", "c")])
G.add_edges_from([("c", "e")])
G.add_edges_from([("e", "f"), ("e", "d"), ("e", "h")])
# G.add_edges_from([("f", "g")])
G.add_edges_from([("g", "d")])
# G.add_edges_from([("h", "d")])
G.add_edges_from([("h", "d"), ("h", "x"), ("h", "y")])
G.add_edges_from([("d", "i"), ("d", "l")])
G.add_edges_from([("i", "j")])
G.add_edges_from([("l", "j")])
G.add_edges_from([("b", "k"), ("b", "z")])
G.add_edges_from([("k", "l")])

pos = {"s": [0, 0], "a": [2, 1], "b": [2, -1], "z": [1, 0], "c": [4, 2], "e": [6, 1], "f": [8, 2], "g": [10,
                                                                                                         2], "h": [9, -0.3], "x": [8, -0.7], "y": [7, -0.7], "d": [12, 1], "i": [14, 1], "k": [6, -1], "l": [12, -1], "j": [14, -0.6]}

# The source and the destination node have their own separate attributes ('s' and 'd' respectively)

G.nodes["s"]["attr"] = "s"
G.nodes["s"]["label"] = "s"
G.nodes["d"]["attr"] = "d"
G.nodes["d"]["label"] = "d"

# g1 = nx.Graph(nx.read_graphml('dataset.graphml'))
# nx.draw(g1, with_labels=True)
# plt.show()


# test_graph.save_to_file('graph2217.pkl')
# test_graph.draw()
structure = GraphStructure(test_graph.get_graph(), 1, 17)
edps = structure.compute_and_sort_edps()
# print(edps)
# structure.colorize_paths(edps)
