#!/usr/bin/env python

"""
In the sample, the rules applying to x are:

x>2440:R
x<1416:A
x>2662:A

Six values of x "matter": x in (2440, 2441) for the first comparison,
x in (1415, 1416) for the second, and x in (2662, 2663) for the third.
These turn into ranges [1, 1415] (any x value in this range is identical
in the function of this machine), [1415, 2440], [2441, 2662], and [2663, 4000]

We'll encode these ranges by inclusive start and exclusive end, so the x values
1416, 2441, 2663, and 4001 are the cutoff values needed.

Do the same for the other parts, and test every combination of representative
values for each part.  If one is accepted, the product of the parts' intervals
tested is the total number of parts accepted for this combination.

This takes a few hours and isn't the intended solution.  I think working backward
through the machine would be faster, plan to revisit this.
"""

import fileinput
import re
from dataclasses import dataclass
from enum import Enum

# set up ####

Comparison = Enum("Comparison", ["LESS_THAN", "GREATER_THAN"])

def unpack_rule(rule: str):
    rule_part = rule[0:1]
    rule_comparison = rule[1:2]
    rule_value = int(re.sub(r"[^\d]", "", rule))
    rule_destination = re.sub(r".*:", "", rule)

    return rule_part, rule_comparison, rule_value, rule_destination

class Rule:
    definition: str
    part_compared: str
    comparator: callable 
    destination: str

    def __init__(self, definition):
        self.definition = definition

        part, comparison, value, destination = unpack_rule(definition)
        self.part_compared = part
        self.destination =  destination

        if comparison == "<":
            self.comparator = lambda x: x < value
        else:
            self.comparator = lambda x: x > value

@dataclass
class Workflow:
    rules: list[Rule]
    default: str

workflows: dict[str, Workflow] = {}
parts: list[dict[str, int]] = []

part_names = ["x", "m", "a", "s"]

ACCEPTED = "A"
REJECTED = "R"

# parse input ####

for line in fileinput.input():
    if len(line.strip()) == 0:
        break

    workflow_key = re.sub(r"\{.*", "", line.strip())
    bracket_parts = re.sub(r".*\{(.*)\}", r"\1", line.strip()).split(",")
    default_destination = bracket_parts[-1]
    rule_definitions = bracket_parts[:-1]
    rules = [Rule(definition=rule_definition) for rule_definition in rule_definitions]

    workflows[workflow_key] = Workflow(
        rules = rules,
        default = default_destination
    )

cutoff_values = {key: [4001] for key in part_names}

for workflow in workflows.values():
    for rule in workflow.rules:
        part, comparison, value, destination = unpack_rule(rule.definition)
        
        if comparison == "<":
            cutoff_values[part].append(value)
        else: # greater than
            cutoff_values[part].append(value + 1)

for key in cutoff_values.keys():
    cutoff_values[key] = sorted(list(set(cutoff_values[key])))

ranges = {}
for key in part_names:
    lower_bound = 1
    ranges[key] = []
    for upper_bound in cutoff_values[key]:
        ranges[key].append([lower_bound, upper_bound])
        lower_bound = upper_bound

def part_accepted(part: dict[str, int]):
    """
    run this part through the workflow and return True for accepted, False for rejected
    """
    workflow_key = "in"

    while workflow_key != ACCEPTED and workflow_key != REJECTED:

        workflow = workflows[workflow_key]
        next_workflow_key = workflow.default

        for rule in workflow.rules:
            if rule.comparator(part[rule.part_compared]):
                next_workflow_key = rule.destination
                break

        workflow_key = next_workflow_key    

    return next_workflow_key == ACCEPTED

# test input combinations ####

parts_accepted = 0

for x in range(len(ranges["x"])):
    x_min = ranges["x"][x][0]
    x_max = ranges["x"][x][1]
    x_values = x_max - x_min

    print(f"starting [{x_min}, {x_max}) with {parts_accepted} so far")

    for m in range(len(ranges["m"])):
        m_min = ranges["m"][m][0]
        m_max = ranges["m"][m][1]
        m_values = m_max - m_min

        for a in range(len(ranges["a"])):
            a_min = ranges["a"][a][0]
            a_max = ranges["a"][a][1]
            a_values = a_max - a_min

            for s in range(len(ranges["s"])):
                s_min = ranges["s"][s][0]
                s_max = ranges["s"][s][1]
                s_values = s_max - s_min

                part = {
                    "x": x_min,
                    "m": m_min,
                    "a": a_min,
                    "s": s_min
                }

                if part_accepted(part):
                    parts_accepted += x_values * m_values * a_values * s_values

print(parts_accepted)