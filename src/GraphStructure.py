import networkx as nx
import matplotlib.pyplot as plt
import copy
import random
import colorsys


class GraphStructure:
    def __init__(self, graph, source, destination):
        self.graph = copy.deepcopy(graph)
        self.source = source
        self.destination = destination
        self.edps = self.compute_and_sort_edps()

        nx.set_edge_attributes(self.graph, "0", "attr")
        nx.set_node_attributes(self.graph, "0", "attr")
        self.graph.nodes[self.source]["attr"] = "s"
        self.graph.nodes[self.source]["label"] = "s"
        self.graph.nodes[self.destination]["label"] = "d"
        self.graph.nodes[self.destination]["attr"] = "d"

    # def give_attrs_to_graph(self):
    #     nx.set_edge_attributes(self.graph, "0", "attr")
    #     nx.set_node_attributes(self.graph, "0", "attr")
    #     self.graph.nodes[self.source]["attr"] = "s"
    #     self.graph.nodes[self.source]["label"] = "s"
    #     self.graph.nodes[self.destination]["label"] = "d"
    #     self.graph.nodes[self.destination]["attr"] = "d"
        # return self.graph

    def generate_colors(self, number):
        return [colorsys.hsv_to_rgb(x/number, 1, 1) for x in range(number)]

    def colorize_paths(self, paths):
        colors = [colorsys.hsv_to_rgb(x/len(paths), 1, 1)
                  for x in range(len(paths))]
        pos = nx.spring_layout(self.graph)

        for path, color in zip(paths, colors):
            nx.draw_networkx_edges(self.graph, pos,
                                   edgelist=[(path[i], path[i+1])
                                             for i in range(len(path) - 1)], edge_color=color, width=2)
        not_colored_edges = set(self.graph.edges()) - set(sum(paths, []))
        nx.draw_networkx_edges(
            self.graph, pos, edgelist=not_colored_edges, edge_color='gray', width=1)
        nx.draw_networkx_nodes(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos)
        plt.show()

    def colorize_one_tree(self, tree):
        for edge in tree:
            self.graph[edge[0]][edge[1]]['color'] = 'blue'
        nx.draw(self.graph, with_labels=True)

    def draw(self):
        pos = nx.circular_layout(self.graph)
        color_mapping = [self.graph.nodes[node].get(
            "color", "red") for node in self.graph.nodes]
        nx.draw(self.graph, with_labels=True,
                pos=pos, node_color=color_mapping)
        plt.show()

    def compute_and_sort_edps(self):

        if self.source not in self.graph:
            print("Source node not in graph")
            return None
        elif self.destination not in self.graph:
            print("Destination node not in graph")
            return None
        else:
            try:
                edge_disjoint_paths = list(
                    nx.edge_disjoint_paths(self.graph, self.source, self.destination))
                edge_disjoint_paths.sort(key=lambda x: len(x), reverse=False)
                return edge_disjoint_paths
            except nx.NetworkXNoPath:
                print("No path from source node", self.source,
                      "to destination node", self.destination)
                return None

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

    def failed_in_all_edps(self, edge_disjoint_paths, failed_edges):
        # def failed_in_edp(edge_disjoint_path):
        #     return any(failed_edge in failed_edges for failed_edge in edge_disjoint_path)
        # return all(failed_in_edp(edge_disjoint_path) for edge_disjoint_path in edge_disjoint_paths)
        for edge_disjoint_path in edge_disjoint_paths:
            contains_failed_edge = False
            for failed_edge in failed_edges:
                if failed_edge in failed_edges:
                    if failed_edge in zip(edge_disjoint_path, edge_disjoint_path[1:]):
                        contains_failed_edge = True
                        break
        return contains_failed_edge

    def buildone(self):
        return self.graph
