#!/usr/bin/env python

"""
big idea: do A*

- heuristic is manhattan distance
- initially map out the graph to find edges
- dynamically build vertices when adding neighbors to visit.  These
  vertices are position + last three directions to get there.  If
  you got where you are by going thrice in the same direction then
  don't map that out

this solution has room for improvement
"""

import fileinput
import math
from dataclasses import dataclass
from enum import Enum
from queue import PriorityQueue
from termcolor import colored

Direction = Enum("Direction", ["NORTH", "EAST", "SOUTH", "WEST"])

opposite_direction = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST
}

def coordinate_direction_key(coords, directions):
    return f"{coords}-{directions}"

class Vertex:
    row: int
    col: int
    g_score: int
    h_score: int
    predecessor_key: str
    preceding_three_directions: list[Direction]

    def __init__(self, row, col, g_score, h_score, predecessor_key, preceding_three_directions):
        self.row = row
        self.col = col
        self.g_score = g_score
        self.h_score = h_score
        self.predecessor_key = predecessor_key
        self.preceding_three_directions = preceding_three_directions

    def __str__(self):
        return f"{self.coords()}: {self.g_score}"

    def key(self):
        return coordinate_direction_key(self.coords(), self.preceding_three_directions)

    def coords(self):
        return f"{self.row},{self.col}"

@dataclass
class Edge:
    weight: int
    direction: Direction
    destination_row: int
    destination_col: int

# discover edges ####

matrix = [[int(x) for x in line.strip()] for line in fileinput.input()]

edges: dict[str, dict[str, Edge]] = {}

for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        label = f"{i},{j}"
        edges[label] = {}

        # an edge from this vertex to a neighbor costs the neighbor's weight
        if i > 0:
            edges[label][f"{i - 1},{j}"] = Edge(int(matrix[i - 1][j]), Direction.NORTH, i - 1, j)
        if j > 0:
            edges[label][f"{i},{j - 1}"] = Edge(int(matrix[i][j - 1]), Direction.WEST, i, j - 1)
        if i < len(matrix) - 1:
            edges[label][f"{i + 1},{j}"] = Edge(int(matrix[i + 1][j]), Direction.SOUTH, i + 1, j)
        if j < len(matrix[0]) - 1:
            edges[label][f"{i},{j + 1}"] = Edge(int(matrix[i][j + 1]), Direction.EAST, i, j + 1)

end_row = len(matrix) - 1
end_col = len(matrix[0]) - 1

# shortest paths from start to end ####

def h_score(row_a, col_a, row_b, col_b) -> int:
    """
    Unweighted Manhattan distance between the given rows and columns
    """
    return abs(row_a - row_b) + abs(col_a - col_b)

start_coords = "0,0"
end_coords = f"{end_row},{end_col}"

# vertices to visit, prioritized by their f-score
vertex_keys_to_visit = PriorityQueue()
start_vertex = Vertex(0, 0, 0, h_score(0, 0, end_row, end_col), None, [])
vertex_keys_to_visit.put((start_vertex.h_score, start_vertex.key()))

vertices: dict[str, Vertex] = { start_vertex.key(): start_vertex }

while not vertex_keys_to_visit.empty():
    _, vertex_key = vertex_keys_to_visit.get()
    vertex = vertices[vertex_key]

    if vertex.coords() == end_coords:
        continue

    # if we got here by going thrice the same direction then we can't go that way now
    forbidden_direction = None
    if len(vertex.preceding_three_directions) == 3:
        if (vertex.preceding_three_directions[0] == vertex.preceding_three_directions[1] and
            vertex.preceding_three_directions[1] == vertex.preceding_three_directions[2]):
            forbidden_direction = vertex.preceding_three_directions[0]

    opposite_of_preceding_direction = None
    if len(vertex.preceding_three_directions) > 0:
        opposite_of_preceding_direction = opposite_direction[vertex.preceding_three_directions[-1]]

    for neighbor_vertex_coords in edges[vertex.coords()].keys():
        edge_to_neighbor = edges[vertex.coords()][neighbor_vertex_coords]
        direction_to_neighbor = edge_to_neighbor.direction
        last_three_directions_to_neighbor = vertex.preceding_three_directions[-2:] + [direction_to_neighbor]

        if direction_to_neighbor == opposite_of_preceding_direction:
            continue

        if direction_to_neighbor == forbidden_direction:
            continue

        neighbor_key = coordinate_direction_key(neighbor_vertex_coords, last_three_directions_to_neighbor)
        neighbor_g_score = vertex.g_score + edges[vertex.coords()][neighbor_vertex_coords].weight

        if neighbor_key not in vertices:
            vertices[neighbor_key] = Vertex(
                edge_to_neighbor.destination_row, 
                edge_to_neighbor.destination_col, 
                math.inf, 
                h_score(edge_to_neighbor.destination_row, edge_to_neighbor.destination_col, end_row, end_col), 
                None, 
                []
            )

        if neighbor_g_score < vertices[neighbor_key].g_score:
            # found a better way to neighbor
            vertices[neighbor_key].g_score = neighbor_g_score
            vertices[neighbor_key].predecessor_key = vertex.key()
            vertices[neighbor_key].preceding_three_directions = last_three_directions_to_neighbor

            if not any(neighbor_vertex_coords == item[1] for item in vertex_keys_to_visit.queue):
                vertex_keys_to_visit.put((neighbor_g_score + vertices[neighbor_key].h_score, neighbor_key))

# find and print min among shortest paths to end ####

# since there are different copies of vertices at the same coordinates
# (from different directions) find the shortest path to the end coords
# among the "clones"

end_vertices = [v for k, v in vertices.items() if end_coords in k]

best_cost = math.inf
best_path = []

for v in end_vertices:
    if v.g_score < best_cost:
        path = ["0,0"]
        best_cost = v.g_score

        while v.predecessor_key != None:
            path.append(v.coords())
            v = vertices[v.predecessor_key]

        best_path = path

for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        color = "white"
        if f"{i},{j}" in best_path:
            color = "yellow"

        print(colored(matrix[i][j], color), end="")
    print()

print(best_cost)
