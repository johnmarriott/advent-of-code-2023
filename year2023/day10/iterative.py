import fileinput

"""
big idea of part one: 
lean heavily on the given "the pipe that contains the animal is one large, continuous loop"
to always take the first valid connection, without any depth/breadth-first-search backtracking/memory

big idea of part two: 
- make a polygon out of the vertices of the path found in part one
- test if every point not on the path is in the interior of this polygon (PNPOLY)

PNPOLY:
A web page by W. Randolph Franklin gives an algorithm for testing if a point is in a polygon.  
If you don't care about what this says about points on the boundary of a polygon you can use it as-is.  
We don't, so we will use it

In C this algorithm is (https://wrfranklin.org/Research/Short_Notes/pnpoly.html):

int pnpoly(int nvert, float *vertx, float *verty, float testx, float testy)
{
  int i, j, c = 0;
  for (i = 0, j = nvert-1; i < nvert; j = i++) {
    if ( ((verty[i]>testy) != (verty[j]>testy)) &&
	 (testx < (vertx[j]-vertx[i]) * (testy-verty[i]) / (verty[j]-verty[i]) + vertx[i]) )
       c = !c;
  }
  return c;
}
"""

# properties for each direction
# vertical/horizontal offsets are amount to add to the respective index to move in that direction
directions = {
    "north": {
        "opposite_direction": "south",
        "vertical_offset": -1,
        "horizontal_offset": 0,
    },
    "east": {
        "opposite_direction": "west",
        "vertical_offset": 0,
        "horizontal_offset": 1
    },    
    "south": {
        "opposite_direction": "north",
        "vertical_offset": 1,
        "horizontal_offset": 0,
    },
    "west": {
        "opposite_direction": "east",
        "vertical_offset": 0,
        "horizontal_offset": -1
    }
}

direction_names = directions.keys()

# map of node character to its "joins" which are the N/E/S/W directions it connects to
# e.g. a vertical pipe joins to the node N and S and not E W of it, so it's T/F/T/F
node_character_to_joins = {
     "|": { "north": True, "east": False, "south": True, "west": False },
     "-": { "north": False, "east": True, "south": False, "west": True },
     "L": { "north": True, "east": True, "south": False, "west": False },
     "J": { "north": True, "east": False, "south": False, "west": True },
     "7": { "north": False, "east": False, "south": True, "west": True },
     "F": { "north": False, "east": True, "south": True, "west": False },
     ".": { "north": False, "east": False, "south": False, "west": False },
     "S": { "north": True, "east": True, "south": True, "west": True } 
}

def path_to_start(i, j, from_direction_name):
    """
    look for a path to the start from node (i, j)
    and coming from from_direction (so we know how not to backtrack)

    assume a valid path exists
    """

    steps = 1 # we took the first step to get here
    while i != start_index[0] or j != start_index[1]: # we haven't looped back to start yet
        path.append([i, j])

        for direction_name in direction_names:
            direction = directions[direction_name]
            if direction_name == from_direction_name: # we would go back the way we came
                continue # skip this direction

            next_i = i + direction["vertical_offset"]
            next_j = j + direction["horizontal_offset"]

            # go this way if it's a valid path
            if (nodes[i][j][direction_name] and nodes[next_i][next_j][direction["opposite_direction"]]):
                print(f"going {direction_name}")
                i = next_i
                j = next_j
                from_direction_name = direction["opposite_direction"]
                steps += 1
                break # break inner for to restart search (outer while) at these new coordinates

    return steps

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

# read stdin to `characters` with a padding of dots around the input
characters = []
for line in fileinput.input():
    row = ['.'] + list(line.strip()) + ['.']
    characters.append(row)

dots = ['.' for x in characters[0]]
characters.insert(0, dots)
characters.append(dots)

# convert characters of text to characters of node connections
nodes = []
for i in range(len(characters)):
    nodes.append([])
    for j in range(len(characters[i])):
        character = characters[i][j]
        print(character, end="")
        nodes[i].append(node_character_to_joins[character])
        if character == "S":
           start_index = [i, j]
    print()

print(f"S is at {start_index}")

path = [start_index]

# part one: take the first valid direction from the start
for direction_name in direction_names:
    direction = directions[direction_name]
    next_i = start_index[0] + direction["vertical_offset"]
    next_j = start_index[1] + direction["horizontal_offset"]

    if nodes[next_i][next_j][direction["opposite_direction"]]:
        print(f"start going {direction_name}")
        length = path_to_start(next_i, next_j, from_direction_name=direction["opposite_direction"])

        # since connections are square the path length is even
        print(f"part one: {length / 2}")
        break # we found a solution (we would come across the reverse path if we didn't stop)

path_x_values = [x[0] for x in path]
path_y_values = [x[1] for x in path]
n_points_interior = 0

# part two: count interior points
for i in range(len(nodes)):
    for j in range(len(nodes[i])):
        if not [i, j] in path:
            if point_in_polygon(path_x_values, path_y_values, i, j): 
                n_points_interior += 1

print(f"part two: {n_points_interior}")