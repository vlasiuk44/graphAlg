import random

class AntColony:
    def __init__(self, graph) -> None:
        self.graph = graph

    def find_best_path(self, generations):
        best_path = None

        for node in self.graph.nodes:
            current_path = self._find_path(node.name, generations)
            if best_path is None or current_path[0] < best_path[0]:
                best_path = current_path

        return best_path

    def _find_path(self, start, generations):
        pheromone_levels, paths = self._initialize_data()

        for _ in range(generations):
            visited, total_distance, skip = self._explore_path([start])
            if not skip:
                pheromone_levels, paths = self._update_pheromones(visited, pheromone_levels, paths, total_distance)

        return pheromone_levels[start], paths[start]

    def _initialize_data(self):
        pheromone_levels = {node.name: float('inf') for node in self.graph.nodes}
        paths = {node.name: [] for node in self.graph.nodes}
        return pheromone_levels, paths

    def _explore_path(self, visited):
        total_distance = 0
        skip = False

        while len(visited) < len(self.graph.nodes):
            current_node = self.graph.find_node_by_name(visited[-1])
            possibilities, visited_neighbor_count, attraction = self._get_node_data(current_node, visited)

            if visited_neighbor_count == len(current_node.neighbors):
                skip = True
                break

            visited, total_distance = self._choose_next_node(possibilities, attraction, visited, total_distance)

        return visited, total_distance, skip

    def _get_node_data(self, node, visited):
        possibilities = []
        visited_neighbor_count = 0
        attraction = 0

        for neighbor, weight, t, n in node.neighbors:
            if neighbor in visited:
                visited_neighbor_count += 1
                continue
            tn = t * n
            attraction += tn
            possibilities.append([neighbor, tn, weight])

        return possibilities, visited_neighbor_count, attraction

    def _choose_next_node(self, possibilities, attraction, visited, total_distance):
        for i in range(len(possibilities)):
            possibilities[i][1] /= attraction
            if i > 0:
                possibilities[i][1] += possibilities[i-1][1]

        random_value = random.random()
        for node, tn, weight in possibilities:
            if random_value < tn:
                visited.append(node)
                total_distance += weight
                break

        return visited, total_distance

    def _update_pheromones(self, visited, pheromone_levels, paths, total_distance):
        for i in range(len(visited) - 1):
            current_node = self.graph.find_node_by_name(visited[i])
            for neighbor, _, t, _ in current_node.neighbors:
                if neighbor == visited[i + 1]:
                    t += 1 / total_distance

        if pheromone_levels[visited[0]] > total_distance:
            pheromone_levels[visited[0]] = total_distance
            paths[visited[0]] = visited

        return pheromone_levels, paths


class Node:
    def __init__(self, name, neighbors) -> None:
        self.name = name
        self.neighbors = neighbors


class Graph:
    def __init__(self, graph_object) -> None:
        self.nodes = [Node(name, [(neighbor[0], neighbor[1], 1, 1 / neighbor[1]) for neighbor in neighbors])
                      for name, neighbors in graph_object.items()]

    def find_node_by_name(self, name):
        return next((node for node in self.nodes if node.name == name), None)


mocked_graph = Graph({
    'a': [('b', 3), ('f', 1)],
    'b': [('a', 3), ('c', 8), ('g', 3)],
    'c': [('b', 3), ('d', 1), ('g', 1)],
    'd': [('c', 8), ('f', 1)],
    'f': [('d', 3), ('a', 3)],
    'g': [('a', 3), ('b', 3), ('c', 3), ('d', 5), ('f', 4)]
})

ant_colony = AntColony(mocked_graph)
distance, path = ant_colony.find_best_path(10000)

print(distance, path)
