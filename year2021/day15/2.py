#!/usr/bin/env python

import fileinput
import math
from dataclasses import dataclass

@dataclass
class Vertex:
    weight_into: int
    neighbor_keys: list[str]

# read input into a matrix ####

# a table for looking up the pseudo-addition of x + n
# by indexing pseudo_add[x][n]
# where x in 1 .. 9 and n in 1 .. 8
# and values wrap around from 9 to 1
# e.g. 9 "+" 1 = 1, 8 "+" 3 = 2
#
# could also do this by summing the digits of x + n, 
# e.g. 9 + 2 = 11 = 1 + 1 = 2 = 9 "+" 2
pseudo_add = [ 
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], # 0 "+" x
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 1], # 1 "+" x
    [2, 3, 4, 5, 6, 7, 8, 9, 1, 2], # 2 "+" x
    [3, 4, 5, 6, 7, 8, 9, 1, 2, 3], # 3 "+" x
    [4, 5, 6, 7, 8, 9, 1, 2, 3, 4], # 4 "+" x
    [5, 6, 7, 8, 9, 1, 2, 3, 4, 5], # 5 "+" x
    [6, 7, 8, 9, 1, 2, 3, 4, 5, 6], # 6 "+" x
    [7, 8, 9, 1, 2, 3, 4, 5, 6, 7], # 7 "+" x
    [8, 9, 1, 2, 3, 4, 5, 6, 7, 8], # 8 "+" x
    [9, 1, 2, 3, 4, 5, 6, 7, 8, 9], # 9 "+" x
]

input = [[int(x) for x in line.strip()] for line in fileinput.input()]
matrix = [[0 for _ in range(len(input[0]) * 5)] for _ in range(len(input) * 5)]
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        n = int(i / len(input)) + int(j / len(input[0]))
        matrix[i][j] = pseudo_add[input[i % len(input)][j % len(input[0])]][n]

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
    print(len(unvisited_vertex_distance_from_start_vertex))
    current_vertex_key = min(unvisited_vertex_distance_from_start_vertex, key=unvisited_vertex_distance_from_start_vertex.get)
    current_distance_from_start = vertex_distance_from_start_vertex[current_vertex_key]

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

print(vertex_distance_from_start_vertex[end_vertex_key])