#!/usr/bin/env python

import fileinput
import itertools
import numpy as np
from dataclasses import dataclass

MIN_XY = 200000000000000
MAX_XY = 400000000000000

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

    def xy_intersection_times(self, other: "Hailstone"):
        """
        Find the respective times that the two hailstones' xy-lines intersect at,
        regardless of z, if any.  Returns the two times at which the two lines are
        at the same point if the intersection exists, None if it doesn't exist.
        """

        # example:
        # Hailstone A: 19, 13, 30 @ -2, 1, -2
        # Hailstone B: 18, 19, 22 @ -1, -1, -2

        # equations are x: 19 - 2t = 18 - s and y: 13 + t = 19 - s
        # which group, x: -2t - (-1s) = (19-18), y: 1t - (-1s) = 13 - 19
        # together this is [[-2, -1], [1, -1]] * [[t],[s]] == [[13],[-19]]

        A = np.array([[self.velocity.x, -other.velocity.x],
                      [self.velocity.y, -other.velocity.y]])
        b = np.array([-self.position.x + other.position.x, 
                      -self.position.y + other.position.y])
        try:
            return np.linalg.solve(A, b)
        except np.linalg.LinAlgError as error:
            if str(error) == "Singular matrix":
                return None
            else:
                raise error

hailstones: list[Hailstone] = []
for line in fileinput.input():
    parts = line.strip().split(" @ ")
    position_values = [int(x) for x in parts[0].split(", ")]
    velocity_values = [int(x) for x in parts[1].split(", ")]

    position = Position(x=position_values[0], y=position_values[1], z=position_values[2])
    velocity = Velocity(x=velocity_values[0], y=velocity_values[1], z=velocity_values[2])

    hailstones.append(Hailstone(position, velocity))

intersections = 0

for i, j in itertools.product(list(range(len(hailstones))), list(range(len(hailstones)))):
    if j <= i:
        continue

    intersection_times = hailstones[i].xy_intersection_times(hailstones[j])

    if intersection_times is not None:
        intersection_position = hailstones[i].position_at_time(intersection_times[0])
        if (intersection_times[0] > 0 and
            intersection_times[1] > 0 and
            intersection_position[0] >= MIN_XY and
            intersection_position[0] <= MAX_XY and
            intersection_position[1] >= MIN_XY and
            intersection_position[1] <= MAX_XY):
            intersections += 1

print(intersections)
