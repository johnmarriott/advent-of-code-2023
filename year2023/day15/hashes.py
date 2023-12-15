#!/usr/bin/env python

import fileinput
import re

def hash(string):
    value = 0
    for character in string:
        value += ord(character)
        value *= 17
        value = value % 256

    return value

def print_boxes(boxes): 
    for key in sorted(boxes.keys()):
        if len(boxes[key]) > 0:
            lenses = " ".join([f"[{lens['label']} {lens['focal_length']}]" for lens in boxes[key]])
            print(f"Box {key}: {lenses}")

for line in fileinput.input():
    inputs = line.strip().split(',')

# part one
hashes = [hash(input) for input in inputs]
print(hashes)
print(f"part one: {sum(hashes)}")

# part two
boxes = {}

for input in inputs:
    label = re.sub("[-=].*", "", input)
    operation = re.sub("[^-=]", "", input)
    focal_length = re.sub(".*[-=]", "", input)
    key = hash(label)

    lens = {
        "label": label,
        "focal_length": focal_length
    }

    if not key in boxes:
        boxes[key] = []

    box = boxes[key]

    if operation == "=":
        lens_with_same_label_index = next((i for i in range(len(box)) if box[i]["label"] == label), None)

        if lens_with_same_label_index is not None:
            box[lens_with_same_label_index] = lens
        else:
            box.append(lens)

    if operation == "-":
        lens_with_same_label_index = next((i for i in range(len(box)) if box[i]["label"] == label), None)

        if lens_with_same_label_index is not None:
            del box[lens_with_same_label_index]
    
    #print(f'\nAfter "{input}":')
    #print_boxes(boxes)

lens_values = []
for key, box in boxes.items():
    for i in range(len(box)):
        lens_values.append((key + 1) * (i + 1) * int(box[i]['focal_length']))

print(lens_values)
print(f"part two: {sum(lens_values)}")