# ----------------------------------------------------Tree Algorithms --------------------------------------------

    def oneTree(self, reverse=False):

        if reverse:
            self.edps.reverse()
            tree_attribute = len(self.edps)
            path_to_extend = self.edps[0]
        else:
            tree_attribute = len(self.edps)
            path_to_extend = self.edps[len(self.edps) - 1]
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
            if data["attr"] == str(len(self.edps)):
                Tree.add_edge(first_node, second_node)
        return Tree

    def multipleTree(self):
        number_tree = 1
        for i in range(0, len(self.edps) - 1):
            edp_to_extend = self.edps[i]
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

    def tree_based_edge(self, edge_disjoint_path):

        number_tree = self.edps.index(edge_disjoint_path) + 1
        edp_to_extend = edge_disjoint_path
        iteration = 0
        while(iteration < len(edp_to_extend)):

            list_of_incident_edges = list(
                self.graph.edges(edp_to_extend[iteration]))

            # edges_with_attributes_zero = (edge for edge in list_of_incident_edges if
            #                               self.graph.get_edge_data(edge[0], edge[1]).get("attr") == "0")

            edges_with_zero_one = [edge for edge in list_of_incident_edges if self.graph.get_edge_data(
                edge[0], edge[1]).get("attr") in [0, -1]]

            for edge in edges_with_zero_one:

                if self.graph.nodes[edge[1]]["attr"] != "s" and self.graph.nodes[edge[1]]["attr"] != "d":

                    self.graph[edge[0]][edge[1]]["attr"] = str(number_tree)
                    self.graph.nodes[edge[1]]["attr"] = str(number_tree)
                    edp_to_extend.append(edge[1])

                if self.graph.nodes[edge[1]]["attr"] == "s" or self.graph.nodes[edge[1]]["attr"] == "d":
                    self.graph.nodes[edge[1]]["attr"] = str(number_tree)

            iteration += 1
        return number_tree

    def reconstruct_tree_based_on_attr(self, tree_attribute):
        Tree = nx.Graph()
        for first_node, second_node, data in self.graph.edges(data=True):
            if data["attr"] == tree_attribute:
                Tree.add_edge(first_node, second_node)
        return Tree

    def after_pruning(self, tree):
        for edge in tree.edges:
            if edge in self.graph.edges:
                self.graph.remove_edge(*edge)

    def prune(self, destination_incident, tree_attribute):

        Tree = nx.Graph()

        for u, v, data in self.graph.edges(data=True):
            if int(tree_attribute) > 0 and data["attr"] == str(tree_attribute):
                Tree.add_edge(u, v)
        print(f"Tree gebildet: {Tree.edges()}")

        if self.source in list(Tree.nodes):
            depth_first_search = list(
                nx.dfs_labeled_edges(Tree, self.source))

            for u, v, direction in depth_first_search:
                if direction == "nontree" or u == v:
                    depth_first_search.remove((u, v, direction))
            print(depth_first_search)

            nodes_visited = set()
            nodes_visited.add(depth_first_search[0][0])
            branches_to_keep = set()
            exist_node_to_delete = False

            for i in range(len(depth_first_search)):
                u, v, direction = depth_first_search[i]
                print(nodes_visited)

                if direction == "forward":
                    nodes_visited.add(v)

                elif direction == "reverse":
                    nodes_visited.remove(v)

                if direction == "forward" or v in branches_to_keep:
                    exist_node_to_delete = False

                if exist_node_to_delete:
                    nx.set_node_attributes(self.graph, values={
                        v: "0"}, name="attr")
                    nx.set_edge_attributes(self.graph, values={
                        (u, v): "0"}, name="attr")

                    print(f"Edge ({u,v}) mit 0")

                if (u, v, direction) != depth_first_search[-1]:
                    u_next, v_next, direction_next = depth_first_search[i+1]
                    if direction == "forward" and direction_next == "reverse" and v not in destination_incident:
                        exist_node_to_delete = True
                    elif v in destination_incident:
                        branches_to_keep.update(nodes_visited)

            if not nx.number_connected_components(Tree) == 1:

                visited_n = set()
                visited_e = set()

                for u, v, label in depth_first_search:
                    if label == "forward":
                        visited_n.add(u)
                        visited_n.add(v)
                        visited_e.add((u, v))
                        print(f"Edge added : {(u,v)}")
                unvisited_n = set(Tree.nodes) - visited_n
                unvisited_e = set(Tree.edges) - visited_e
                print(f"Unvisited nodes are: {unvisited_n}")
                print(f"Unvisited edges are: {unvisited_e}")

                for edge in unvisited_e:
                    if self.graph[edge[0]][edge[1]]["attr"] == str(tree_attribute):
                        self.graph[edge[0]][edge[1]]["attr"] = "0"

    def prune_akt(self, destination_incident, tree_attribute):

        leaf_nodes = ["s"]

        while len(leaf_nodes) > 0:
            # print("Iam here")
            Tree = nx.Graph()

            for u, v, data in self.graph.edges(data=True):
                if int(tree_attribute) > 0 and data["attr"] == str(tree_attribute):
                    Tree.add_edge(u, v)
            print(f"Tree gebildet: {Tree.edges()}")

            if self.source in list(Tree.nodes):
                depth_first_search = list(
                    nx.dfs_labeled_edges(Tree, self.source))

                for u, v, direction in depth_first_search:
                    if direction == "nontree" or u == v:
                        depth_first_search.remove((u, v, direction))
                print(depth_first_search)

                nodes_visited = set()
                nodes_visited.add(depth_first_search[0][0])
                branches_to_keep = set()
                exist_node_to_delete = False

                for i in range(len(depth_first_search)):
                    u, v, direction = depth_first_search[i]
                    # print(nodes_visited)

                    if direction == "forward":
                        nodes_visited.add(v)

                    elif direction == "reverse":
                        nodes_visited.remove(v)

                    if direction == "forward" or v in branches_to_keep:
                        exist_node_to_delete = False

                    if exist_node_to_delete:
                        nx.set_node_attributes(self.graph, values={
                            v: "0"}, name="attr")
                        nx.set_edge_attributes(self.graph, values={
                            (u, v): "0"}, name="attr")

                        print(f"Edge ({u,v}) mit 0")

                    if (u, v, direction) != depth_first_search[-1]:
                        u_next, v_next, direction_next = depth_first_search[i+1]
                        if direction == "forward" and direction_next == "reverse" and v not in destination_incident:
                            exist_node_to_delete = True
                        elif v in destination_incident:
                            branches_to_keep.update(nodes_visited)

                if not nx.number_connected_components(Tree) == 1:

                    visited_n = set()
                    visited_e = set()

                    for u, v, label in depth_first_search:
                        if label == "forward":
                            visited_n.add(u)
                            visited_n.add(v)
                            visited_e.add((u, v))
                            # print(f"Edge added : {(u,v)}")
                    unvisited_n = set(Tree.nodes) - visited_n
                    unvisited_e = set(Tree.edges) - visited_e
                    # print(f"Unvisited nodes are: {unvisited_n}")
                    # print(f"Unvisited edges are: {unvisited_e}")

                    for edge in unvisited_e:
                        if self.graph[edge[0]][edge[1]]["attr"] == str(tree_attribute):
                            self.graph[edge[0]][edge[1]]["attr"] = "0"

            Tree_new = nx.Graph()

            leaf_nodes = []

            for u, v, data in self.graph.edges(data=True):
                if int(tree_attribute) > 0 and data["attr"] == str(tree_attribute):
                    if self.graph.degree(u) == 1 and u not in destination_incident and u != self.source:
                        leaf_nodes.append(u)

                    elif self.graph.degree(v) == 1 and v not in destination_incident and v != self.source:
                        leaf_nodes.append(v)

                    Tree_new.add_edge(u, v)

    def remove_unconnected_nodes(self):

        connected_components = list(nx.connected_components(self.graph))
        for component in connected_components:
            if len(component) == 1:
                node = list(component)[0]
                self.graph.remove_node(node)

    def contains_failed_edge(self, edge_disjoint_path, failed_edges):

        edp_edges = [(edge_disjoint_path[i], edge_disjoint_path[i+1])
                     for i in range(len(edge_disjoint_path) - 1)]
        for edge in edp_edges:
            if edge in failed_edges:
                return True
        return False

    def has_no_failed_edge(self, edge_disjoint_path, failed_edges):
        return not self.contains_failed_edge(edge_disjoint_path, failed_edges)

    def find_path(self, tree, node, destination_incidents, path):

        path += [node]
        if node in destination_incidents:
            return path

        for neighbor in tree[node]:

            if neighbor not in path:
                new_path = self.find_path(
                    tree, neighbor, destination_incidents, path)

                if new_path:
                    return new_path
        return None

    def one_tree_routing(self, destination_incidents, failed_edges):

        edge_disjoint_paths = self.compute_and_sort_edps()
        # sorted_edps = sorted(edge_disjoint_paths, key=len)
        print(
            f"hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh {edge_disjoint_paths}")
        tree_attr = 1
        destination_reached = False
        path_to_d = []

        for edp in edge_disjoint_paths:

            if self.has_no_failed_edge(edp, failed_edges):
                destination_reached = True
                path_to_d = edp
                break

        if not destination_reached:

            Tree = nx.Graph()
            for u, v, data in self.graph.edges(data=True):
                if int(tree_attr) > 0 and data["attr"] == str(tree_attr):
                    Tree.add_edge(u, v)

            path = self.find_path(Tree, self.source, destination_incidents, [])
            print(f"path is : {path}")

            if path:
                print(
                    f"Der Destination kann über diesen Pfad erreicht werden ggg : {path}")
            else:
                print("Der Destination kann nicht erreicht werden ")
        else:
            print(
                f"Der Destination kann über diesen Pfad erreicht werden : {path_to_d}")

    def multiple_tree_routing(self, edge_disjoint_paths, destination_incidents, failed_edges, trees):

        sorted_edps = sorted(edge_disjoint_paths, key=len)
        tree_attr = len(edge_disjoint_paths)
        destination_reached = False
        path_to_d = []

        for edp in sorted_edps:

            if self.has_no_failed_edge(edp, failed_edges):
                destination_reached = True
                path_to_d = edp
                break

        if not destination_reached:

            tree_attr = 1

            for tree in trees:

                Tree = nx.Graph()
                for u, v, data in self.graph.edges(data=True):
                    if int(tree_attr) > 0 and data["attr"] == str(tree_attr):
                        Tree.add_edge(u, v)

                path = self.find_path(Tree, destination_incidents)

                if path:
                    print(
                        f"Der Destination kann über diesen Pfad erreicht werden : {path}")
                    break
                else:
                    if tree_attr == len(edge_disjoint_paths):
                        return "Der Destination kann nicht erreicht werden"
                    tree_attr += 1
        else:
            print(
                f"Der Destination kann über diesen Pfad erreicht werden : {path_to_d}")

    def build(self, fraction, version=None):

        edge_disjoint_paths = self.compute_and_sort_edps()
        print(
            f"EDPS between {self.source} and {self.destination}: {edge_disjoint_paths}")
        print("------------------------------------------------------------------")

        edge_attrs = nx.get_edge_attributes(self.graph, "attr")
        print(f"Attributes before extending EDP : {edge_attrs}")

        destination_incidents = self.find_destination_incidents()
        print(f"Destination neighbors : {destination_incidents}")

        self.number_the_computed_edps(edge_disjoint_paths)
        edge_attrs_after = nx.get_edge_attributes(self.graph, "attr")
        print(f"attributes after numbering the EDPs : {edge_attrs_after}")

        # failed_edges_random = self.generate_random_failed_edges(fraction)
        # failed_edges_random = [(2, 7), (3, 6)]
        failed_edges_random = [(2, 7), (3, 6), (1, 3)]
        shortest_path_after_removing_failededges = self.compute_shortest_path(
            failed_edges_random)

        # Convert paths to edges
        edps_edge_list = []
        for edge_disjoint_path in edge_disjoint_paths:
            path_edges = [(edge_disjoint_path[i], edge_disjoint_path[i+1])
                          for i in range(len(edge_disjoint_path) - 1)]
            edps_edge_list.append(path_edges)

        # One tree building
        if version == "onetree":
            one_tree = self.oneTree(reverse=True)

            edge_attrs_after = nx.get_edge_attributes(self.graph, "attr")
            print(f"attributes after building one tree : {edge_attrs_after}")

            self.disconnect_the_edges_of_the_destination()

            self.prune_akt(destination_incidents, 1)
            self.remove_failed_edges(failed_edges_random)
            self.remove_unconnected_nodes()

            edge_attrs_pruned = nx.get_edge_attributes(self.graph, "attr")
            print("------------------------------------------------------------------")
            print(f"attributes after pruning the tree : {edge_attrs_pruned}")

            # self.one_tree_routing(edge_disjoint_paths,
            #                       failed_edges_random, destination_incidents)

            Tree = nx.Graph()
            for first_node, second_node, data in self.graph.edges(data=True):
                if data["attr"] == "1":
                    Tree.add_edge(first_node, second_node)
            print(f"Tree with attr 1 is : {Tree.edges}")

            pos = nx.circular_layout(self.graph)
            nx.draw(self.graph, with_labels=True, pos=pos)
            plt.show()

        else:
            for edge_disjoint_path in edge_disjoint_paths:

                tree_attr = self.tree_based_edge(
                    edge_disjoint_path, edge_disjoint_paths)
                self.disconnect_the_edges_of_the_destination()
                self.prune_akt(destination_incidents, tree_attr)
