#!/usr/bin/env python

import copy
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
        
def block_can_drop(block: Block, space: list[list[list[Block]]]):
    """
    Return whether a block can drop in the given space. 
    A block can drop if for each of its cubes, the cube below it in the space is
    empty or is currently occupied by this block.
    """
    if block.start_z == 0: # this is the floor
        return False

    other_blocks_below = False
    for i in range(block.start_x, block.end_x + 1):
        for j in range(block.start_y, block.end_y + 1):
            for k in range(block.start_z, block.end_z + 1):
                if space[i][j][k - 1] is not None and space[i][j][k - 1] != block:
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

def settle_blocks(blocks: list[Block], space) -> int: 
    """
    let blocks naturally fall and return the number of distinct blocks that fell
    """

    bricks_dropped = []

    blocks_dropped_in_last_pass = True
    while blocks_dropped_in_last_pass:
        print_space(space)
        blocks_dropped_in_last_pass = False

        for block in blocks:
            if block_can_drop(block, space):
                drop_block(block, space)
                blocks_dropped_in_last_pass = True
                bricks_dropped.append(block.label)

    return len(list(set(bricks_dropped)))

settle_blocks(blocks, space)

# test disintegrations ####

def how_many_blocks_will_drop_if_a_block_is_disintegrated(block_disintegrated: Block, space: list[list[list[Block]]]):
    space_without_block = copy.deepcopy(space)
    for i in range(block_disintegrated.start_x, block_disintegrated.end_x + 1):
        for j in range(block_disintegrated.start_y, block_disintegrated.end_y + 1):
            for k in range(block_disintegrated.start_z, block_disintegrated.end_z + 1):
                space_without_block[i][j][k] = None

    blocks_without_block = copy.deepcopy(blocks)
    blocks_without_block.remove(block_disintegrated)

    return settle_blocks(blocks_without_block, space_without_block)

print_space(space)
n_blocks_could_be_disintegrated = {}
for candidate_disintegration_block in blocks:
    if candidate_disintegration_block.start_z == 0:
        continue # don't disintegrate the floor

    print(f"trial disintegrating block {candidate_disintegration_block.label}")

    n_blocks_could_be_disintegrated[candidate_disintegration_block.label] = how_many_blocks_will_drop_if_a_block_is_disintegrated(candidate_disintegration_block, space)

print(f"\n\n{sum(list(n_blocks_could_be_disintegrated.values()))}")
