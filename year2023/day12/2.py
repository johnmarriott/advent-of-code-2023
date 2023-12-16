#!/usr/bin/env python

import fileinput

# number of times to repeat input, it is 5 for the solution but lower values can help troubleshooting
MULTIPLICATION_FACTOR = 5

"""
in the given input there are at most 17 ? on one line
so brute force of trying each ? as #/. is prohibitive

part one of this turns into (49 choose 30) ~ 10^13 combinations
so we can't brute force that way either

instead try slotting them in from left to right
- find out min space that the remaining ones need = n_digits + sum(digits)
  this is if they were all neighbors with one dot between
- left to right, where can the current digit go?
    - need n digits of ? and #
    - next spot needs to be ? or .
    - if it fits then take the substring after n+1 digits (first n + the ?|. after)

do this plus memoization on previously-seen maps + lengths
"""

spring_map_counts_seen = {}

def count_valid_combinations(spring_map, spring_counts):
    spring_map_counts_key = f"{spring_map}_{','.join([str(x) for x in spring_counts])}"
    if spring_map_counts_key in spring_map_counts_seen:
        return spring_map_counts_seen[spring_map_counts_key]

    valid_combinations = 0

    first_spring_group_length = spring_counts[0]
    remaining_spring_counts = spring_counts[1:]

    # minimum space that the remaining springs need is their widths plus one gap
    # between them
    # e.g. [1, 3] shoved to the right of the line needs "#.###" at minimum
    min_space_for_remaining_springs = sum(remaining_spring_counts) + len(remaining_spring_counts) - 1

    # the maximum string that we could put just the first group into (the line minus
    # the characters in the space necessary to fit them)
    max_spring_map_for_first_spring_group = spring_map[:(len(spring_map) - min_space_for_remaining_springs)]

    if len(max_spring_map_for_first_spring_group) < first_spring_group_length:
        spring_map_counts_seen[spring_map_counts_key] = 0
        return 0
    
    # check if each possible spring-length slot in our buffer fits this group of springs
    for i in range(len(max_spring_map_for_first_spring_group) - first_spring_group_length + 1):
        # the map characters where a group this size might go
        candidate_spring_group = max_spring_map_for_first_spring_group[i:i + first_spring_group_length]
        # what's left in this map if we went with this candidate
        post_candidate_spring_map = max_spring_map_for_first_spring_group[i + first_spring_group_length:]

        if not '.' in candidate_spring_group: # there are enough #? to fit this
            # all spots to the left need to have been . or ?, otherwise we skipped a necessary spring
            spring_map_passed_over = max_spring_map_for_first_spring_group[:i]
            if len(spring_map_passed_over) > 0 and ('#' in spring_map_passed_over): 
                continue

            # if this was the last digit to fit in and there aren't springs remaining, yield one success
            if len(remaining_spring_counts) == 0:
                if not "#" in post_candidate_spring_map:
                    valid_combinations += 1
            else: # there are more to fit in the rest of the line
                # the spot after we put this group in the map
                next_spot = spring_map[i + first_spring_group_length:i + first_spring_group_length + 1]

                # the part of the map after this group and its buffer
                remaining_spring_map = spring_map[i + first_spring_group_length + 1:]

                if (next_spot == "." or next_spot == "?"): # the next spot isn't a spring
                    if len(remaining_spring_map) > 0: # there is some space left for the remaining groups 
                        valid_combinations += count_valid_combinations(remaining_spring_map, remaining_spring_counts)

    spring_map_counts_seen[spring_map_counts_key] = valid_combinations
    return valid_combinations

valid_combinations = []
for line in fileinput.input():
    springs_single = line.strip().split(' ')[0]
    counts_single = line.strip().split(' ')[1]

    springs_multiplied = '?'.join([springs_single] * MULTIPLICATION_FACTOR)
    counts_multiplied = ','.join([counts_single] * MULTIPLICATION_FACTOR)

    # set same variables from part 1 and proceed
    spring_map = springs_multiplied 
    spring_counts = [int(x) for x in counts_multiplied.split(',')]

    n_valid_combinations = count_valid_combinations(spring_map, spring_counts)
    valid_combinations.append(n_valid_combinations)
    print(f"{springs_multiplied} {counts_multiplied} -> {n_valid_combinations}")

print(sum(valid_combinations))
