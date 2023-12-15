import fileinput

field = []
gear_adjacent_numbers = {}

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

            # check all around this number for a gear
            # look one row above/below the current row 
            # and one column before/after the number start/end
            start_row = row - 1 # inclusive
            end_row = row + 2 # exclusive
            start_column = number_start - 1
            end_column = number_end + 1

            for i in range(start_row, end_row):
                for j in range(start_column, end_column):
                    cell = field[i][j]
                    if cell == "*":
                        if f"{i},{j}" in gear_adjacent_numbers:
                            gear_adjacent_numbers[f"{i},{j}"].append(number)
                        else:
                            gear_adjacent_numbers[f"{i},{j}"] = [number]
                        print(f"{number} is adjacent to a gear at {i},{j}")
            
            # move past this whole number
            column = number_end
        else:
            column += 1

    row += 1

gear_ratios = [x[0] * x[1] for x in gear_adjacent_numbers.values() if len(x) == 2]
print(gear_ratios)
print(sum(gear_ratios))
