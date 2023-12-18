#!/usr/bin/env python

import fileinput
import math
from dataclasses import dataclass

@dataclass
class Vertex:
    weight_into: int
    neighbor_keys: list[str]

# read input into a matrix ####

matrix = [[int(x) for x in line.strip()] for line in fileinput.input()]

# construct graph ####

# graph is a dict of Vertex objects
# keys of graph are vertex keys (redundant)
# values are vertices
graph: dict[str, Vertex] = {}

for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        key = f"{i},{j}"

        neighbors = []
        if i > 0:
            neighbors.append(f"{i-1},{j}") # north
        if j > 0:
            neighbors.append(f"{i},{j-1}") # west
        if i < len(matrix) - 1:
            neighbors.append(f"{i+1},{j}") # south
        if j < len(matrix[0]) - 1:
            neighbors.append(f"{i},{j+1}") # east

        graph[key] = Vertex(
            weight_into=int(matrix[i][j]),
            neighbor_keys=neighbors
        )

# find shortest path from start vertex to all others ####

start_vertex_key = "0,0"
end_vertex_key = f"{len(matrix) - 1},{len(matrix[0]) - 1}"

# basic Dijkstra
# track the distance from the start vertex in both places, it's nice to have on the 
# unvisited list because you can search for the min among unvisited in one place,
# and the full vertex distance from start doesn't get deleted from.
# but you do have to do extra bookkeeping
unvisited_vertex_distance_from_start_vertex = { key: math.inf for key in graph.keys() }
vertex_distance_from_start_vertex = { key: math.inf for key in graph.keys() }
vertex_predecessor_key_from_start_vertex = { key: None for key in graph.keys() }

unvisited_vertex_distance_from_start_vertex[start_vertex_key] = 0
vertex_distance_from_start_vertex[start_vertex_key] = 0

while len(unvisited_vertex_distance_from_start_vertex) > 0:
    current_vertex_key = min(unvisited_vertex_distance_from_start_vertex, key=unvisited_vertex_distance_from_start_vertex.get)
    current_distance_from_start = vertex_distance_from_start_vertex[current_vertex_key]

    print(f"visiting {current_vertex_key}")
    del unvisited_vertex_distance_from_start_vertex[current_vertex_key]

    # check if distances/paths of neighbors should be updated
    for neighbor_key in graph[current_vertex_key].neighbor_keys:
        if not neighbor_key in unvisited_vertex_distance_from_start_vertex:
            continue

        distance_from_start_to_neighbor = current_distance_from_start + graph[neighbor_key].weight_into

        if distance_from_start_to_neighbor < vertex_distance_from_start_vertex[neighbor_key]:
            unvisited_vertex_distance_from_start_vertex[neighbor_key] = distance_from_start_to_neighbor
            vertex_distance_from_start_vertex[neighbor_key] = distance_from_start_to_neighbor
            vertex_predecessor_key_from_start_vertex[neighbor_key] = current_vertex_key
            print(f"updating {neighbor_key} to {current_distance_from_start} + {graph[neighbor_key].weight_into} = {distance_from_start_to_neighbor} via {current_vertex_key}")

print(vertex_distance_from_start_vertex[end_vertex_key])