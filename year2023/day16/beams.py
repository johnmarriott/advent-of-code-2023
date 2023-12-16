#!/usr/bin/env python

"""
pad the field with a new @ character, it's a light sink: if the 
beam hits it then the light is extinguished
"""

import fileinput
from dataclasses import dataclass
from enum import Enum
from termcolor import colored

Direction = Enum("Direction", ["NORTH", "EAST", "SOUTH", "WEST"])
Node = Enum("Node", ["SINK", "VERTICAL_SPLITTER", "HORIZONTAL_SPLITTER", "SW_TO_NE_MIRROR", "NW_TO_SE_MIRROR", "EMPTY"])

@dataclass
class Beam:
    row: int
    col: int
    direction: Direction

    def __str__(self):
        return(f"{self.row},{self.col},{self.direction}")

symbol_to_node = {
    "@": Node.SINK,
    "|": Node.VERTICAL_SPLITTER,
    "-": Node.HORIZONTAL_SPLITTER,
    "/": Node.SW_TO_NE_MIRROR,
    "\\": Node.NW_TO_SE_MIRROR,
    ".": Node.EMPTY
}

# color to print the map per the number of light beams there, see possible by termcolor.COLORS
def beam_count_color(n):
    if n <= 0:
        return "white"
    if n == 1:
        return "yellow"
    if n == 2:
        return "green"
    return "magenta"

def print_state(map, beams: list[Beam], energy_field):
    if len(map) > 15:
        return

    for i in range(len(map)):
        for j in range(len(map[0])):
            n_beams_here = sum(1 for beam in beams if beam.row == i and beam.col == j)
            print(colored(map[i][j], beam_count_color(n_beams_here)), end="")
        
        print(f" {''.join(['#' if x == 1 else ' ' for x in energy_field[i]])}")
    print()

def nodes_energized_starting_at(intital_beam):
    print(f"starting at {intital_beam}")

    # initialize energy field as all positions unvisited
    energy_field = [[0 for _ in range(len(map[0]))] for _ in range(len(map))]

    # start off with one beam going east from the sink left of 1,1
    beams = [intital_beam]
    print_state(map, beams, energy_field)

    # keep track of row/col/directions that a beam of light has passed through
    # so loops can die
    states_seen = [str(beams[0])]

    while len(beams) > 0:
        # new beams in this iteration, will add to list after we loop over it
        new_beams = []

        for beam in beams:
            # advance a step
            if beam.direction == Direction.NORTH:
                beam.row -= 1
            elif beam.direction == Direction.EAST:
                beam.col += 1
            elif beam.direction == Direction.SOUTH:
                beam.row += 1
            else: # must be west
                beam.col -= 1

            # act on the new position's node type
            node = symbol_to_node[map[beam.row][beam.col]]
            if node == Node.EMPTY or map[beam.row][beam.col] == Node.SINK:
                next
            elif node == Node.HORIZONTAL_SPLITTER:
                # if moving east/west do nothing
                if beam.direction == Direction.NORTH or beam.direction == Direction.SOUTH:
                    beam.direction = Direction.EAST
                    new_beams.append(Beam(beam.row, beam.col, Direction.WEST))
            elif node == Node.VERTICAL_SPLITTER:
                # if moving north/south do nothing
                if beam.direction == Direction.EAST or beam.direction == Direction.WEST:
                    beam.direction = Direction.NORTH
                    new_beams.append(Beam(beam.row, beam.col, Direction.SOUTH))
            elif node == Node.NW_TO_SE_MIRROR:
                if beam.direction == Direction.NORTH:
                    beam.direction = Direction.WEST
                elif beam.direction == Direction.EAST:
                    beam.direction = Direction.SOUTH
                elif beam.direction == Direction.SOUTH:
                    beam.direction = Direction.EAST
                else: # it's going west
                    beam.direction = Direction.NORTH
            else: # it's a SW to NE mirror
                if beam.direction == Direction.NORTH:
                    beam.direction = Direction.EAST
                elif beam.direction == Direction.EAST:
                    beam.direction = Direction.NORTH
                elif beam.direction == Direction.SOUTH:
                    beam.direction = Direction.WEST
                else: # it's going west
                    beam.direction = Direction.SOUTH

        # discard beams that are now a sink
        beams[:] = [beam for beam in beams if not symbol_to_node[map[beam.row][beam.col]] == Node.SINK]

        # add new beams in this pass
        beams.extend(new_beams)

        # discard beams that are in previously-seen states
        beams[:] = [beam for beam in beams if not str(beam) in states_seen]

        # energize and track current positions
        for beam in beams:
            energy_field[beam.row][beam.col] = 1
            states_seen.append(str(beam))

        print_state(map, beams, energy_field)

    return sum([sum(line) for line in energy_field])

# read input ####
lines = [line.strip() for line in fileinput.input()]

# pad the map with sinks
sinks = ["@" for _ in range(len(lines[0]) + 2)]
map = [sinks]
for line in lines:
    map.append(["@"] + list(line) + ["@"])
map.append(sinks)

# part one ####
start_beam = Beam(1, 0, Direction.EAST)
print(f"part one: {nodes_energized_starting_at(start_beam)}")

# part two ####
edge_starts = (
    [Beam(0, col, Direction.SOUTH) for col in range(len(map[0]))] +
    [Beam(len(map[0]) - 1, col, Direction.NORTH) for col in range(len(map[0]))] +
    [Beam(row, 0, Direction.EAST) for row in range(len(map))] +
    [Beam(row, len(map) - 1, Direction.WEST) for row in range(len(map))] 
)

energies = [nodes_energized_starting_at(beam) for beam in edge_starts]
print(f"part two: {max(energies)}")