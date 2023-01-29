import networkx as nx
import matplotlib.pyplot as plt
import copy
import random


class GraphStructure:
    def __init__(self, graph, source, destination):
        self.graph = copy.deepcopy(graph)
        self.source = source
        self.destination = destination

    def give_attrs_to_graph(self):
        nx.set_edge_attributes(self.graph, "0", "attr")
        nx.set_node_attributes(self.graph, "0", "attr")
        self.graph.nodes[self.source]["attr"] = "s"
        self.graph.nodes[self.source]["label"] = "s"
        self.graph.nodes[self.destination]["label"] = "d"
        self.graph.nodes[self.destination]["attr"] = "d"
        return self.graph

    def compute_and_sort_edps(self):
        edge_disjoint_paths = list(
            nx.edge_disjoint_paths(self.graph, self.source, self.destination))
        edge_disjoint_paths.sort(key=lambda x: len(x), reverse=False)
        return edge_disjoint_paths

    def is_spanning_tree(self):
        return len(list(
            nx.edge_disjoint_paths(self.graph, self.source, self.destination))) == 1

    def number_the_computed_edps(self, edge_disjoint_paths):
        number_tree = 1
        for edge_disjoint_path in edge_disjoint_paths:                                                    #
            for i in range(0, len(edge_disjoint_path)-1):
                if self.graph.nodes[edge_disjoint_path[i+1]]["attr"] != "d":
                    self.graph.nodes[edge_disjoint_path[i+1]
                                     ]["attr"] = str(number_tree)
                    self.graph[edge_disjoint_path[i]
                               ][edge_disjoint_path[i+1]]["attr"] = str(number_tree)
                self.graph[edge_disjoint_path[i]
                           ][edge_disjoint_path[i+1]]["attr"] = str(number_tree)
            number_tree += 1
        # return self.graph

    def compute_shortest_path(self, failedEdges):
        graph_copy = copy.deepcopy(self.graph)
        graph_copy.remove_edges_from(failedEdges)
        try:
            shortest_path = nx.shortest_path_length(
                graph_copy, self.source, self.destination)
        except nx.NetworkXNoPath:
            shortest_path = -1
        return shortest_path

    def remove_destination_incidents_from_all_structures(self, destination):
        destination_incidents = set()
        for destination_edge in self.graph.edges(destination):
            destination_incidents.add(destination_edge[1])
            self.graph[destination_edge[0]][destination_edge[1]]["attr"] = -1
        return destination_incidents

    def find_destination_incidents(self):
        destination_incidents = set()
        for destination_edge in self.graph.edges(self.destination):
            destination_incidents.add(destination_edge[1])
        return destination_incidents

    def find_the_incidents_of_source(self, source):
        source_incidents = set()
        for source_edge in self.graph.edges(source):
            source_incidents.add(source_edge[1])
        return source_incidents

    def generate_random_failed_edges(self, fraction):
        graph = self.graph
        number_of_failed_edges = int(fraction * graph.number_of_edges())
        failed_edges = random.sample(graph.edges(), number_of_failed_edges)
        return failed_edges

    def disconnect_the_edges_of_the_destination(self):
        destination_incidents = set()
        for destination_edge in self.graph.edges(self.destination):
            destination_incidents.add(destination_edge[1])
            self.graph[destination_edge[0]][destination_edge[1]]["attr"] = "-1"
        # return destination_incidents

    def edges_attrs_of_destination(self):
        list_edges = nx.edge_subgraph(self.graph, [(
            u, v) for u, v, data in self.graph.edges(data=True) if data["attr"] == "-1"])
        return list_edges

    def set_failed_edges(self, failed_edges):
        for failed_edge in failed_edges:
            self.graph[failed_edge[0]][failed_edge[1]]["failed"] = True

    def remove_failed_edges(self, failed_edges):
        self.graph.remove_edges_from(failed_edges)
        print(f"Those edges are removed : {failed_edges}")

    def edps_in_ascending_order(edge_disjoint_paths):
        edge_disjoint_paths.reverse()

    def convert_path_to_edges(edge_disjoint_path):
        path_edges = [(edge_disjoint_path[i], edge_disjoint_path[i+1])
                      for i in range(len(edge_disjoint_path) - 1)]
        return path_edges

    def is_source_still_reachable(self):
        return nx.has_path(self.graph, self.source, self.destination)

    def failed_in_all_edps(edge_disjoint_paths, failed_edges):
        def failed_in_edp(edge_disjoin_path):
            return any(failed_edge in failed_edges for failed_edge in edge_disjoin_path)
        return all(failed_in_edp(edge_disjoint_path) for edge_disjoint_path in edge_disjoint_paths)

