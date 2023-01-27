from GraphStructure import GraphStructure
import networkx as nx


class Build:

    def __init__(self, graph_structure: GraphStructure):
        self.graph_structure = graph_structure

    def build(self, version="oneTree"):

        self.graph_structure.give_attrs_to_graph()
        node_attr = nx.get_node_attributes(self.graph_structure.graph, "attr")
        print(
            f"The attributes of the nodes before computing the EDPs :{node_attr}")
        print("------------------------------------------------------")

        edge_disjoint_paths = self.graph_structure.compute_and_sort_edps()
        print(
            f"The EDPs between source and destination are : {edge_disjoint_paths}")
        print("------------------------------------------------------")

        self.graph_structure.number_the_computed_edps(edge_disjoint_paths)
        failed_edges = self.graph_structure.generate_random_failed_edges(0.3)
        self.graph_structure.set_failed_edges(failed_edges)

        if version == "oneTree":
            self.graph_structure.oneTree(edge_disjoint_paths, reverse=False)
        else:
            self.graph_structure.multipleTree(edge_disjoint_paths)

        destination_incidents = self.graph_structure.find_destination_incidents()
        print(
            f"The incidents of the destination are : {destination_incidents}")
        print("------------------------------------------------------")

        node_attr_after = nx.get_node_attributes(
            self.graph_structure.graph, "attr")
        print(
            f"The attributes of the nodes before computing the EDPs :{node_attr_after}")
        print("------------------------------------------------------")

        self.graph_structure.disconnect_the_edges_of_the_destination()

        print(
            f"The edges with attribut -1  are : {self.graph_structure.edges_attrs_of_destination()}")

        pruned_graph = self.graph_structure.prune_branches_from_tree(
            "2", destination_incidents)
