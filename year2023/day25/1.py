#!/usr/bin/env python

"""
In short, find source/target vertices where a min cut between them is of size three,
the product of the sizes of the two connected components.

Long story: 

Treat the input as an undirected graph (this would all work the same and
fit better with the network ideas as a directed graph but I started it as undirected
and didn't undo that) where components are vertices and connections are edges.

Randomly pick source and target vertices.  These will be in the two connected components
of the disjoint graph we get after removing the right three edges.

The right three edges are the "minimum cut" of the graph.

Use the idea of the Ford-Fulkerson algorithm to:

- find a path from source to target
- remove the edges of this path from the graph
- find a path from source to target in the modified graph
- remove / find / remove so that we've now removed three paths
- try and fail to find a path from source to target since the
  three minimum cut edges were parts of the three paths removed,
  so source is disconnected from target now

This method depends on the initial choice of source and target, so try the above
with a random source/target until a valid choice is found, that is, the above steps 
happened (including failing to find a path in the last step).

When a valid source/target are found, can use BFS to find all vertices reachable by
the source vertex so that the sizes of the two components are known.

I think this whole thing could be a call to networkx.min_cut, wrote this before 
realizing that, oh well.

Also swapped out a manual implementation of path_from_start_to_end
with just wrapping a scipy function by converting from a list to an adjacency
matrix and back again.  Could treat it as an adjacency matrix everywhere to avoid 
that (but could avoid all of that with the above networkx call anyway).
"""

import copy
import fileinput
import numpy as np
import random
from collections import defaultdict, deque
from scipy.sparse.csgraph import shortest_path

NO_EDGE = -9999 # what scipy shortest_path denotes no edge with

vertices = defaultdict(list)

for line in fileinput.input():
    parts = line.strip().split(": ")
    from_label = parts[0]
    to_labels = parts[1].split(" ")

    for to_label in to_labels:
        vertices[from_label].append(to_label)
        vertices[to_label].append(from_label)

def path_from_start_to_end(vertices, start, end):
    """
    return a list of edges that are some path from the start 
    to the end vertex
    """

    vertex_keys = list(vertices.keys())

    adjacency_matrix = np.zeros((len(vertex_keys), len(vertex_keys)))

    for vertex_key in vertex_keys:
        for neighbor_key in vertices[vertex_key]:
            adjacency_matrix[vertex_keys.index(vertex_key)][vertex_keys.index(neighbor_key)] = 1

    start_index = vertex_keys.index(start)
    end_index = vertex_keys.index(end)
    
    _, adjacency_path = shortest_path(adjacency_matrix, directed=False, return_predecessors=True)

    index_path = [end_index]
    i = end_index
    while adjacency_path[start_index, i] != NO_EDGE: 
        index_path.append(adjacency_path[start_index, i])
        i = adjacency_path[start_index, i]

    path = [vertex_keys[i] for i in index_path]
    return list(reversed(path))

def vertices_reachable_from_vertex(vertices, vertex):
    """
    return a list of vertices that are reachable from the
    given vertex, including that vertex
    """

    vertices_to_visit: deque[str] = deque([vertex])
    visited_vertices = set()

    while len(vertices_to_visit) > 0:
        vertex_to_visit = vertices_to_visit.popleft()

        if vertex_to_visit in visited_vertices:
            continue

        visited_vertices.add(vertex_to_visit)
        unvisited_neighbors = set(vertices[vertex_to_visit]) - visited_vertices
        vertices_to_visit.extend(unvisited_neighbors)

    return list(visited_vertices)

def min_cut_sizes(vertices: dict[list[str]], source, target) -> (int, int, int):
    """
    return a tuple of the number of edges in the min cut that separates 
    source from target, the number of vertices in the source connected component,
    and the number of vertices in the target connected component
    """

    vertices_mutable: dict[list[str]] = copy.deepcopy(vertices)

    # mutate graph in place by removing edges on paths from start to end
    # until there is no path from start to end
    graph_has_path_start_to_end = True
    n_paths_removed = 0

    while graph_has_path_start_to_end:
        maybe_path_from_start_to_end = path_from_start_to_end(vertices_mutable, source, target)

        if len(maybe_path_from_start_to_end) < 2:
            graph_has_path_start_to_end = False
            break

        n_paths_removed += 1

        # pair up the vertex labels, the path [a b c d] turns into pairs
        # (a, b), (b, c), (c, d)
        path_edges = zip(maybe_path_from_start_to_end[:-1], maybe_path_from_start_to_end[1:])

        for path_edge in path_edges:
            # both since undirected
            vertices_mutable[path_edge[0]].remove(path_edge[1])
            vertices_mutable[path_edge[1]].remove(path_edge[0])

    # find all vertices reachable from the source, these are one of the
    # two connected components of the remaining graph.  Ones not found
    # by this are the other
    source_component = vertices_reachable_from_vertex(vertices_mutable, source)

    # list all original edges that would connect these components
    min_cut = []
    for vertex, neighbors in vertices.items():
        for neighbor in neighbors:
            if ((vertex in source_component and neighbor not in source_component) or 
                (vertex not in source_component and neighbor in source_component)):
                min_cut.append((vertex, neighbor))

    n_vertices_source_component = len(source_component)
    n_vertices_target_component = len(vertices.keys()) - n_vertices_source_component
    return n_paths_removed, n_vertices_source_component, n_vertices_target_component

min_cut_size = 0

while min_cut_size != 3:
    # since graph is currently connected, pick two as the network's
    # source and target vertices
    source = random.choice(list(vertices.keys()))
    target = random.choice(list(vertices.keys()))

    sizes = min_cut_sizes(vertices, source, target)
    min_cut_size = sizes[0]

print(sizes[1] * sizes[2])
