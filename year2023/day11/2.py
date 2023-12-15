import fileinput

GALACTIC_EXPANSION = 2

# detect galaxies now, and make the starmap all 1s for the distance to traverse this node
starfield = []
galaxies = []
i = 0
for line in fileinput.input():
    for j in range(len(line)):
        if line[j] == '#':
            galaxies.append([i, j])
    row = [1 for x in line.strip()]
    starfield.append(row)
    i += 1

print(f"\npre-expansion galaxies at: {galaxies}\n")

galaxy_rows = [galaxy[0] for galaxy in galaxies]
galaxy_columns = [galaxy[1] for galaxy in galaxies]

for i in range(len(starfield)):
    for j in range(len(starfield[i])):
        # if this row or column doesn't contain a galaxy, expand this node
        if (not (i in galaxy_rows)) or (not (j in galaxy_columns)):
            starfield[i][j] = GALACTIC_EXPANSION

for row in starfield:
    print(row)

sum = 0
for a in range(len(galaxies)):
    for b in range(a + 1, len(galaxies)):
        # traverse from galaxy a to galaxy b
        galactic_distance = 0

        # start at the coordinates of galaxy a
        i = galaxies[a][0]
        j = galaxies[a][1]

        # move down until the row of galaxy b
        # can always move down because of the galaxy ordering
        while i != galaxies[b][0]:
            i += 1
            galactic_distance += starfield[i][j]

        # move sideways until the column of galaxy b
        # figure out left/right from their coordinates
        if galaxies[a][1] != galaxies[b][1]:
            direction = int((galaxies[b][1] - galaxies[a][1]) / abs(galaxies[b][1] - galaxies[a][1]))
            while j != galaxies[b][1]:
                j += direction
                galactic_distance += starfield[i][j]
        
        print(f"from {galaxies[a]} to {galaxies[b]} is {galactic_distance}")
        sum += galactic_distance

print(sum)