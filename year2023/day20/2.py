#!/usr/bin/env python

"""
This solution is customized to my input.  Could replace the lines around
    nodes_going_to_lg = ["ls", "nb", "vc", "vg"]
with a lookup in the network of which nodes go the the predecessor of rx

rx comes from &lg

Running pulses for a while to wait for lg to send a low didn't work.

lg is a conjunction of:
  &vg
  &nb
  &vc
  &ls

lg will send a low pulse if all four of these are high

Track the number of button presses it takes to get each of these to 
send a high pulse.  If this sequence is periodic for each of these four
separately, then we can see when all four line up.  Look for:
- at least two values for each of these
- the second value found for each node to be a multiple of the first
  - if so, the least common multiple of the four first values is probably the solution
  - if not, another approach is needed.  Not needed, it turns out that for the 
    given this way works :)

"""

import fileinput
from dataclasses import dataclass
from enum import Enum
from functools import reduce
from operator import mul

class Value(Enum):
    LOW = False
    HIGH = True

    def __str__(self):
        if self == Value.LOW:
            return "low"
        return "high"

# a pulse active in the network
@dataclass
class Pulse:
    from_label: str
    to_label: str
    value: bool

# superclass for conjunction/flipflop nodes in the network
# also used for nodes in the mapping with a no operation
class Node:
    label: str

    def __init__(self, label: str):
        self.label = label

    def receive(self, pulse: Pulse, queue: list[dict[str, bool]]):
        pass

class Conjunction(Node):
    inputs: dict[str, Value]
    output_label: list[str]

    def __init__(self, label, output_labels):
        super().__init__(label=label)
        self.inputs = {} # these get added after initialization
        self.output_labels = output_labels

    def __str__(self):
        return f"Conjunction {self.input_labels} : {self.input_values} → {self.output_labels}"

    def add_input(self, input_label):
        self.inputs[input_label] = Value.LOW

    def receive(self, pulse: Pulse, queue: list[dict[str, bool]]):
        self.inputs[pulse.from_label] = pulse.value

        # emit low if all inputs are high, else emit high
        input_values = list(self.inputs.values())
        if input_values.count(Value.HIGH) == len(input_values): 
            value = Value.LOW
        else:
            value = Value.HIGH

        for output_label in self.output_labels:
            queue.append(Pulse(from_label=self.label, to_label=output_label, value=value))

class FlipFlop(Node):
    value: bool 
    output_labels: str

    def __init__(self, label, output_labels):
        super().__init__(label=label)
        self.value = Value.LOW
        self.output_labels = output_labels

    def __str__(self):
        return f"FlipFlop {self.value} → {self.output_labels}"

    def receive(self, pulse: Pulse, queue: list[dict[str, bool]]):
        if pulse.value == Value.HIGH:
            pass # do nothing if receive high
        else:
            if self.value == Value.LOW:
                self.value = Value.HIGH
            else:
                self.value = Value.LOW

            for output_label in self.output_labels:
                queue.append(Pulse(from_label=self.label, to_label=output_label, value=self.value))

class Broadcaster(Node):
    output_labels: list[str]

    def __init__(self, output_labels):
        super().__init__(label="broadcaster")
        self.output_labels = output_labels

    def __str__(self):
        return f"→ {self.output_labels}"

    def receive(self, pulse: Pulse, queue: list[dict[str, bool]]):
        for output_label in self.output_labels:
            queue.append(Pulse(from_label=self.label, to_label=output_label, value=pulse.value))

network: dict[str, Node] = {}
lines = [line.strip() for line in fileinput.input()]

# track connections so that we can set conjunction inputs 
# and nodes that are just a destination after the first pass
connections = []

for line in lines:
    line_parts = line.split(" -> ")
    outputs = line_parts[1].split(', ')
    label = "broadcaster"

    if line_parts[0] == "broadcaster":
        network[label] = Broadcaster(output_labels=outputs)
    else:
        label = line_parts[0][1:]

        if line_parts[0][0] == "%":
            network[label] = FlipFlop(label=label, output_labels=outputs)
        else: # must be conjunction
            network[label] = Conjunction(label=label, output_labels=outputs)
        
    for output_label in outputs:
        connections.append({"from": label, "to": output_label})

for connection in connections:
    # add an input-only node not seen in the first sweep
    if not connection["to"] in network:
        network[connection["to"]] = Node(connection["to"])

    # add incoming connections to conjunctions created in the first sweep
    if isinstance(network[connection["to"]], Conjunction):
        network[connection["to"]].add_input(connection["from"])

def press_button(nodes_to_lg_high_at: dict[str, list[int]], n: int):
    queue: list[Pulse] = [Pulse(from_label="button", to_label="broadcaster", value=Value.LOW)]

    while len(queue) > 0:
        pulse = queue.pop(0)

        if pulse.to_label == "lg" and pulse.value == Value.HIGH:
            nodes_to_lg_high_at[pulse.from_label].append(n)

        network[pulse.to_label].receive(pulse=pulse, queue=queue)

nodes_going_to_lg = ["ls", "nb", "vc", "vg"]
nodes_to_lg_high_at = {node: [] for node in nodes_going_to_lg}
n = 0

while True:
    n += 1

    # do we have at least two possible cycle values for each of the nodes going to g?
    if all([len(nodes_to_lg_high_at[node]) > 1 for node in nodes_going_to_lg]):
        if all([nodes_to_lg_high_at[node][1] % nodes_to_lg_high_at[node][0] == 0 for node in nodes_going_to_lg]):
            break

    press_button(nodes_to_lg_high_at, n)

cycle_values = [nodes_to_lg_high_at[node][0] for node in nodes_going_to_lg]


print(cycle_values)
print(reduce(mul, cycle_values, 1))