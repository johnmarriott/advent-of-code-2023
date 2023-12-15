#!/usr/bin/env python

import fileinput

"""
turn characters into numbers: . is zero and # is one = binary string -> numeric value
so that the rows/columns of the field of ash and rocks are numeric

then look for reflections in the number arrays instead of vector comparisons

stop after finding the first mirror because, "you need to find a 
perfect reflection across either a horizontal line between two rows 
or across a vertical line between two columns"
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

def has_reflection(first, second):
    """
    does one of these lists have a reflection of the other in it
    
    [1, 2, 3] x [3, 2, 1, 5] have a reflection
    [1, 2, 3] x [1, 2, 3] do not
    """
    min_length = min(len(first), len(second))
    first.reverse() # reverse in place for comparison
    return first[:min_length] == second[:min_length]

def vertical_reflection_value(field):
    row_values = field_row_values(field)

    for i in range(1, len(row_values)):
        # if adjacent values are equal there might be a reflection between them
        if row_values[i-1] == row_values[i]:
            top_half = row_values[:i]
            bottom_half = row_values[i:]

            if has_reflection(top_half, bottom_half):
                value = 100 * i
                print(f"has vertical reflection: {value}")
                return value

    # no vertical reflection was found
    return 0

def horizonal_reflection_value(field):
    column_values = field_column_values(field)

    for j in range(1, len(column_values)):
        if column_values[j - 1] == column_values[j]:
            left_half = column_values[:j]
            right_half = column_values[j:]

            if has_reflection(left_half, right_half):
                value = j
                print(f"has horizontal reflection: {value}")
                return value
            
    # no horizontal reflection was found
    return 0

def mirror_value(field):
    for i in range(len(field)):
        for j in range(len(field[0])):
            print(" " if field[i][j] == "0" else "#", end="")
        print()

    horizontal_value = horizonal_reflection_value(field)

    if horizontal_value == 0: # no horizontal reflection
        return vertical_reflection_value(field)
    else:
        return horizontal_value

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
