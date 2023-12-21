#!/usr/bin/env python

import fileinput
from dataclasses import dataclass
from enum import Enum

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
# also used for nodes in the mapping with a 
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
            print(f"{self.label} -{value}-> {output_label}")
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
                print(f"{self.label} -{self.value}-> {output_label}")
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
            print(f"broadcaster -{pulse.value}-> {output_label}")
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

def press_button():
    """
    returns the number of low and high button presses 
    resulting from the button press
    """
    print("button -low-> broadcaster")
    queue: list[Pulse] = [Pulse(from_label="button", to_label="broadcaster", value=Value.LOW)]
    low_pulses = 0
    high_pulses = 0

    while len(queue) > 0:
        pulse = queue.pop(0)
        if pulse.value == Value.HIGH:
            high_pulses += 1
        else:
            low_pulses += 1

        network[pulse.to_label].receive(pulse=pulse, queue=queue)
    
    return low_pulses, high_pulses

total_high_pulses = 0
total_low_pulses = 0

for i in range(1000):
    print(f"\nAfter {i+1} button press{'es' if i > 0 else ''}:")    
    low, high = press_button()
    total_low_pulses += low
    total_high_pulses += high

print(total_low_pulses, total_high_pulses)
print(total_low_pulses * total_high_pulses)
