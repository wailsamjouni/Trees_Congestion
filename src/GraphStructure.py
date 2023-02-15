import networkx as nx
import matplotlib.pyplot as plt
import copy
import random
import colorsys
import logging
import os


class GraphStructure:
    def __init__(self, graph, source, destination):

        self.graph = copy.deepcopy(graph)
        self.source = source
        self.destination = destination

        nx.set_edge_attributes(self.graph, "0", "attr")
        nx.set_node_attributes(self.graph, "0", "attr")

        self.graph.nodes[self.source]["attr"] = "s"
        self.graph.nodes[self.source]["label"] = "s"

        self.graph.nodes[self.destination]["label"] = "d"
        self.graph.nodes[self.destination]["attr"] = "d"

    def _get_logger(self, log_file):

        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)

        handler.stream.seek(0)
        handler.stream.truncate()
        handler.close()

        logger = logging.getLogger(log_file)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        return logger

    def clear_log_file(self):
        self.file_handler.stream.seek(0)
        self.file_handler.stream.truncate()
        self.file_handler.close()

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

        logger = self._get_logger('compute_and_sort_edps.log')

        if self.source not in self.graph:
            logger.error("Source node not in graph")

            return None
        elif self.destination not in self.graph:
            logger.error("Destination node not in graph")

            return None
        else:
            try:
                edge_disjoint_paths = list(
                    nx.edge_disjoint_paths(self.graph, self.source, self.destination))
                edge_disjoint_paths.sort(key=lambda x: len(x), reverse=False)
                logger.info("Edge disjoint paths: {} are computed and sorted".format(
                    edge_disjoint_paths))

                return edge_disjoint_paths
            except nx.NetworkXNoPath:
                logger.error("No path from source node", self.source,
                             "to destination node", self.destination)

                return None

    def is_spanning_tree(self):
        return len(list(
            nx.edge_disjoint_paths(self.graph, self.source, self.destination))) == 1

    def number_the_computed_edps(self, edge_disjoint_paths):

        logger = self._get_logger('number_the_computed_edps.log')

        number_tree = 1
        for edge_disjoint_path in edge_disjoint_paths:
            for i in range(0, len(edge_disjoint_path)-1):
                if self.graph.nodes[edge_disjoint_path[i+1]]["attr"] != "d":
                    self.graph.nodes[edge_disjoint_path[i+1]
                                     ]["attr"] = str(number_tree)
                    self.graph[edge_disjoint_path[i]
                               ][edge_disjoint_path[i+1]]["attr"] = str(number_tree)

                self.graph[edge_disjoint_path[i]
                           ][edge_disjoint_path[i+1]]["attr"] = str(number_tree)
            logger.debug(
                f'The edge disjoint path number {i + 1} has the attribute {number_tree}')

            number_tree += 1

    def compute_shortest_path(self, failedEdges):

        logger = self._get_logger('compute_shortest_path.log')

        graph_copy = copy.deepcopy(self.graph)
        logger.debug(f'A copy of the original graph has been created')

        graph_copy.remove_edges_from(failedEdges)
        logger.debug(
            f'The edges {failedEdges} have been removed from the copied graph')

        try:
            shortest_path = nx.shortest_path_length(
                graph_copy, self.source, self.destination)
            logger.debug(
                f'The shortest path from {self.source} to {self.destination} is {shortest_path}')

        except nx.NetworkXNoPath:
            shortest_path = -1
            logger.exception(
                f'No path from {self.source} to {self.destination}')

        return shortest_path

    def remove_destination_incidents_from_all_structures(self, destination):

        logger = self._get_logger('remove_destination_incidents.log')

        destination_incidents = set()
        for destination_edge in self.graph.edges(destination):
            destination_incidents.add(destination_edge[1])
            self.graph[destination_edge[0]][destination_edge[1]]["attr"] = -1
            logger.info(
                f'The edge ({destination_edge[0]}, {destination_edge[1]}) has now the attribute -1')

        logger.debug(
            'The incidents of the destination are {destination_incidents}')

        return destination_incidents

    def find_destination_incidents(self):

        logger = self._get_logger('find_destination_incidents.log')

        destination_incidents = set()
        logger.info(f'Destination incident list is {destination_incidents}')

        for destination_edge in self.graph.edges(self.destination):
            destination_incidents.add(destination_edge[1])
            logger.info(
                f'The node {destination_edge[1]} has been added to the incident list')
            logger.info(
                f'Destination incident list is {destination_incidents}')
        return destination_incidents

    def find_the_incidents_of_source(self, source):

        logger = self._get_logger('find_the_incidents_of_source.log')

        source_incidents = set()
        logger.info(f'Source incident list is {source_incidents}')
        for source_edge in self.graph.edges(source):
            source_incidents.add(source_edge[1])
            logger.info(
                f'The node {source_edge[1]} has been added to the incident list')

            logger.info(
                f'Source incident list is {source_incidents}')
        return source_incidents

    def generate_random_failed_edges(self, fraction):

        logger = self._get_logger('generate_random_failed_edges.log')

        graph = self.graph
        logger.debug(f'A new graph has been created: {graph}')

        number_of_failed_edges = int(fraction * graph.number_of_edges())
        logger.info(f'The number of failed edges is {number_of_failed_edges}')
        failed_edges = random.sample(graph.edges(), number_of_failed_edges)
        logger.debug(f'Generated edges are : {failed_edges}')
        return failed_edges

    def disconnect_the_edges_of_the_destination(self):

        logger = self._get_logger(
            'disconnect_the_edges_of_the_destination.log')

        destination_incidents = set()
        for destination_edge in self.graph.edges(self.destination):
            destination_incidents.add(destination_edge[1])
            self.graph[destination_edge[0]][destination_edge[1]]["attr"] = "-1"
            logger.info(
                f'The edge ({destination_edge[0]}, {destination_edge[1]}) has now the attribute -1')

        logger.debug(
            'The incidents of the destination are {destination_incidents}')

    def edges_attrs_of_destination(self):
        list_edges = nx.edge_subgraph(self.graph, [(
            u, v) for u, v, data in self.graph.edges(data=True) if data["attr"] == "-1"])
        return list_edges

    def set_failed_edges(self, failed_edges):

        logger = self._get_logger(
            'set_failed_edges.log')

        logger.info(f'The failed edges are {failed_edges}')

        for failed_edge in failed_edges:
            self.graph[failed_edge[0]][failed_edge[1]]["failed"] = True
            logger.debug(
                f'The edge ({failed_edge[0]}, {failed_edge[1]}) has now the value True')

    def remove_failed_edges(self, failed_edges):

        logger = self._get_logger(
            'remove_failed_edges.log')

        self.graph.remove_edges_from(failed_edges)
        logger.debug(
            f'The edges {failed_edges} have been removed from the graph')

    def edps_in_ascending_order(edge_disjoint_paths):
        edge_disjoint_paths.reverse()

    def convert_path_to_edges(edge_disjoint_path):
        path_edges = [(edge_disjoint_path[i], edge_disjoint_path[i+1])
                      for i in range(len(edge_disjoint_path) - 1)]
        return path_edges

    def is_source_still_reachable(self):
        return nx.has_path(self.graph, self.source, self.destination)

    def buildone(self):
        return self.graph
