from GraphStructure import GraphStructure
import networkx as nx
import logging
import matplotlib.pyplot as plt


class Build:

    def __init__(self, graph: GraphStructure):
        self.graph = graph

    def build(self, fraction, version=None):

        logger = self.graph._get_logger('build.log')

        edge_disjoint_paths = self.graph.compute_and_sort_edps()
        logger.info(
            f'EDPS between {self.graph.source} and {self.graph.destination} are :{edge_disjoint_paths}')

        edge_attrs = nx.get_edge_attributes(self.graph.graph, "attr")
        logger.info(f'Attributes before extending EDP : {edge_attrs}')

        destination_incidents = self.graph.find_destination_incidents()
        logger.info(f'Destination neighbors are : {destination_incidents}')

        self.graph.number_the_computed_edps(edge_disjoint_paths)

        edge_attrs_after = nx.get_edge_attributes(self.graph.graph, "attr")
        logger.info(
            f'Attributes after numbering the EDPs : {edge_attrs_after}')

        # failed_edges_random = self.graph.generate_random_failed_edges(fraction)
        failed_edges_random = [(5, 10), (0, 2), (1, 2), (1, 6)]
        logger.warning(f'Failed edges are : {failed_edges_random}')

        shortest_path_after_removing_failededges = self.graph.compute_shortest_path(
            failed_edges_random)
        logger.info(
            f'Shortest path after removing failed edges: {shortest_path_after_removing_failededges}')

        # One tree building
        if version == "onetree":

            number = self.graph.oneTree(edge_disjoint_paths, reverse=True)
            logger.debug(f'One tree choosed')

            edps = sorted(list(nx.edge_disjoint_paths(
                self.graph.graph, self.graph.source, self.graph.destination)), key=len, reverse=False)
            logger.debug(f'The sorted EDPs are : {edps}')

            logger.info(
                f'Updated edps between {self.graph.source} and {self.graph.destination} are : {edps}')

            edge_attrs_after = nx.get_edge_attributes(self.graph.graph, "attr")
            logger.info(
                f'Attributes after building one tree : {edge_attrs_after}')

            self.graph.disconnect_the_edges_of_the_destination()

            self.graph.prune_akt(destination_incidents, number)
            self.graph.remove_failed_edges(failed_edges_random)
            # self.graph.remove_unconnected_nodes()

            Tree = nx.Graph()
            for first_node, second_node, data in self.graph.graph.edges(data=True):
                if data["attr"] == str(number):
                    Tree.add_edge(first_node, second_node)

            edge_attrs_pruned = nx.get_edge_attributes(
                self.graph.graph, "attr")
            logger.debug(
                f'Attributes after pruning the tree : {edge_attrs_pruned}')

            logger.warning(f'Tree is : {Tree}')

            self.graph.one_tree_routing(edps, Tree,
                                        destination_incidents, failed_edges_random)
            logger.info('Routing has just begun')
            logger.debug(f'Tree with attr {len(edps)} is : {Tree.edges}')

            pos = nx.circular_layout(Tree)
            nx.draw(Tree, with_labels=True, pos=pos)
            plt.show()

            # pos = nx.circular_layout(self.graph.buildone())
            # nx.draw(self.graph.buildone(), with_labels=True, pos=pos)
            # plt.show()

        else:
            logger.debug(f'Multiple tree choosed')
            for edge_disjoint_path in edge_disjoint_paths:

                tree_attr = self.graph.tree_based_edge(edge_disjoint_paths,
                                                       edge_disjoint_path)
                self.graph.disconnect_the_edges_of_the_destination()

                self.graph.prune_akt(destination_incidents, tree_attr)
