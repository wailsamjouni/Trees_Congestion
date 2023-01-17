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
            print(path_list)
        number_tree = number_tree + 1 if not reverse else number_tree - 1

#################################################################################################


def oneTreeImplementation(graph_copy, edp):
    number_tree = 1
    # if reverse:
    #     edps.reverse()
    #     number_tree = len(edps)
    # else:
    #     number_tree = 1
    number_of_nodes_added = 0
    for i in range(1, len(edp) - 1):
        path_list = edp
        print(path_list)
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
    print(path_list)
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


def routing(source, destination, failedEdges, graph, version="one"):

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

    # number the paths
    giveThePathsNumbers(g_copy, edps, build_time_edps)

    # Give the failededges attr "failed" True value
    for fail in failedEdges:
        g_copy[fail[0]][fail[1]]["failed"] = True

    # Building of trees either one or multiple tree
    startTreeBuilding = timer()
    if version == "one":
        oneTree(g_copy, edps, reverse=True)
    else:
        multipletree(g_copy, edps)
    endBuildingTree = timer()
    Timetaken = endBuildingTree - startTreeBuilding

    # Remove destination edges from all structures
    destination_incidents = removeDestinationIncidentFromAllStructures(
        g_copy, destination)

    # Find the edges of the source node
    source_incidents = findTheIncidentsOfSource(g_copy, source)

    # truncate the trees to remove unwanted branches
    startTreeTruncating = timer()

    endTreeTruncating = timer()
    timeTruncating = endTreeTruncating - startTreeTruncating

#################################################################################################
#################################################################################################
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

    def giveThePathsNumbers(graph, edps, build_time_edps):
        number_path = 1
        for edp in edps:
            for i in range(0, len(edp) - 1):
                if graph.nodes[edp[i+1]]["attr"] != "d":
                    graph.nodes[edp[i+1]]["attr"] = str(number_path)
                graph.nodes[edp[i]][edp[i+1]]["attr"] = str(number_path)
            number_path += 1
        build_finished = timer()
        time_of_build = build_finished - build_time_edps

    def removeDestinationIncidentFromAllStructures(graph, destination):
        destination_incidents = set()
        for destination_edge in graph.edges(destination):
            destination_incidents.add(destination_edge[1])
            graph[destination_edge[0]][destination_edge[1]]["attr"] = -1
        return destination_incidents

    def findTheIncidentsOfSource(graph, source):
        source_incidents = set()
        for source_edge in graph.edges(source):
            source_incidents.add(source_edge[1])
        return source_incidents

    def truncateTreesBranches(graph, source, source_incidents, destination_incidents, edps, tree_attributes=None):
        trees_attributes = []
        if tree_attributes is None:
            for u, v, data in graph.edges(data=True):
                if data["attr"] not in trees_attributes and int(data["attr"]) > 0:
                    trees_attributes.append(data["attr"])
        else:
            trees_attributes.append(tree_attributes)

        # Reconstructing all the trees
        for attribute in trees_attributes:
            Tree = nx.Graph()
            for u, v, data in graph.edges(data=True):
                if data["attr"] == attribute:
                    Tree.add_edge(u, v)
            node_list = list(Tree.nodes)

            # If the source node in the tree
            if source in node_list:
                depth_first_search = list(nx.dfs_labeled_edges(Tree, source))
                for firstNode, secondNode, direction in depth_first_search:
                    # Either "forward", "nontree" or "reverse"
                    # nontree edge is one in which both u and v have been visited but the edge is not in the DFS tree.
                    if direction == "nontree" or firstNode == secondNode:
                        depth_first_search.remove(
                            (firstNode, secondNode, direction))
                visited_nodes = set()
                edges_of_tree = set()
                visited_nodes.add(depth_first_search[0][0])

                # Pass through the matrix generated by dfs
                for i in range(len(depth_first_search)):
                    firstNode, secondNode, direction = depth_first_search[i]
                    # "forward" means that firstNode has been visited but scondNode has not
                    if direction == "forward":
                        visited_nodes.add(firstNode)
                    if direction == "reverse":
                        edges_of_tree.add((firstNode, secondNode))


                    #################################################################################################
                    #################################Create Graph##################################################
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

# G.add_edges_from([("s", "a")])
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

# The source and the destination node have their own separate attributes ('s' and 'd' respectively)
nx.set_edge_attributes(G, "0", "attr")
nx.set_node_attributes(G, "0", "attr")

G.nodes["s"]["attr"] = "s"
G.nodes["s"]["label"] = "s"
G.nodes["d"]["attr"] = "d"
G.nodes["d"]["label"] = "d"

# print(list(nx.dfs_labeled_edges(G, "s")))

dfs = list(nx.dfs_labeled_edges(G, "s"))
for n1, n2, label in dfs:
    if label == "nontree" or n1 == n2:
        dfs.remove((n1, n2, label))


print(dfs)

node_attr = nx.get_node_attributes
edge_attr = nx.get_edge_attributes
list_of_nodes = list(G.nodes)
source = list_of_nodes.index("s")
destination = list_of_nodes.index("d")


paths = list(nx.edge_disjoint_paths(
    G, "s", "d"))
paths.sort(key=lambda x: len(x), reverse=True)

# my_edp = paths[0]
# nx.draw(G.subgraph(extended_path), pos=pos,
#         node_color="blue", edge_color='blue')
# oneTreeImplementation(G, my_edp)
# nx.draw(G.subgraph(paths[1]), pos=pos, node_color="blue", edge_color='blue')

nx.draw(G, with_labels=1, node_color='red', pos=pos)
plt.show()


def calculateTheBestRouteToDestination(g_copy, source, destination, d_incidents):
    trees_attributes = []
    for firstNode, secondNode, data in g_copy.edges(data=True):
        if data["attr"] not in trees_attributes and int(data["attr"]) > 0:
            trees_attributes.append(data["attr"])

    for attribute in trees_attributes:
        Tree = nx.Graph()
        for firstNode, secondNode, data in g_copy.edges(data=True):
            if data is not None and "attr" in data and data["attr"] == attribute:
                Tree.add_edge(firstNode, secondNode)
        if source in list(Tree.nodes):
            depth_first_search = list(nx.dfs_labeled_edges(Tree, source))
            for firstNode, secondNode, direction in depth_first_search:
                if direction == "nontree" or firstNode == secondNode:
                    depth_first_search.remove(
                        (firstNode, secondNode, direction))
        else:
            continue
