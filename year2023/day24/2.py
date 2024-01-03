#!/usr/bin/env python

"""
The positions at time t for the first three sample hailstones are

(19 - 2t, 13 + t, 30 - 2t)
(18 - t, 19 - t, 22 - 2t)
(20 - 2t, 25 - 2t, 34 - 4t)

want to find px, py, pz and vx, vy, vz such that

    (px + vx t1, py + vy t1, pz + vz t1) == (19 - 2t1, 13 + t1, 30 - 2t1) 
    (px + vx t2, py + vy t2, pz + vz t2) == (18 - t2, 19 - t2, 22 - 2t2) 
    (px + vx t3, py + vy t3, pz + vz t3) == (20 - 2t3, 25 - 2t3, 34 - 4t3) 

for some positive integers t1, t2, and t3

These are nine variables and nine equations.  Use sympy to solve the system.  
The first three equations listed for the sample and full input work in my case
"""

import fileinput
from dataclasses import dataclass
from sympy.solvers import solve
from sympy import symbols

@dataclass
class Position:
    x: int
    y: int
    z: int

@dataclass
class Velocity:
    x: int
    y: int
    z: int

class Hailstone:
    position: Position
    velocity: Velocity

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def position_at_time(self, time):
        return (self.position.x + self.velocity.x * time, 
                self.position.y + self.velocity.y * time, 
                self.position.z + self.velocity.z * time)

hailstones: list[Hailstone] = []
for line in fileinput.input():
    parts = line.strip().split(" @ ")
    position_values = [int(x) for x in parts[0].split(", ")]
    velocity_values = [int(x) for x in parts[1].split(", ")]

    position = Position(x=position_values[0], y=position_values[1], z=position_values[2])
    velocity = Velocity(x=velocity_values[0], y=velocity_values[1], z=velocity_values[2])

    hailstones.append(Hailstone(position, velocity))

px, py, pz = symbols('px, py, pz')
vx, vy, vz = symbols('vx, vy, vz')
t1, t2, t3 = symbols('t1, t2, t3')

equations = (
    px + vx * t1 - (hailstones[0].position.x + hailstones[0].velocity.x * t1),
    py + vy * t1 - (hailstones[0].position.y + hailstones[0].velocity.y * t1),
    pz + vz * t1 - (hailstones[0].position.z + hailstones[0].velocity.z * t1),
    px + vx * t2 - (hailstones[1].position.x + hailstones[1].velocity.x * t2),
    py + vy * t2 - (hailstones[1].position.y + hailstones[1].velocity.y * t2),
    pz + vz * t2 - (hailstones[1].position.z + hailstones[1].velocity.z * t2),
    px + vx * t3 - (hailstones[2].position.x + hailstones[2].velocity.x * t3),
    py + vy * t3 - (hailstones[2].position.y + hailstones[2].velocity.y * t3),
    pz + vz * t3 - (hailstones[2].position.z + hailstones[2].velocity.z * t3)
)

solution = solve(equations, px, py, pz, vx, vy, vz, t1, t2, t3)

print(solution[0][0] + solution[0][1] + solution[0][2])