# ----------------------------------------------------Tree Algorithms --------------------------------------------

    def oneTree(self, edge_disjoint_paths, reverse=False):

        logger = self._get_logger("oneTree.log")

        if reverse:
            edge_disjoint_paths.reverse()
            tree_attribute = len(edge_disjoint_paths)
            path_to_extend = edge_disjoint_paths[0]
            logger.info('The edps are in descending order')

        else:
            tree_attribute = len(edge_disjoint_paths)
            path_to_extend = edge_disjoint_paths[len(edge_disjoint_paths) - 1]
            logger.info('The edps are in ascending order')

        iteration = 0
        while (iteration < len(path_to_extend)):
            list_of_incident_edges = list(
                self.graph.edges(path_to_extend[iteration]))

            edges_with_attributes_zero = (edge for edge in list_of_incident_edges if
                                          self.graph.get_edge_data(edge[0], edge[1]).get("attr") == "0")

            for edge in edges_with_attributes_zero:
                node_attr_value = self.graph.nodes[edge[1]]["attr"]
                if node_attr_value == "0" or node_attr_value == str(tree_attribute):

                    self.graph.nodes[edge[1]]["attr"] = str(tree_attribute)
                    logger.info(
                        f'The node {edge[1]} has now the attribute {tree_attribute}')

                    self.graph[edge[0]][edge[1]]["attr"] = str(tree_attribute)
                    logger.debug(
                        f'The edge ({edge[0]}, {edge[1]}) has now the atttirbute {tree_attribute}')

                    path_to_extend.append(edge[1])
                    logger.debug(
                        f'Node {edge[1]} has been added to the path {path_to_extend}')

                if node_attr_value == "d":
                    self.graph[edge[0]][edge[1]]["attr"] = str(tree_attribute)
                    logger.debug(
                        f'the edge ({edge[0]}, {edge[1]}) has now the attribute {tree_attribute}')

            iteration = iteration + 1

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

    def tree_based_edge(self, edge_disjoint_paths, edge_disjoint_path):

        number_tree = edge_disjoint_paths.index(edge_disjoint_path) + 1
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

                # if self.graph.nodes[edge[1]]["attr"] == "s" or self.graph.nodes[edge[1]]["attr"] == "d":
                #     self.graph.nodes[edge[1]]["attr"] = str(number_tree)

            iteration += 1
        return number_tree

    def reconstruct_tree_based_on_attr(self, tree_attribute):

        logger = self._get_logger("reconstruct_tree_based_on_attr.log")

        Tree = nx.Graph()
        logger.debug('Graph created')

        for first_node, second_node, data in self.graph.edges(data=True):
            if data["attr"] == tree_attribute:
                Tree.add_edge(first_node, second_node)
        logger.debug('Tree created : {Tree}')

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

            for u, v, direction in depth_first_search:
                if direction == "nontree":
                    logging.warning("Nontree musst not be here")

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

        # self.clear_log_file()
        logger = self._get_logger('prune_akt.log')

        leaf_nodes = ["s"]

        while len(leaf_nodes) > 0:
            Tree = nx.Graph()

            for u, v, data in self.graph.edges(data=True):
                if int(tree_attribute) > 0 and data["attr"] == str(tree_attribute):
                    Tree.add_edge(u, v)
            logger.debug(f'Tree gebildet: {Tree.edges()}')

            if self.source in list(Tree.nodes):
                logger.debug(f"Source is in graph: {self.source}")

                depth_first_search = list(
                    nx.dfs_labeled_edges(Tree, self.source))

                logger.info(
                    f"Depth first search computed: {depth_first_search}")

                depth_first_search = [
                    nontree for nontree in depth_first_search if nontree[0] == nontree[1] or nontree[2] != 'nontree']

                logger.debug(
                    f"Nontree edges removed: {depth_first_search}")

                check_list = [
                    edge_traversal for edge_traversal in depth_first_search if edge_traversal[2] != "nontree"]

                if any("nontree" in item for item in check_list):
                    logger.error(
                        f"Some nontree edges are present in the graph: {check_list}")

                nodes_visited = set()
                nodes_visited.add(depth_first_search[0][0])
                branches_to_keep = set()
                exist_node_to_delete = False

                for i in range(len(depth_first_search)):
                    u, v, direction = depth_first_search[i]
                    logger.info(
                        f'Das Element ({u},{v},{direction}) wird bearbeitet')

                    if direction == "forward":
                        nodes_visited.add(v)
                        logger.debug(
                            f'Node "{v}" has been visisted')
                        logger.debug(f'List of nodes visited: {nodes_visited}')

                    elif direction == "reverse":
                        nodes_visited.remove(v)
                        logger.debug(
                            f'Node "{v}" has been removed from visited list')
                        logger.debug(f'List of nodes visited: {nodes_visited}')

                    if direction == "forward" or v in branches_to_keep:
                        exist_node_to_delete = False
                        logger.debug(
                            f'Node "{v}" is forward or in branches_to_keep')
                    logger.warning(
                        f'List of branches_to_keep: {branches_to_keep}')

                    if exist_node_to_delete:
                        nx.set_node_attributes(self.graph, values={
                            v: "0"}, name="attr")
                        nx.set_edge_attributes(self.graph, values={
                            (u, v): "0"}, name="attr")

                        logger.debug(f'Edge {(u,v)} has attribut "0"')

                    if (u, v, direction) != depth_first_search[-1]:

                        u_next, v_next, direction_next = depth_first_search[i+1]
                        logger.debug(
                            f'Element ({u},{v},{direction}) wird mit Element ({u_next},{v_next},{direction_next}) verglichen')

                        if direction == "forward" and direction_next == "reverse" and u == u_next and v == v_next and v not in destination_incident:
                            exist_node_to_delete = True

                            logger.debug(
                                f'The current element and the next is "forward" and "reverse" respectively": ({direction}, {direction_next})')

                        elif v in destination_incident or self.graph.degree(v) > 1:
                            # elif v in destination_incident or self.graph.degree(v) > 1:
                            logger.debug(
                                f'"{v}" is in destination_incident or degree > 1')

                            branches_to_keep.update(nodes_visited)
                            logger.debug(
                                f'The list of branches to keep is updated: {branches_to_keep}')

                if not nx.number_connected_components(Tree) == 1:
                    logger.debug(f'The graph is not connected')

                    visited_n = set()
                    visited_e = set()

                    for u, v, label in depth_first_search:
                        if label == "forward":
                            visited_n.add(u)
                            visited_n.add(v)
                            visited_e.add((u, v))
                    unvisited_n = set(Tree.nodes) - visited_n
                    unvisited_e = set(Tree.edges) - visited_e

                    logger.debug(f"Unvisited edges are: {unvisited_e}")

                    for edge in unvisited_e:
                        if self.graph[edge[0]][edge[1]]["attr"] == str(tree_attribute):
                            self.graph[0]["attr"] = "0"
                            self.graph[1]["attr"] = "0"
                            self.graph[edge[0]][edge[1]]["attr"] = "0"

                            logger(
                                f'Attribut 0 assigned to node : "{edge[0]} and node : "{edge[1]}"')

                            logger.debug(
                                f"Attribut 0 assigned to edge : {(u,v)}")

            Tree_new = nx.Graph()

            leaf_nodes = []

            for u, v, data in self.graph.edges(data=True):
                if int(tree_attribute) > 0 and data["attr"] == str(tree_attribute):
                    Tree_new.add_edge(u, v)

            logger.debug(
                f'Tree built to check if still exists another nodes and edges to prune: {Tree_new.edges()}')

            for u, v, data in Tree_new.edges(data=True):
                if Tree_new.degree(u) == 1 and u not in destination_incident and u != self.source:
                    leaf_nodes.append(u)

                elif Tree_new.degree(v) == 1 and v not in destination_incident and v != self.source:
                    leaf_nodes.append(v)
            logger.debug(f'Leaf nodes: {leaf_nodes}')

    def remove_unconnected_nodes(self):

        logger = self._get_logger('remove_unconnected_nodes.log')

        connected_components = list(nx.connected_components(self.graph))
        for component in connected_components:
            if len(component) == 1:
                node = list(component)[0]
                self.graph.remove_node(node)
                logger.debug(f'Node "{node}" has been removed from graph')

        logger.debug(
            f'Graph after removing unconnected nodes: {self.graph.edges()}')

    # def contains_failed_edge(self, edge_disjoint_path, failed_edges):

    #     logger = self._get_logger('contains_failed_edge.log')

    #     edp_edges = [(edge_disjoint_path[i], edge_disjoint_path[i+1])
    #                  for i in range(len(edge_disjoint_path) - 1)]
    #     logger.debug(f'Path converted to edges: {edp_edges}')

    #     for edge in edp_edges:
    #         if edge in failed_edges:
    #             logger.info(
    #                 f'This edge disjoint path contains an edge "{edge}" that has been found in failed edges')

    #             return True
    #     return False

    def contains_failed_edges(self, edge_disjoint_path, failed_edges):

        logger = self._get_logger('contains_failed_edge.log')

        edp_edges = [(edge_disjoint_path[i], edge_disjoint_path[i+1])
                     for i in range(len(edge_disjoint_path) - 1)]
        logger.debug(f'Path converted to edges: {edp_edges}')

        failed_path = [edge for edge in edp_edges if edge in failed_edges]
        if failed_path:
            logging.info(
                'This edge disjoint path contains edges that has been found in failed edges: %s', failed_path)
            return True
        else:
            logging.info('Der Pfad enthält keine fehlerhaften Kanten.')
            return False

    def has_no_failed_edge(self, edge_disjoint_path, failed_edges):
        return not self.contains_failed_edge(edge_disjoint_path, failed_edges)

    def find_path(self, tree, node, destination_incidents, path):

        logger = self._get_logger('find_path.log')

        if self.source not in self.graph:

            print("The source node not found in the graph")
            logger.error(f'Source node "{self.source}" not found in the graph')
            return None

        path += [node]
        if node in destination_incidents:
            logger.debug(
                f'Path found between source "{self.source}" node and an incident of the destination node "{self.destination}": {path}')
            return path

        for neighbor in tree[node]:

            if neighbor not in path:
                new_path = self.find_path(
                    tree, neighbor, destination_incidents, path)

                if new_path:
                    logger.info(
                        f'Path found between source "{self.source}" node and an incident of the destination node "{self.destination}": {path}')

                    return new_path
        logger.error(
            f'No path found between source "{self.source}" node and an incident of the destination node "{self.destination}"')

        return None

    # def path_has_failure(self, path, failed_edges):

    #     logger = self._get_logger('path_has_failure.log')

    #     path_edges = [(path[i], path[i+1])
    #                   for i in range(len(path) - 1)]

    #     for (u, v) in path_edges:
    #         if (u, v) in failed_edges or (v, u) in failed_edges:
    #             logging.info(
    #         'This edge disjoint path contains edges that has been found in failed edges: %s', failed_path)
    #             return True
    #     return False

    def path_has_failure(self, edge_disjoint_path, failed_edges):

        logger = self._get_logger('path_has_failure.log')

        path_edges = [(edge_disjoint_path[i], edge_disjoint_path[i+1])
                      for i in range(len(edge_disjoint_path) - 1)]

        logger.debug(f'Path converted to edges: {path_edges}')

        def is_edge_failed(edge):
            return edge in failed_edges or (edge[1], edge[0]) in failed_edges

        failed_path = [
            edge for edge in path_edges if is_edge_failed(edge)]
        if failed_path:
            logging.error(
                'This edge disjoint path contains edges that has been found in failed edges: %s', failed_path)
            return True
        else:
            logging.info(
                'This edge disjoint path does not suffer any failure.')
            return False

    def one_tree_routing(self, edge_disjoint_paths, one_tree, destination_incidents, failed_edges):

        logger = self._get_logger('one_tree_routing.log')

        tree_attr = 1
        destination_reached = False
        path_to_d = []

        for edp in edge_disjoint_paths:

            logger.info(f'Edge disjoint path: {edp} will be checked')

            has_failure = self.path_has_failure(edp, failed_edges)
            if not has_failure:

                destination_reached = True
                path_to_d = edp
                logger.info(
                    f'Destination node "{self.destination}" can be reached through this path {path_to_d}')
                break

        if not destination_reached:

            path = self.find_path(one_tree, self.source,
                                  destination_incidents, [])

            if path:
                logger.info(
                    f'Destination node "{self.destination}" can be reached through this path {path} using depth first search')

            else:
                logger.error(
                    'Destination node "{self.destination}" can not be reached')

    def multiple_tree_routing(self, edge_disjoint_paths, destination_incidents, failed_edges, trees):

        logger = self._get_logger('multiple_tree_routing.log')

        sorted_edps = sorted(edge_disjoint_paths, key=len)
        destination_reached = False
        path_to_d = []

        for edp in sorted_edps:

            logger.info(f'Edge disjoint path: {edp} will be checked')

            if self.has_no_failed_edge(edp, failed_edges):
                destination_reached = True
                path_to_d = edp
                logger.info(
                    f'Destination node "{self.destination}" can be reached through this path {path_to_d}')
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
                    logger.info(
                        f'Destination node "{self.destination}" can be reached through this path {path} using depth first search')
                    break
                else:
                    if tree_attr == len(edge_disjoint_paths):
                        logger.error(
                            'Destination node "{self.destination}" can not be reached')
                    tree_attr += 1
        # else:
        #     logger.info(
        #         f'Destination node "{self.destination}" can be reached through this path {path_to_d}')

    def build(self, fraction, version=None):

        logger = self._get_logger('build.log')

        edge_disjoint_paths = self.compute_and_sort_edps()
        logger.info(
            f'EDPS between {self.source} and {self.destination} are :{edge_disjoint_paths}')

        edge_attrs = nx.get_edge_attributes(self.graph, "attr")
        logger.info(f'Attributes before extending EDP : {edge_attrs}')

        destination_incidents = self.find_destination_incidents()
        logger.info(f'Destination neighbors are : {destination_incidents}')

        self.number_the_computed_edps(edge_disjoint_paths)

        edge_attrs_after = nx.get_edge_attributes(self.graph, "attr")
        logger.info(f'Attributes after numbering the EDPs : {edge_attrs}')

        # failed_edges_random = self.generate_random_failed_edges(fraction)
        failed_edges_random = [(2, 7)]

        shortest_path_after_removing_failededges = self.compute_shortest_path(
            failed_edges_random)
        logger.info(
            f'Shortest path after removing failed edges: {shortest_path_after_removing_failededges}')

        # One tree building
        if version == "onetree":

            self.oneTree(edge_disjoint_paths, reverse=True)
            logger.debug(f'One tree choosed')

            edps = list(nx.edge_disjoint_paths(
                self.graph, self.source, self.destination))
            logger.info(
                f'Updated edps between {self.source} and {self.destination} are : {edps}')

            edge_attrs_after = nx.get_edge_attributes(self.graph, "attr")
            logger.info(
                f'Attributes after building one tree : {edge_attrs_after}')

            self.disconnect_the_edges_of_the_destination()
            self.prune_akt(destination_incidents, 1)
            self.remove_failed_edges(failed_edges_random)
            self.remove_unconnected_nodes()

            Tree = nx.Graph()
            for first_node, second_node, data in self.graph.edges(data=True):
                if data["attr"] == "1":
                    Tree.add_edge(first_node, second_node)

            edge_attrs_pruned = nx.get_edge_attributes(self.graph, "attr")
            logger.debug(
                f'Attributes after pruning the tree : {edge_attrs_pruned}')

            self.one_tree_routing(edps, Tree,
                                  destination_incidents, failed_edges_random)
            logger.info('Routing has just begun')
            logger.debug(f'Tree with attr 1 is : {Tree.edges}')

            # pos = nx.circular_layout(self.graph)
            # nx.draw(self.graph, with_labels=True, pos=pos)
            # plt.show()
            # pos = nx.circular_layout(Tree)
            # nx.draw(Tree, with_labels=True, pos=pos)
            # plt.show()

        else:
            logger.debug(f'Multiple tree choosed')
            for edge_disjoint_path in edge_disjoint_paths:

                tree_attr = self.tree_based_edge(edge_disjoint_paths,
                                                 edge_disjoint_path)
                self.disconnect_the_edges_of_the_destination()
                self.prune_akt(destination_incidents, tree_attr)
