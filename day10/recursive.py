import fileinput

"""
this only does part one, because I:
- wrote this recursively at first
- hit Python's default recursion limit (which is 1000, come on)
- rewrote it iteratively to find out what the actual path length is
- came back and set the recursion limit higher and it worked
- added on to the iterative version for part two (but it should work find with this one if it maintained the path)
"""

import sys
sys.setrecursionlimit(100000) # default is 1000

# map of node character to "joins" which are the N/E/S/W directions it connects to
# e.g. a vertical pipe joins to the node N and S and not E W of it, so it's T/F/T/F
node_character_to_joins = {
     "|": [True, False, True, False],
     "-": [False, True, False, True],
     "L": [True, True, False, False],
     "J": [True, False, False, True],
     "7": [False, False, True, True],
     "F": [False, True, True, False],
     ".": [False, False, False, False],
     "S": [True, True, True, True] 
}

# these lists of info about directions are kinda ugly, this was improved 
# in the iterative version (didn't bring that back here)
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

directions = [NORTH, EAST, SOUTH, WEST]
direction_names = ["north", "east", "south", "west"]
opposite_directions = [SOUTH, WEST, NORTH, EAST] # lookup so that opposite_direction[NORTH] = SOUTH

# lookup for the offset to move in this direction
# so that offset[SOUTH] = 1 and offset[EAST] = 0
vertical_direction_offset = [-1, 0, 1, 0]

# similar to vertical offset, offset[EAST] = 1
horizontal_direction_offset = [0, 1, 0, -1]

def path_to_start(i, j, from_direction):
    """
    look for a path to the start from node index (i, j)
    and coming from from_direction (so we know how not to backtrack)

    returns (True, n) if a loop back to S is found from the given (i, j) index
      where n is the number of steps from (i. j) to the start
    returns (False, x) if a loop back to S isn't found from (i, j), value of x doesn't matter
    """

    print(f"at ({i}, {j}) coming from the {direction_names[from_direction]} / ", end="")

    # base case 1 - found the start and we're not in the initial call
    if i == start_index[0] and j == start_index[1] and from_direction != -1:
        return True, 0

    # recursive case -- see if we can go any of N/E/S/W and if so try going that way
    # if we can't go anywhere then return False

    # try to go each direction - did I not come from there, 
    # can I go there, and can that node connect to me?
    for direction in directions:

        # don't go back the way we came
        if from_direction == direction:
            continue

        opposite_direction = opposite_directions[direction]
        next_i = i + vertical_direction_offset[direction]
        next_j = j + horizontal_direction_offset[direction]

        if (nodes[i][j][direction] and nodes[next_i][next_j][opposite_direction]):
                print(f"try going {direction_names[direction]}")
                success, length = path_to_start(next_i, next_j, from_direction=opposite_direction)
                if success:
                    return success, length + 1
    
    # if we made it here then no direction worked out
    return False, 0

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

# find a path from the start, stopping after first success since
# "the pipe that contains the animal is one large, continuous loop"
for direction in directions:
    opposite_direction = opposite_directions[direction]
    next_i = start_index[0] + vertical_direction_offset[direction]
    next_j = start_index[1] + horizontal_direction_offset[direction]

    if nodes[next_i][next_j][opposite_direction]:
        print(f"start going {direction_names[direction]}")
        success, length = path_to_start(next_i, next_j, from_direction=opposite_direction)
        if success:
            # since the connections are all square the furthest distance is the number of steps/2
            print((length + 1) / 2)
            break
