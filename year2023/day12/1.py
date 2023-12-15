#!/usr/bin/env python

import fileinput
import itertools
import re

"""
in the given input there are at most 17 ? on one line
so brute force of trying each ? as #/. is prohibitive

big idea: for each line, find
- how many ? there are = n_unknowns
- how many # are there = n_given_springs
- how many springs there are = n_springs

then we need to find homes for (n_springs - n_given_springs) = n_derelict_springs
among the n_unknown slots, and there are (n_unknown choose n_derelect) ways to 
put those derelect springs in those slots

e.g. for the line ?###???????? 3,2,1
there are 9 unknowns, 3 given, and 6 springs
so there are 3 derelict springs that can go into 9 places
there are (9 choose 3) = 84 arrangements to consider
instead of 2^9 = 512
"""

valid_combinations = []
for line in fileinput.input():
    print(line)
    n_valid_combinations = 0
    springs = line.strip().split(' ')[0]
    spring_counts = [int(x) for x in line.strip().split(' ')[1].split(',')]

    n_unknowns = len(re.sub(r"[^\?]", "", springs))
    n_given_springs = len(re.sub(r"[^#]", "", springs))
    n_springs = sum(spring_counts)
    n_derelict_springs = n_springs - n_given_springs

    unknown_indices = [] # where the ? are in the line
    for i in range(len(springs)):
        if springs[i] == "?":
            unknown_indices.append(i)

    for combination in itertools.combinations(unknown_indices, n_derelict_springs):
        test_springs = list(springs)

        # change all indices in this combination to springs
        for unknown_index in combination:
            test_springs[unknown_index] = '#'

        # change all other unknowns to dots, it's all # and . now
        test_springs = ['.' if x == '?' else x for x in test_springs]

        # turn this list back into a string with dots in start/end trimmed off
        test_spring_string = ''.join(test_springs)

        # get counts of groups of # characters
        # throw out leading/trailing dots to avoid empty strings in split
        test_spring_counts = [len(x) for x in re.split(r"\.+", test_spring_string.strip('.'))]

        if test_spring_counts == spring_counts:
            print(test_spring_string)
            n_valid_combinations += 1

    print(f"{n_valid_combinations}\n\n")
    valid_combinations.append(n_valid_combinations)

print(sum(valid_combinations))
    