# ----------------------------------------------------Tree Algorithms --------------------------------------------

    def oneTree(self, edge_disjoint_paths, reverse=False):

        if reverse:
            edge_disjoint_paths.reverse()
            tree_attribute = len(edge_disjoint_paths)
            path_to_extend = edge_disjoint_paths[0]
        else:
            tree_attribute = len(edge_disjoint_paths)
            path_to_extend = edge_disjoint_paths[len(edge_disjoint_paths) - 1]
        iteration = 0
        # nodes = path_to_extend
        while (iteration < len(path_to_extend)):
            list_of_incident_edges = list(
                self.graph.edges(path_to_extend[iteration]))
            edges_with_attributes_zero = (edge for edge in list_of_incident_edges if
                                          self.graph.get_edge_data(edge[0], edge[1]).get("attr") == "0")
            for edge in edges_with_attributes_zero:
                edge_attr_value = self.graph.nodes[edge[1]]["attr"]
                if edge_attr_value == "0" or edge_attr_value == str(tree_attribute):
                    self.graph.nodes[edge[1]]["attr"] = str(tree_attribute)
                    self.graph[edge[0]][edge[1]]["attr"] = str(tree_attribute)
                    path_to_extend.append(edge[1])
                if edge_attr_value == "d":
                    self.graph[edge[0]][edge[1]]["attr"] = str(tree_attribute)
            iteration = iteration + 1
        Tree = nx.Graph()
        for first_node, second_node, data in self.graph.edges(data=True):
            if data["attr"] == "1":
                Tree.add_edge(first_node, second_node)
        return Tree

    def multipleTree(self, edge_disjoint_paths):
        number_tree = 1
        for i in range(0, len(edge_disjoint_paths) - 1):
            edp_to_extend = edge_disjoint_paths[i]
            iteration = 0
            while(iteration < len(edp_to_extend)):
                list_of_incident_edges = list(
                    self.graph.edges(edp_to_extend[iteration]))
                edges_with_attributes_zero = (edge for edge in list_of_incident_edges if
                                              self.graph.get_edge_data(edge[0], edge[1]).get("attr") == "0")
                for edge in edges_with_attributes_zero:
                    if self.graph.nodes[edge[1]]["attr"] != "s" and self.graph.nodes[edge[1]]["attr"] != "d":
                        self.graph[edge[0]][edge[1]]["attr"] = str(number_tree)
                        self.graph.nodes[edge[1]]["attr"] = str(number_tree)
                        edp_to_extend.append(edge[1])
                    if self.graph.nodes[edge[1]]["attr"] != "d":
                        self.graph.nodes[edge[1]]["attr"] = str(number_tree)
                iteration += 1

    def reconstruct_tree_based_on_attr(self, tree_attribute):
        Tree = nx.Graph()
        for first_node, second_node, data in self.graph.edges(data=True):
            if data["attr"] == tree_attribute:
                Tree.add_edge(first_node, second_node)
        return Tree

    def prune_branches_from_tree(self, tree_attribute, destination_incidents):

        Tree = nx.Graph()

        for u, v, data in self.graph.edges(data=True):
            if data["attr"] == tree_attribute:
                Tree.add_edge(u, v)

        depth_first_search = list(nx.dfs_labeled_edges(Tree, self.source))

        for u, v, direction in depth_first_search:
            if u == v or direction == "nontree":
                depth_first_search.remove((u, v, direction))

        print(depth_first_search)
        print("------------------------")
        nodes_visited = list()
        nodes_visited.append(depth_first_search[0][0])  # source added
        branches_to_keep = set()
        exist_node_to_delete = False

        for i in range(len(depth_first_search)):
            u, v, direction = depth_first_search[i]

            if direction == "forward":
                nodes_visited.append(v)

            if direction == "reverse":
                nodes_visited.remove(v)

            if exist_node_to_delete:
                nx.set_node_attributes(self.graph, {v: "0"}, "attr")
                nx.set_edge_attributes(self.graph, {(u, v): "0"}, "attr")

            if direction == "forward" or v in branches_to_keep:
                exist_node_to_delete = False

            # leaf means that the current direction is "forward and the next is "reverse"
            notOutOfBounds = i < len(depth_first_search) - 1
            if i < len(depth_first_search) - 1:
                first_node, second_node, next_direction = depth_first_search[i+1]
                isLeaf = direction == "forward" and next_direction == "reverse"
                isDestinationIncident = v in destination_incidents

                # if direction == "forward" and next_direction == "reverse" and second_node in destination_incidents:
                if isLeaf and isDestinationIncident:
                    print(f"The {i}-th iteration : {branches_to_keep}")
                    # We add the whole path
                    for node in nodes_visited:
                        branches_to_keep.add(node)
                if (isLeaf and not isDestinationIncident) or (nx.degree(self.graph, v) == 0 and isDestinationIncident):
                    print(
                        f"The {i}-th iteration not incident: {branches_to_keep}")
                    exist_node_to_delete = True
        return self.graph

    def one_tree_routing(self, one_tree, failed_edges, edge_disjoint_paths, number_of_nodes, number_of_nodes_after):
        dfs_from_cutted_edges = set()
        for failed_edge in failed_edges:
            if failed_edge in one_tree.edges():
                one_tree.remove_edge(failed_edge)
                dfs_from_cutted_edges.add(failed_edge)
        if len(edge_disjoint_paths) == 1 and number_of_nodes == number_of_nodes_after:
            if nx.is_connected(self.graph):
                spanning_tree = nx.minimum_spanning_tree(one_tree)
                shortest_path = nx.shortest_path(
                    one_tree, source=self.source, target=self.destination)
                return shortest_path
            else:
                print("No spanning tree can be built.")
        else:

            # Welche Node soll ich nehmen aus der Kante (u,v)
            for edge in dfs_from_cutted_edges:
                visited_nodes = set()
                paths_to_destination = []

                def dfs(node, path_to_destination):
                    if node not in visited_nodes:
                        visited_nodes.add(node)
                        path_to_destination.append(node)
                        if node == self.destination:
                            paths_to_destination.append(path_to_destination[:])
                        else:
                            for neighbor in one_tree.neighbors(node):
                                dfs(neighbor, path_to_destination)
                        path_to_destination.pop()
                    return paths_to_destination

                sorted_paths = sorted(dfs(edge[0], []), key=len, reverse=False)

                if len(sorted_paths) == 0:
                    print(
                        f"Destination cannot be reached from the node {edge[0]}")
                else:
                    paths_without_source = []

                    for path in sorted_paths:
                        if self.source not in path:
                            paths_without_source.append(path)
                            sorted_paths.remove(path)

                    paths_with_source = sorted_paths

                    if len(paths_without_source) > 0:
                        my_path = paths_without_source[0]
                        path_edges = [(my_path[i], my_path[i+1])
                                      for i in range(len(my_path) - 1)]
                        print(
                            f"The destination can be reached from the node {edge[0]} by the path : {my_path}")
                        return my_path, path_edges
                    elif len(paths_with_source) > 0:
                        my_path = paths_with_source[0]
                        path_edges = [(my_path[i], my_path[i+1])
                                      for i in range(len(my_path) - 1)]
                        print(
                            f"The destination can be reached from the node {edge[0]} by the path : {my_path}")
                        return my_path, path_edges
                    else:
                        continue
