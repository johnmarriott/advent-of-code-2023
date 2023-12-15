import fileinput

def sequence_differences(sequence):
    """
    return a sequence of differences of a sequence
    e.g. [0 3 6 9 12] -> [3 3 3 3]
    """

    differences = []
    for i in range(1, len(sequence)):
        differences.append(sequence[i] - sequence[i - 1])
    
    return differences 

def next_value_of_sequence(sequence):
    differences = sequence_differences(sequence)

    # base case - differences of this list is all zeros
    if sum([abs(x) for x in differences]) == 0:
        # sequence is constant so return any element
        return sequence[0]
    
    # recursive case 
    return next_value_of_sequence(differences) + sequence[-1]

def previous_value_of_sequence(sequence):
    differences = sequence_differences(sequence)

    # base case - differences of this list is all zeros
    if sum([abs(x) for x in differences]) == 0:
        # sequence is constant so return any element
        return sequence[0]
    
    # recursive case 
    return sequence[0] - previous_value_of_sequence(differences)

next_values = []
previous_values = []
for line in fileinput.input():
    sequence = [int(x) for x in line.strip().split()]
    next_values.append(next_value_of_sequence(sequence))
    previous_values.append(previous_value_of_sequence(sequence))
    
print(f"part one: {sum(next_values)}")
print(f"part two: {sum(previous_values)}")