import networkx as nx
import matplotlib.pyplot as plt
from GraphStructure import GraphStructure
from Graph import Graph
from Build import Build
import random

generate_graph = Graph(11, 10, filename='graph1718.pkl')
# generate_graph.save_to_file('graph1110.pkl')

g_copy = GraphStructure(generate_graph.get_graph(), 11, 3)
number_of_nodes = g_copy.graph.number_of_nodes()
print(f"Number of nodes of the graph: {number_of_nodes}")
g_copy.give_attrs_to_graph()

# g = g_copy.build()
attr_node = nx.get_node_attributes(g_copy.graph, "attr")
print(
    f"The attributes of the nodes before computing the EDPs :{attr_node}")
print("------------------------------------------------------")
attr_edge = nx.get_edge_attributes(g_copy.graph, "attr")
print(
    f"The attributes of the edges before computing the EDPs :{attr_edge}")
print("------------------------------------------------------")

edge_disjoint_paths = g_copy.compute_and_sort_edps()
print(
    f"The EDPs between source and destination are : {edge_disjoint_paths}")
print("------------------------------------------------------")

g_copy.number_the_computed_edps(edge_disjoint_paths)
failed_edges_random = g_copy.generate_random_failed_edges(0.3)
print(
    f"The generated failed edges are : {failed_edges_random}")
print("------------------------------------------------------")

shortest_path_after_removing_failededges = g_copy.compute_shortest_path(
    failed_edges_random)

# Convert paths to edges
edps_edge_list = []
for edge_disjoint_path in edge_disjoint_paths:
    path_edges = [(edge_disjoint_path[i], edge_disjoint_path[i+1])
                  for i in range(len(edge_disjoint_path) - 1)]
    edps_edge_list.append(path_edges)
print(edps_edge_list)

# Make edge failures
failed_edges = []
for edp in edps_edge_list:
    failed_edges.append(random.choice(edp))
print(
    f"*************************************************************************{failed_edges}")

# Check if all paths suffer a failure
contains = g_copy.failed_in_all_edps(edge_disjoint_paths, failed_edges)
if contains:
    one_tree = g_copy.oneTree(edge_disjoint_paths, reverse=True)

    attr_edge = nx.get_edge_attributes(g_copy.graph, "attr")
    print(
        f"The attributes of the edges after computing the EDPs :{attr_edge}")
    print("------------------------------------------------------")

    destination_incidents = g_copy.find_destination_incidents()
    print(f"The incidents of the destination are : {destination_incidents}")
    print("------------------------------------------------------")

    g_copy.disconnect_the_edges_of_the_destination()
    print(
        f"The edges with attribut -1  are : {destination_incidents}")
    print("------------------------------------------------------")

    pruned_graph = g_copy.prune_branches_from_tree(
        str(len(edge_disjoint_paths)), destination_incidents)

    attr_node_after = nx.get_node_attributes(g_copy.graph, "attr")
    print("*********************************************************************")
    print("*********************************************************************")
    print(
        f"The attributes of the nodes after pruning :{attr_node_after}")
    print("------------------------------------------------------")
    attr_edge_after = nx.get_edge_attributes(g_copy.graph, "attr")
    print(
        f"The attributes of the edges after pruning :{attr_edge_after}")
    print("------------------------------------------------------")

    path = g_copy.compute_shortest_path(failed_edges)
    g_copy.remove_failed_edges(failed_edges)
    number_of_nodes_after = g_copy.graph.number_of_nodes()
    print(
        f"Number of nodes of the graph after pruning: {number_of_nodes_after}")

    g_copy.one_tree_routing(
        one_tree, failed_edges, edge_disjoint_paths, number_of_nodes, number_of_nodes_after)

    pos = nx.circular_layout(pruned_graph)
    nx.draw(pruned_graph, with_labels=True, pos=pos)
    plt.show()

else:
    g_copy.multipleTree(edge_disjoint_paths)


# g_copy.colorize_paths(edge_disjoint_paths)
