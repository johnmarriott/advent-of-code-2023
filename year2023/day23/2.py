#!/usr/bin/env python

import fileinput
import networkx as nx
from collections import defaultdict

"""
Big idea: treat this as a weighted undirected graph.  Enumerate (NetworkX's all simple graphs
is used here but anything should work) the paths from start to end and take the one with the
greatest path weight.

Before doing that, simplify the graph.  It has a lot of "hallways" that can be removed, for example
in the sample input it isn't until the path is at row 4, column 12 that there's a choice of direction.  
The path from the start to that spot can be treated as one edge with a weight of the steps skipped
between them.

For example, in this graph

    a -1- b -1- c -1- d ...
    |     |           |
    1     1           1
    |     |           |
    e -1- f -1- g -1- h
    .
    .
    .
    
c can be snipped, which results in

    a -1- b ----2---- d ...
    |     |           |
    1     1           1
    |     |           |
    e -1- f -1- g -1- h
    .
    .
    .

This simplifies the graph from (in my input file) 9424 vertices to 36, so the naïve enumeration of all paths works.
"""

# weights is a dict/dict of edge weights between vertices.  Since this is an undirected
# graph, use these helper functions to store one weight for each pair of vertices
def set_weight_between(vertex_key_a, vertex_key_b, weight, weights):
    if vertex_key_a < vertex_key_b:
        weights[vertex_key_a][vertex_key_b] = weight
    else:
        weights[vertex_key_b][vertex_key_a] = weight

def weight_between(vertex_key_a, vertex_key_b, weights) -> int:
    if vertex_key_a < vertex_key_b:
        return weights[vertex_key_a][vertex_key_b]
    else:
        return weights[vertex_key_b][vertex_key_a]

def forget_weight(vertex_key_a, vertex_key_b, weights):
    if vertex_key_a < vertex_key_b:
        del weights[vertex_key_a][vertex_key_b]
    else:
        del weights[vertex_key_b][vertex_key_a]


def make_graph():
    vertices: dict[str, list[str]] = defaultdict(list)
    weights: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    # the sample and full input both satisfy these assumptions, so we'll make them:
    # - there are hashes along the border except for the entrance/exit
    # - the entrance/exit only have routes straight down/up from them
    lines = [line.strip() for line in fileinput.input()]
    field = [list(line) for line in lines]

    start_key = "0,1"
    end_key = f"{len(field) - 1},{len(field[0]) - 2}"
    vertex_above_end_key = f"{len(field) - 2},{len(field[0]) - 2}"

    vertices[start_key] = ["1,1"]
    weights[start_key]["1,1"] = 1

    vertices[end_key] = [vertex_above_end_key]
    weights[end_key][vertex_above_end_key] = 1

    for i in range(1, len(field) - 1):
        for j in range(1, len(field[0]) - 1):
            if field[i][j] == '#':
                continue

            vertex_key = f"{i},{j}"

            for neighbor in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                # add edges from this vertex to its neighbors
                # if neighbor is a non-hash then add the usual edge
                neighbor_symbol = field[neighbor[0]][neighbor[1]]

                if not neighbor_symbol == "#":
                    vertices[vertex_key].append(f"{neighbor[0]},{neighbor[1]}")
                    set_weight_between(vertex_key, f"{neighbor[0]},{neighbor[1]}", 1, weights)

    return vertices, weights, start_key, end_key

vertices, weights, start_key, end_key = make_graph()

def snip_graph(vertices: dict[str, list[str]], weights):
    """
    Try to modify the graph by removing vertices with exactly two neighbors.  
    Return True if it was possible.
    """

    vertices_with_two_neighbors = [key for key in vertices.keys() if len(vertices[key]) == 2]

    if len(vertices_with_two_neighbors) == 0:
        return False

    vertex_with_two_neighbors = vertices_with_two_neighbors[0]
    left_neighbor = vertices[vertex_with_two_neighbors][0] # may not actually be left/right in the original layout
    right_neighbor = vertices[vertex_with_two_neighbors][1]

    vertices[left_neighbor].remove(vertex_with_two_neighbors)
    vertices[left_neighbor].append(right_neighbor)

    vertices[right_neighbor].remove(vertex_with_two_neighbors)
    vertices[right_neighbor].append(left_neighbor)

    del vertices[vertex_with_two_neighbors]

    set_weight_between(
        left_neighbor, 
        right_neighbor, 
        weight_between(vertex_with_two_neighbors, left_neighbor, weights) + weight_between(vertex_with_two_neighbors, right_neighbor, weights),
        weights
    )
    
    forget_weight(vertex_with_two_neighbors, left_neighbor, weights)
    forget_weight(vertex_with_two_neighbors, right_neighbor, weights)

    return True

# condense graph by snipping vertices with exactly two neighbors
while snip_graph(vertices, weights):
    pass

graph = nx.Graph(vertices)

longest_path = None
longest_path_weight = 0

for path in nx.all_simple_paths(graph, start_key, end_key):
    path_pairs = zip(path[:-1], path[1:])

    path_weight = 0
    for edge in list(path_pairs):
        path_weight += weight_between(edge[0], edge[1], weights)

    if path_weight > longest_path_weight:
        longest_path_weight = path_weight
        longest_path = path

print(f"\n\n{longest_path_weight}")