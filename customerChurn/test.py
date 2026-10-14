
graph = {
    'A': {'B': 4, 'C': 2},
    'B': {'D': 5},
    'C': {'D': 8, 'E': 10},
    'D': {'F': 6},
    'E': {'F': 3},
    'F': {}
}

import heapq

def uniform_cost_search(graph, start, goal):
    queue = [(0, [start])]
    visited = set()

    while queue:
        cost, path = heapq.heappop(queue)
        node = path[-1]

        if node == goal:
            return path, cost

        if node not in visited:
            visited.add(node)
            for neighbor, edge_cost in graph[node].items():
                new_cost = cost + edge_cost
                new_path = path + [neighbor]
                heapq.heappush(queue, (new_cost, new_path))

    return None, float('inf')

# Run UCS from A to F
path, total_cost = uniform_cost_search(graph, 'A', 'F')
print("Path found:", path)
print("Total cost:", total_cost)
