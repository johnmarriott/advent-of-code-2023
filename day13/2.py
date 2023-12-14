#!/usr/bin/env python

import fileinput

"""
turn characters into numbers: . is zero and # is one = binary string -> numeric value
so that the rows/columns of the field of ash and rocks are numeric

for a smudged: the reflections of the lists should match apart from exactly one
pair of values, and these values differ in exactly one binary place value
"""

def field_row_values(field):
    """
    numeric values of rows of a field converted to binary digits

    e.g.
    [[1, 0],  turns into  [2,
     [0, 1]]               1]
    """
    return [int("".join(row), 2) for row in field]

def field_column_values(field):
    """
    numeric values of columns of a field converted to binary digits

    e.g.
    [[1, 0], 
     [0, 1]]
             turns into
     [2, 1]
    """
    return [int("".join([row[j] for row in field]), 2) for j in range(len(field[0]))]

def has_smudged_reflection(first, second):
    """
    is the pairwise xor of the elements of this list all zeroes with exactly one power of two?

    [1, 10, 2] x [2, 2, 1, 4] has a smudged reflection because the pairwise
    differences (from the x out) are [0, 10, 0] which could be that one side
    has #.#. = 10 and the other has ..#. = 2 which can be fixed

    [1, 10, 1] x [2, 2, 1, 4] does not since the differences are [1, 8, 0] and
    we would have to fix two smudges
    """
    min_length = min(len(first), len(second))
    first.reverse() # reverse in place for comparison
    differences = [first[i] ^ second[i] for i in range(min_length)]

    n_differences_nonzero = sum([1 if x != 0 else 0 for x in differences])
    if n_differences_nonzero != 1:
        return False
    else:
        nonzero_difference = sum(differences) # all the rest are zero

        # int.bit_count() will "Return the number of ones in the binary representation 
        # of the absolute value of the integer"
        # and a power of two has exactly one one in its binary representation
        return nonzero_difference.bit_count() == 1 

def smudged_vertical_reflection_value(field):
    row_values = field_row_values(field)

    for i in range(1, len(row_values)):
        top_half = row_values[:i]
        bottom_half = row_values[i:]

        if has_smudged_reflection(top_half, bottom_half):
            value = 100 * i
            print(f"has smudged vertical reflection: {value}") 
            return value

    return 0

def smudged_horizontal_reflection_value(field):
    column_values = field_column_values(field)

    for j in range(1, len(column_values)):
        left_half = column_values[:j]
        right_half = column_values[j:]

        if has_smudged_reflection(left_half, right_half):
            value = j
            print(f"has smudged horizontal reflection: {value}")
            return value
            
    return 0

def mirror_value(field):
    for i in range(len(field)):
        for j in range(len(field[0])):
            print(" " if field[i][j] == "0" else "#", end="")
        print()

    value = smudged_vertical_reflection_value(field)
    if value == 0: 
        value = smudged_horizontal_reflection_value(field)
        if value == 0:
            # something wrong, every field should have a valid reflection
            # (this will cause sum at end to fail)
            return None
        else:
            return value
    else:
        return value

current_field = []
fields = [current_field]

for line in fileinput.input():
    row = ["0" if x == "." else "1" for x in line.strip()]

    if row == []:
        current_field = []
        fields.append(current_field)
    else:
        current_field.append(row)

field_values = [mirror_value(field) for field in fields]

print(sum(field_values))
