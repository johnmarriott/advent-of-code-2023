#!/usr/bin/emv python

import fileinput

field = []
for line in fileinput.input():
    field.append(line.strip())

scores = []
for j in range(len(field[0])):

    # something like [# O . . O # . O]
    column = [field[i][j] for i in range(len(field))]

    # since we are only going to count round rocks
    # adding a line of cube rocks at the top won't
    # contribute to the score.  Adding a line of cube rocks
    # at the bottom also won't, but will shift the index.
    # Since the actual bottom row gets weight 1 this is ok.
    # Pad the column with a # on each side so that we can
    # look at runs of slots strictly between #s
    #
    # it's now something like [# # O . . O # . O #]
    column.insert(0, '#')
    column.append('#')

    # indices of #s to sort between
    cube_indices = [i for i, x in enumerate(column) if x == "#"]
    
    # will be the column with Os sorted to the left of each group,
    # with 1s where Os are are zeroes elsewhere.  Start with a 
    # zero of the first # we're looking at
    sorted_column = [0]

    for i in range(1, len(cube_indices)):
        # would be [] then [O . . O] in our example string
        sub_column = column[cube_indices[i - 1] + 1 : cube_indices[i]]

        # turn O into 1 and . into 0 for sorting and later scoring
        sub_column_numeric = [1 if x == 'O' else 0 for x in sub_column] # e.g. [1 0 0 1]
        sub_column_numeric.sort(reverse=True) # e.g. [1 1 0 0]
        sorted_column.extend(sub_column_numeric)
        sorted_column.append(0) # add a 0 for the # between groups

    # sorted column is like [# # O O . . # O . #]
    #              which is [0 0 1 1 0 0 0 1 0 0]
    weights = [a * b for a, b in zip(sorted_column, list(reversed(range(len(sorted_column)))))]
    scores.append(sum(weights))

print(scores)
print(sum(scores))
