#!/usr/bin/emv python

"""
big idea:
make it into 1/0/# from the start
don't put zeros in for #, just take that into account when scoring

one cycle: shift N W S E

after each spin cycle, look for a copy of this one in the past,
if it's there use that period to find the field matching the state
at one beellion spin cycles

score that final state
"""

import fileinput

FINAL_CYCLE = 1000000000

character_map = {
    "#": "#",
    "O": 1,
    ".": 0
}

def print_field(field, row_scores = None):
    if row_scores is None:
        row_scores = ['' for _ in field]

    for i in range(len(field)):
        for cell in field[i]:
            print(f"{' ' if cell == 0 else cell}", end="")
        print(f" {row_scores[i]}")
    print()

def print_fields(north, west, south, east):
    # assume they're the same size
    for i in range(len(north)):
        print(f"{''.join(str(' ' if x == 0 else x) for x in north[i])} {''.join(str(' ' if x == 0 else x) for x in west[i])} {''.join(str(' ' if x == 0 else x) for x in south[i])} {''.join(str(' ' if x == 0 else x) for x in east[i])}")
    print()

def shift_vectors(vectors):
    """
    for a list of vectors, shift each of them to the start

    e.g. [#, 0, 1, 0, #, 1, 0, #]
      -> [#, 1, 0, 0, #, 1, 0, #]
    to each vector in the list
    """
    shifted_vectors = []
    for vector in vectors:
        # split vector into sub-lists of elements between
        # hash characters as in part 1
        cube_indices = [i for i, x in enumerate(vector) if x == "#"]
        shifted_vector = ['#']

        for i in range(1, len(cube_indices)):
            sublist = vector[cube_indices[i - 1] + 1 : cube_indices[i]]
            sublist.sort(reverse=True)
            shifted_vector.extend(sublist)
            shifted_vector.append('#')

        shifted_vectors.append(shifted_vector)

    return shifted_vectors

def shift_north(field):
    # turn field into N to S vectors
    vectors = [[field[i][j] for i in range(len(field))] for j in range(len(field[0]))]
    
    shifted_vectors = shift_vectors(vectors)

    # reconstitute the field
    shifted_field = [[shifted_vectors[j][i] for j in range(len(shifted_vectors))] for i in range(len(shifted_vectors[0]))]
    return shifted_field

def shift_west(field):
    return shift_vectors(field)

def shift_south(field):
    # turn field into S to N vectors
    vectors = [[field[i][j] for i in reversed(range(len(field)))] for j in range(len(field[0]))]
    
    shifted_vectors = shift_vectors(vectors)

    # reconstitute the field
    shifted_field = [[shifted_vectors[j][i] for j in range(len(shifted_vectors))] for i in reversed(range(len(shifted_vectors[0])))]
    return shifted_field

def shift_east(field):
    # turn field into E to W vectors
    vectors = [list(reversed(row)) for row in field]
    shifted_vectors = shift_vectors(vectors)

    # reconstitute the field
    shifted_field = [list(reversed(row)) for row in shifted_vectors]
    return shifted_field

def spin_cycle(field, n):
    field_north = shift_north(field)
    field_west = shift_west(field_north)
    field_south = shift_south(field_west)
    field_east = shift_east(field_south)
    print(f"after {n} spins:")
    print_fields(field_north, field_west, field_south, field_east)
    return field_east

def field_row_scores(field):
    round_rock_counts = [x.count(1) for x in field]
    return [a * b for a, b in zip(round_rock_counts, list(reversed(range(len(field)))))]

field = []
for line in fileinput.input():
    # pad field with # so that we can always sub-sort between #s
    row = ['#']
    row.extend([character_map[x] for x in line.strip()])
    row.append('#')
    field.append(row)

def fields_period(fields):
    last_field = fields[len(fields) - 1]

    for i in reversed(range(len(fields) - 1)):
        if fields[i] == last_field:
            return len(fields) - i - 1

    return 0

hashes = ['#' for _ in range(len(field[0]))]
field.insert(0, hashes)
field.append(hashes)
print_field(field)

fields = [field] # field zero is the initial state

while len(fields) < FINAL_CYCLE + 1: 
    field = spin_cycle(field, len(fields))
    fields.append(field)
    period = fields_period(fields)

    if period > 0:
        offset = period - ((FINAL_CYCLE - len(fields) + 1) % period)
        final_board = fields[len(fields) - 1 - offset]
        print(f"period {period} after {len(fields) - 1} spin cycles, go back {offset} to index {len(fields) - offset - 1}\n")

        row_scores = field_row_scores(final_board)
        print_field(final_board, row_scores)
        print(sum(row_scores))

        break
