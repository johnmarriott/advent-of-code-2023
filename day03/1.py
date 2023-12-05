import fileinput

field = []
sum = 0

# read stdin to `field` with a padding of dots around the input
for line in fileinput.input():
    row = ['.'] + list(line.strip()) + ['.']
    field.append(row)

dots = ['.' for x in field[0]]

field.insert(0, dots)
field.append(dots)

for row in field:
    for cell in row:
        print(cell, end='')
    print()

# look for numbers in the field and include them if they're
# adjacent to a symbol (= non-dot/non-numeric character)
row = 0
while row < len(field):
    column = 0
    while column < len(field[0]):
        cell = field[row][column]

        if cell.isnumeric():
            # get the rest of the number 
            # from column number_start to number_end
            number_start = column # inclusive start
            number_end = number_start + 1 # exclusive end
            number = cell

            while field[row][number_end].isnumeric():
                number += field[row][number_end]
                number_end += 1

            number = int(number)

            # check all around this number for a symbol
            # look one row above/below the current row 
            # and one column before/after the number start/end
            symbol_adjacent = False
            start_row = row - 1 # inclusive
            end_row = row + 2 # exclusive
            start_column = number_start - 1
            end_column = number_end + 1

            for i in range(start_row, end_row):
                for j in range(start_column, end_column):
                    cell = field[i][j]
                    if not cell == '.' and not cell.isnumeric():
                        symbol_adjacent = True

            print(f"found {number} at ({row}, {column}) / included in total: {symbol_adjacent}")
            
            if symbol_adjacent:
                sum += number

            # move past this whole number
            column = number_end
        else:
            column += 1

    row += 1

print(sum)