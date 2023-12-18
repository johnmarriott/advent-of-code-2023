#!/usr/bin/env python

import fileinput
import re
from dataclasses import dataclass
from shapely.geometry import Polygon
from shapely.ops import unary_union

"""
big idea:

construct a polygon out of blocks on the path
- first block is a 1x1 square "at" (0, 0) 
  - initial polygon has coords (0, 0), (1, 0), (1, -1), (0, -1)
  - the "pen position" is the top left corner of the last block to be added,
    currently (0, 0)

- adding a movement, e.g., R6, becomes:
  - R6 is a 6x1 rectangle
  - since it moves right, it starts at the top right corner of square with
    its top left corner at the pen position: (1, 0)
  - this polygon is (1,0), (7,0), (7,-1), (1, -1)
  - the square at the end of the polygon (i.e., if we were adding six squares
    on one at a time, the last square to be added) has a top left corner
    at (6, 0) so that is the new pen position

in general, to do a movement we add a new rectangle to the list of polygons
and update the pen position to the top left corner of the "last square added"

when the path has been turned into a list of polygons, then:
- merge them into one polygon, it will be a width-1 square around the lava pit,
  with both exterior and interior points included
- take only the exterior points of this polygon, this is the boundary of the pit
"""

@dataclass
class Point:
    x: int
    y: int

def next_polygon(position: Point, direction: str, length: int):
    """
    Return a tuple of rectangle that would be tacked on to a unit square with top
    left corner at `position` that goes in the given `direction` and `length` and
    the updated position which is the coordinate of the top left corner of the 
    "last" square added to the path along this rectangle
    """

    if direction == "3": # up
        new_polygon = Polygon([ 
            (position.x, position.y),
            (position.x, position.y + length),
            (position.x + 1, position.y + length),
            (position.x + 1, position.y)
        ]) 
        new_position = Point(position.x, position.y + length)
        return new_polygon, new_position

    if direction == "2": # left
        new_polygon = Polygon([ 
            (position.x, position.y),
            (position.x - length, position.y),
            (position.x - length, position.y - 1),
            (position.x, position.y - 1)
        ]) 
        new_position = Point(position.x - length, position.y)
        return new_polygon, new_position

    if direction == "1": # down
        new_polygon = Polygon([ 
            (position.x, position.y - 1),
            (position.x + 1, position.y - 1),
            (position.x + 1, position.y - 1 - length),
            (position.x, position.y - 1 - length)
        ]) 
        new_position = Point(position.x, position.y - length)
        return new_polygon, new_position

    # else direction = 0 = right
    new_polygon = Polygon([ 
        (position.x + 1, position.y),
        (position.x + 1 + length, position.y),
        (position.x + 1 + length, position.y - 1),
        (position.x + 1, position.y - 1)
    ]) 
    new_position = Point(position.x + length, position.y)
    return new_polygon, new_position
  

# start at (0, 0) and an initial unit square
current_position = Point(0, 0)
polygons = [Polygon([(0, 0), (1, 0), (1, -1), (0, -1)])]

for line in fileinput.input():
    hex_part = re.sub(r".*#", "", line.strip())

    length_hex = hex_part[0:5]
    length = int(length_hex, 16)

    direction = hex_part[5:6]

    polygon, current_position = next_polygon(current_position, direction, length)
    polygons.append(polygon)

merged_polygon = unary_union(polygons)
merged_polygon_exterior = Polygon(merged_polygon.exterior.coords)

print(int(merged_polygon_exterior.area))
