from GraphStructure import GraphStructure
import networkx as nx


class Build:

    def __init__(self, graph_structure: GraphStructure):
        self.graph_structure = graph_structure

    def number(self):
        return self.graph_structure.graph.number_of_nodes()

    def build(self):
        number_of_nodes = self.graph_structure.graph.number_of_nodes()
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

        shortest_path_after_removing_failededges = self.graph_structure.compute_shortest_path(
            failed_edges)
        # self.graph_structure.set_failed_edges(failed_edges)

        contains_all_edps_fails = self.graph_structure.failed_in_all_edps(
            edge_disjoint_paths, failed_edges)

        if contains_all_edps_fails:
            one_tree = self.graph_structure.oneTree(
                edge_disjoint_paths, reverse=True)
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

        path = self.graph_structure.compute_shortest_path(failed_edges)

        self.graph_structure.remove_failed_edges(failed_edges)
        number_of_nodes_after = self.graph_structure.graph.number_of_nodes()

        self.graph_structure.edps_in_ascending_order(edge_disjoint_paths)

        # isReachable = self.graph_structure.is_source_still_reachable()

        # if isReachable:
        #     print(shortest_path_after_removing_failededges, "still a path from", self.graph_structure.source, "to",
        #           self.graph_structure.destination, "in the modified graph")

        #     # calculate Edps again
        #     edps_after_cut_edges = list(nx.edge_disjoint_paths(
        #         self.graph_structure.graph, self.graph_structure.source, self.graph_structure.destination))
        #     common_edge_disjoint_paths = set(
        #         edge_disjoint_paths).intersection(edps_after_cut_edges)
        #     if len(common_edge_disjoint_paths) != 0:
        #         print(
        #             f"We still can reach the destination from the source using those originl edge disjoint paths : {common_edge_disjoint_paths}")

        # else:
        #     print("The destination cannot be reached anymore")
