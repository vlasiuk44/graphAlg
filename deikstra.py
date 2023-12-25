class Node:
    def __init__(self, name, neighbors) -> None:
        self.name = name
        self.neighbors = neighbors


class Graph:
    def __init__(self, graph_object) -> None:
        self.nodes = [Node(name, neighbors) for name, neighbors in graph_object.items()]

    def find_node_by_name(self, name):
        return next((node for node in self.nodes if node.name == name), None)


class Dijkstra:
    def __init__(self, graph) -> None:
        self.graph = graph

    def search(self, start, end):
        distances = {node.name: float('inf') for node in self.graph.nodes}
        paths = {node.name: None for node in self.graph.nodes}
        visited = {node.name: False for node in self.graph.nodes}

        distances[start] = 0

        for _ in range(len(self.graph.nodes)):
            min_node = min((node for node in self.graph.nodes if not visited[node.name]),
                           key=lambda n: distances[n.name], default=None)

            if min_node is None:
                break

            visited[min_node.name] = True

            for neighbor, weight in min_node.neighbors:
                distance = distances[min_node.name] + weight
                if distances[neighbor] > distance:
                    distances[neighbor] = distance
                    paths[neighbor] = min_node.name

        return distances[end], self.create_path(start, end, paths)

    @staticmethod
    def create_path(start, end, paths):
        path = [end]
        current_node = end

        while current_node != start:
            current_node = paths[current_node]
            path.insert(0, current_node)

        return path


testGraph = Graph({
    '1': [('2', 10), ('3', 6), ('4', 8)],
    '2': [('4', 5), ('5', 13), ('7', 11)],
    '3': [('5', 3)],
    '4': [('3', 2), ('5', 5), ('7', 12), ('6', 7)],
    '5': [('6', 9), ('9', 12)],
    '6': [('8', 8), ('9', 10)],
    '7': [('6', 4), ('8', 6), ('9', 16)],
    '8': [('9', 15)],
    '9': [],
})

dijkstra = Dijkstra(testGraph)
distance, path = dijkstra.search('1', '9')
print(distance, path)
assert distance == 21
assert path == ['1', '3', '5', '9']
