import fileinput

starfield = []
for line in fileinput.input():
    row = list(line.strip())
    starfield.append(row)

    # add new blank row now if this is all dots
    if len([x for x in row if x != '.']) == 0: # there aren't any non-dots
        starfield.append(row.copy()) # copy because we'll mutate this later

# find out which columns have all dots
all_dot_columns = []
for j in range(len(starfield[0])):
    all_dots = True
    for i in range(len(starfield)):
        if starfield[i][j] != '.':
            all_dots = False

    if all_dots:
        all_dot_columns.append(j)

# add an extra dot to all rows at the all-dot columns
# do this in reverse so the indices don't shift over
for column_to_expand in reversed(all_dot_columns):
    for row in starfield:
        row.insert(column_to_expand, '.')

for row in starfield:
    for cell in row:
        print(cell, end="")
    print()

galaxies = []
for i in range(len(starfield)):
    for j in range(len(starfield[i])):
        if starfield[i][j] == '#':
            galaxies.append([i, j])

print(f"\ngalaxies at: {galaxies}\n")

sum = 0
for i in range(len(galaxies)):
    for j in range(i + 1, len(galaxies)):
        manhattan_distance = abs(galaxies[i][0] - galaxies[j][0]) + abs(galaxies[i][1] - galaxies[j][1])
        print(f"from {galaxies[i]} to {galaxies[j]} is {manhattan_distance}")
        sum += manhattan_distance

print(sum)