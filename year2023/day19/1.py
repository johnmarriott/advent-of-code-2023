#!/usr/bin/env python

import fileinput
import re
from dataclasses import dataclass
from enum import Enum

Comparison = Enum("Comparison", ["LESS_THAN", "GREATER_THAN"])

@dataclass
class Workflow:
    rules: list[str]
    default: str

workflows: dict[str, Workflow] = {}
parts: list[dict[str, int]] = []

ACCEPTED = "A"
REJECTED = "R"

finished_workflows = False
for line in fileinput.input():
    if len(line.strip()) == 0:
        finished_workflows = True
        continue

    if finished_workflows:
        line_parts = line.split(",")
        parts.append({
            "x": int(re.sub(r"[^\d]", "", line_parts[0])),
            "m": int(re.sub(r"[^\d]", "", line_parts[1])),
            "a": int(re.sub(r"[^\d]", "", line_parts[2])),
            "s": int(re.sub(r"[^\d]", "", line_parts[3]))
        })
        continue

    workflow_key = re.sub(r"\{.*", "", line.strip())
    bracket_parts = re.sub(r".*\{(.*)\}", r"\1", line.strip()).split(",")
    default_destination = bracket_parts[-1]
    workflows[workflow_key] = Workflow(
        rules = bracket_parts[:-1],
        default = default_destination
    )

accepted_part_sum = 0

for part in parts:
    print(f"{{x={part['x']},m={part['m']},a={part['a']},s={part['s']}}}: in", end="")
    workflow_key = "in"

    while workflow_key != ACCEPTED and workflow_key != REJECTED:

        workflow = workflows[workflow_key]
        next_workflow_key = workflow.default

        for rule in workflow.rules:
            rule_part = rule[0:1]
            rule_comparison = rule[1:2]
            rule_value = int(re.sub(r"[^\d]", "", rule))
            rule_destination = re.sub(r".*:", "", rule)

            if ((rule_comparison == "<" and part[rule_part] < rule_value)
                or (rule_comparison == ">" and part[rule_part] > rule_value)):
                    next_workflow_key = rule_destination
                    break

        print(f" -> {next_workflow_key}", end="")
        workflow_key = next_workflow_key    

    print()
    if next_workflow_key == ACCEPTED:
        accepted_part_sum += sum(part.values())

print()
print(accepted_part_sum)
