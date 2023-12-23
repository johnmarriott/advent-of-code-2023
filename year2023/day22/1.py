#!/usr/bin/env python

import fileinput
from dataclasses import dataclass

@dataclass
class Block:
    start_x: int
    start_y: int
    start_z: int
    end_x: int
    end_y: int
    end_z: int
    label: str

# read input and set up block space ####

def block_ranges(blocks):
    # all of the input coordinates are nonnegative 
    max_xy = max([max(block.start_x, block.end_x, block.start_y, block.start_y) for block in blocks])
    max_z = max([max(block.start_z, block.end_z) for block in blocks])
    return max_xy, max_z

def create_blocks():
    blocks: list[Block] = []

    # add blocks from input
    for line in fileinput.input():
        terminals = line.strip().split("~")
        start_x, start_y, start_z = terminals[0].split(",")
        end_x, end_y, end_z = terminals[1].split(",")

        blocks.append(Block(
            start_x=int(start_x), start_y=int(start_y), start_z=int(start_z),
            end_x=int(end_x), end_y=int(end_y), end_z=int(end_z),
            label=len(blocks) + 1 # line number of input
        ))
        
    # add a block for the floor
    max_xy, _ = block_ranges(blocks)
    floor = Block(start_x=0, start_y=0, start_z=0, end_x=max_xy, end_y=max_xy, end_z=0, label="F")
    blocks.append(floor)

    return blocks

def create_space(blocks: list[Block]):
    max_xy, max_z = block_ranges(blocks)
    # space is a grid represented by a 3d (x,y,z)-indexed list of pointers to blocks in these spots
    # do this the long way (instead of [None]*n) so that we don't have pointers to the same thing
    space = [[[None for _ in range(max_z + 1)] for _ in range(max_xy + 1)] for _ in range(max_xy + 1)]

    for block in blocks:
        for i in range(block.start_x, block.end_x + 1):
            for j in range(block.start_y, block.end_y + 1):
                for k in range(block.start_z, block.end_z + 1):
                    space[i][j][k] = block

    return space

blocks = create_blocks()
space = create_space(blocks)

# block/space helpers ####
        
def block_can_drop(block: Block, space: list[list[list[Block]]], missing_block: Block = None):
    """
    Return whether a block can drop in the given space.  If missing block is None:
    A block can drop if for each of its cubes, the cube below it in the space is
    empty or is currently occupied by this block.

    An optional missing_block can be provided, and if it is then we pretend that
    it is missing from the space when we check if this block can drop.  In this case,
    a block can drop if for each of its cubes, the cube below it in the space is
    empty, is currently occupied by this block, or is currently occupied by
    the missing block.
    """
    if block.start_z == 0: # this is the floor
        return False

    other_blocks_below = False
    for i in range(block.start_x, block.end_x + 1):
        for j in range(block.start_y, block.end_y + 1):
            for k in range(block.start_z, block.end_z + 1):
                if (space[i][j][k - 1] is not None and 
                    space[i][j][k - 1] != block and
                    (missing_block is None or space[i][j][k - 1] != missing_block)):
                    other_blocks_below = True

    return not other_blocks_below

def drop_block(block: Block, space: list[list[list[Block]]]):
    for i in range(block.start_x, block.end_x + 1):
        for j in range(block.start_y, block.end_y + 1):
            for k in range(block.start_z, block.end_z + 1):
                space[i][j][k] = None
                space[i][j][k-1] = block
    
    block.start_z -= 1
    block.end_z -= 1

def print_space(space: list[list[list[Block]]]):
    if len(space[0][0]) > 10:
        return

    for k in range(len(space[0][0])):
        print(f"z={k}", end="")
        if len(space) > 2:
            for i in range(len(space) - 2):
                print(" ", end="")
    print()

    for i in range(len(space)):
        for k in range(len(space[0][0])):
            for j in range(len(space[0])):
                if space[i][j][k] == None:
                    print("·", end="")
                else:
                    print(space[i][j][k].label, end="")
            print(" ", end="")
        print()

# let blocks naturally settle ####
        
print("\nsettle\n")

blocks_dropped_in_last_pass = True
while blocks_dropped_in_last_pass:
    print_space(space)
    blocks_dropped_in_last_pass = False

    for block in blocks:
        if block_can_drop(block, space):
            print(f"dropping {block}")
            drop_block(block, space)
            print(f"      to {block}")
            blocks_dropped_in_last_pass = True

# see which blocks could be disintegrated ####

print("\ndisintegrate\n")

print_space(space)
n_blocks_could_be_disintegrated = 0

for block in blocks:
    if block.start_z == 0:
        continue # don't disintegrate the floor

    candidate_can_be_disintegrated = True
    for other_block in blocks:
        if other_block != block:
            if block_can_drop(other_block, space, missing_block=block):
                candidate_can_be_disintegrated = False
    
    if candidate_can_be_disintegrated:
        print(f"could disintegrate {block.label}")
        n_blocks_could_be_disintegrated += 1

print(f"\n\n{n_blocks_could_be_disintegrated}")
