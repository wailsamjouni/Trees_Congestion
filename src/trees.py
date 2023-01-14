#################################################################################################
####################################################Bibliotheken#############################
#################################################################################################
import networkx as nx
import matplotlib.pyplot as plt
import copy
from timeit import default_timer as timer

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

#################################################################################################


#################################################################################################
####################################Begin OneTree#####################################
def oneTree(graph_copy, edps, reverse=False):

    if reverse:
        edps.reverse()
        number_tree = len(edps)
    else:
        number_tree = 1
    for edp in edps:
        number_of_nodes_added = 0
        for i in range(1, len(edp) - 1):
            path_list = [edp[i]]
            iteration = 0
            while (iteration < len(path_list)):
                adjacent_edges_of_node = list(
                    graph_copy.edges(path_list[iteration]))
                edges_belong_no_structure = (edge for edge in adjacent_edges_of_node if
                                             graph_copy.get_edge_data(edge[0], edge[1]).get("attr") == "0")
                for edge in edges_belong_no_structure:
                    if graph_copy.nodes[edge[1]]["attr"] == "0":
                        graph_copy[edge[0]][edge[1]]["attr"] = str(number_tree)
                        graph_copy.nodes[edge[1]]["attr"] = str(number_tree)

                        path_list.append(edge[1])
                        number_of_nodes_added += 1

                    if graph_copy.nodes[edge[1]]["attr"] == "d":
                        graph_copy[edge[0]][edge[1]]["attr"] = str(number_tree)
                iteration += 1
        number_tree = number_tree + 1 if not reverse else number_tree - 1
#################################################################################################
######################################End OneTree#########################################################
#################################################################################################
######################################Begin MultipleTree#########################################################
#################################################################################################


def multipletree(graph_copy, edps):
    number_tree = 1
    for edp in edps:
        number_of_nodes_added = 0
        for i in range(1, len(edp) - 1):
            path_list = [edp[i]]
            iteration = 0
            while (iteration < len(path_list)):
                adjacent_edges_of_node = list(
                    graph_copy.edges(path_list[iteration]))
                edges_belong_no_structure = (edge for edge in adjacent_edges_of_node if
                                             graph_copy.get_edge_data(edge[0], edge[1]).get("attr") == "0")
                for edge in edges_belong_no_structure:
                    node_incident_attrs = [
                        graph_copy[e[0]][e[1]]["attr"] for e in graph_copy.edges(edge[1])]
                    if str(number_tree) not in node_incident_attrs and graph_copy[edge[0]][edge[1]]["attr"] == "0" and graph_copy.nodes[edge[1]]["attr"] != "s" and graph_copy.nodes[edge[1]]["attr"] != "d":
                        graph_copy.nodes[edge[0]][edge[1]
                                                  ]["attr"] = str(number_tree)
                        graph_copy.nodes[edge[1]]["attr"] = str(number_tree)
                        path_list.append(edge[1])
                        number_of_nodes_added += 1
                    if graph_copy.nodes[edge[1]]["attr"] == "d":
                        graph_copy[edge[0]][edge[1]]["attr"] = str(number_tree)
                iteration += 1
        number_tree += 1


###############################################################################################
#################################################################################################
def routing(source, destination, failedEdges, graph):

    # copy of the original Graph
    g_copy = copy.deepcopy(graph)

    shortest_path = computeShortestPath(
        graph, source, destination, failedEdges)

    # Assign the nodes and edges attribut 0
    nx.set_edge_attributes(g_copy, "0", "attr")
    nx.set_node_attributes(g_copy, "0", "attr")

    # Assign source and destination node 's' and 'd' attributes respectively
    g_copy.nodes[list_of_nodes[source]]["attr"] = "s"
    g_copy.nodes[list_of_nodes[source]]["label"] = "s"

    g_copy.nodes[list_of_nodes[destination]]["label"] = "d"
    g_copy.nodes[list_of_nodes[destination]]["label"] = "d"

    try:
        build_time_edps = timer()
        edps = list(nx.edge_disjoint_paths(g_copy, source, destination))
    except:
        # that means that the destination cannot be reached
        return (True, 0, 0, [])

    # Sort the computed edps
    edps.sort(key=lambda x: len(x), reverse=False)

    #################################################################################################
    # remove failed edges and compute the shortest path

    def computeShortestPath(graph, source, destination, failedEdges):
        graph.remove_edges_from(failedEdges)
        try:
            shortest_path = nx.shortest_path_length(graph, source, destination)
        except nx.NetworkXNoPath:
            shortest_path = -1
        return shortest_path
#################################################################################################
    # number the paths

    def giveThePathsNumbers(graph, edps):
        number_path = 1
        for edp in edps:
            for i in range(0, len(edp) - 1):
                if graph.nodes[edp[i+1]]["attr"] != "d":
                    graph.nodes[edp[i+1]]["attr"] = str(number_path)
                graph.nodes[edp[i]][edp[i+1]]["attr"] = str(number_path)
            number_path += 1
        build_finished = timer()
        time_of_build = build_finished - build_time_edps


#################################################################################################
#################################################################################################
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

G.add_edges_from([("s", "a"), ("s", "b")])
G.add_edges_from([("a", "c")])
G.add_edges_from([("c", "e")])
G.add_edges_from([("e", "f"), ("e", "d"), ("e", "h")])
G.add_edges_from([("f", "g")])
G.add_edges_from([("g", "d")])
G.add_edges_from([("h", "d")])
G.add_edges_from([("d", "i"), ("d", "l")])
G.add_edges_from([("i", "j")])
G.add_edges_from([("l", "j")])
G.add_edges_from([("b", "k")])
G.add_edges_from([("k", "l")])

pos = {"s": [0, 0], "a": [2, 1], "b": [2, -1], "c": [4, 2], "e": [6, 1], "f": [8, 2], "g": [10,
                                                                                            2], "h": [9, -0.3], "d": [12, 1], "i": [14, 1], "k": [6, -1], "l": [12, -1], "j": [14, -0.6]}

nx.set_edge_attributes(G, "0", "attr")
nx.set_node_attributes(G, "0", "attr")

node_attr = nx.get_node_attributes
edge_attr = nx.get_edge_attributes
list_of_nodes = list(G.nodes)
source = list_of_nodes.index("s")
destination = list_of_nodes.index("d")


paths = list(nx.edge_disjoint_paths(
    G, "s", "d"))
print(len(paths))
print(paths[0])
x = False
list_of_incident_edges = list(G.edges(paths[0][0]))
if G.nodes[list_of_nodes[source]]["attr"] == "0":
    x = True
print(x)

first_path = paths[0]
node_candidate_incident_attrs = [G[e[0]][e[1]]["attr"]
                                 for e in G.edges(first_path[3])]
print(node_candidate_incident_attrs)
print(G.edges("e"))

nx.draw(G, with_labels=1, node_color='red', pos=pos)
plt.show()


g_copy = copy.deepcopy(G)
nx.set_edge_attributes(g_copy, "0", "attr")
nx.set_node_attributes(g_copy, "0", "attr")
