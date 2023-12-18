#!/usr/bin/env python

import fileinput
import re
from dataclasses import dataclass

@dataclass
class Point:
    row: int
    col: int

def direction_char_to_offset(direction_char):
    """
    (row, column) index offsets to travel in the direction of the input character
    """
    if direction_char == "U":
        return -1, 0
    if direction_char == "D":
        return 1, 0
    if direction_char == "L":
        return 0, -1
    if direction_char == "R":
        return 0, 1
    
current_point = Point(0, 0)
path = [current_point]

for line in fileinput.input():
    direction = line[0]
    length = int(re.sub(r".* (\d+) .*", r"\1", line))

    row_offset, column_offset = direction_char_to_offset(direction)

    for _ in range(length):
        current_point = Point(current_point.row + row_offset, current_point.col + column_offset)
        path.append(current_point)

path_row_values = [point.row for point in path]
path_col_values = [point.col for point in path]
max_row = max(path_row_values)
min_row = min(path_row_values)
max_col = max(path_col_values)
min_col = min(path_col_values)

for i in range(min_row, max_row + 1):
    for j in range(min_col, max_col + 1):
        if len([p for p in path if p.row == i and p.col == j]) > 0:
            print('#', end="")
        else:
            print(' ', end="")
    print()
print()

# use pnpoly from day 10 to find interior points
def point_in_polygon(vertx, verty, testx, testy):
    """
    Python implementation of PNPOLY at https://wrfranklin.org/Research/Short_Notes/pnpoly.html
    keeping the variable names close to the C implementation, this could be improved upon, e.g. https://github.com/JoJocoder/PNPOLY/tree/master

    vertx - list of x coordinates of polygon
    verty - list of y coordinates of polygon
    testx, testy - coordinate to test if it's in the polygon

    returns True if the point is in the interior of the polygon, False if it is in the exterior, and undocumented if it is on the boundary
    """

    c = False
    nvert = len(vertx)
    j = nvert - 1
  
    for i in range(nvert):
        if ( ((verty[i]>testy) != (verty[j]>testy)) 
            and (testx < (vertx[j]-vertx[i]) * (testy-verty[i]) / (verty[j]-verty[i]) + vertx[i]) ):
            c = not c

        j = i

    return c

interior_points = []
for i in range(min_row, max_row + 1):
    for j in range(min_col, max_col + 1):
        if  point_in_polygon(path_row_values, path_col_values, i, j):
            interior_points.append(Point(i, j))

lava_points = 0
for i in range(min_row, max_row + 1):
    for j in range(min_col, max_col + 1):
        if (len([p for p in path if p.row == i and p.col == j]) + 
            len([p for p in interior_points if p.row == i and p.col ==j])> 0):
            lava_points += 1
            print('#', end="")
        else:
            print(' ', end="")
    print()
print()

print(lava_points)
