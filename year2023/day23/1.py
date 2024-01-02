#!/usr/bin/env python

"""
This works for the given input but I'm not confident that it works in general.

The solution to part two could be applied here 
"""

import fileinput
from dataclasses import dataclass
from queue import PriorityQueue

@dataclass
class Vertex:
    cost_from_start: int
    path_from_start: list[str]

def make_graph():
    vertices: dict[str, Vertex] = {}
    edges: dict[str, dict[str, int]] = {} 
    
    # the sample and full input both satisfy these assumptions, so we'll make them:
    # - there are hashes along the border except for the entrance/exit
    # - the entrance/exit only have routes straight down/up from them
    lines = [line.strip() for line in fileinput.input()]
    field = [list(line) for line in lines]

    start_key = "0,1"
    end_key = f"{len(field) - 1},{len(field[0]) - 2}"

    vertices[start_key] = Vertex(cost_from_start=0, path_from_start=[])
    vertices[end_key] = Vertex(cost_from_start=0, path_from_start=[])
    edges[start_key] = {"1,1": 1}
    edges[end_key] = {}

    for i in range(1, len(field) - 1):
        for j in range(1, len(field[0]) - 1):
            if field[i][j] != '.':
                continue

            vertex_key = f"{i},{j}"
            edges[vertex_key] = {}
            vertices[vertex_key] = Vertex(cost_from_start=0, path_from_start=[])

            for neighbor in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                # add edges from this vertex to its neighbors
                # if neighbor is a dot then add the usual edge
                # if neighbor is a slide, then (if we're at the top end of the
                # slide then add an edge to the one at the bottom of the slide
                # else don't add one)
                neighbor_symbol = field[neighbor[0]][neighbor[1]]

                if neighbor_symbol == ".":
                    edges[vertex_key][f"{neighbor[0]},{neighbor[1]}"] = 1
                elif neighbor_symbol == "#":
                    pass 
                elif neighbor_symbol == ">" and i == neighbor[0] and j == neighbor[1] - 1:
                    edges[vertex_key][f"{neighbor[0]},{neighbor[1] + 1}"] = 2
                elif neighbor_symbol == "v" and i == neighbor[0] - 1 and j == neighbor[1]:
                    edges[vertex_key][f"{neighbor[0] + 1},{neighbor[1]}"] = 2
                elif neighbor_symbol == "<" and i == neighbor[0] and j == neighbor[1] + 1: 
                    edges[vertex_key][f"{neighbor[0]},{neighbor[1] - 1}"] = 2
                elif neighbor_symbol == "^" and i == neighbor[0] - 1 and j == neighbor[1]:
                    edges[vertex_key][f"{neighbor[0] + 1},{neighbor[1]}"] = 2
                else:
                    pass # we're at the bottom of a slide

    return vertices, edges, start_key, end_key

vertices, edges, start_key, end_key = make_graph()

vertex_keys_to_visit = PriorityQueue()
vertex_keys_to_visit.put((-vertices[start_key].cost_from_start, start_key))

while not vertex_keys_to_visit.empty():
    _, vertex_key = vertex_keys_to_visit.get()
    vertex = vertices[vertex_key]
    neighbor_keys = edges[vertex_key]

    for neighbor_key in neighbor_keys:
        neighbor = vertices[neighbor_key]

        if (neighbor.cost_from_start < vertex.cost_from_start + edges[vertex_key][neighbor_key] and
            not neighbor_key in vertex.path_from_start):
            neighbor.cost_from_start = vertex.cost_from_start + edges[vertex_key][neighbor_key]
            neighbor.path_from_start = vertex.path_from_start + [vertex_key]
            vertex_keys_to_visit.put((-neighbor.cost_from_start, neighbor_key))

print(vertices[end_key].cost_from_start)
