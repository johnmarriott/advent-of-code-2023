#!/usr/bin/env python

# this is slow

import fileinput
import re

mappings = {}
seed_ranges = []
item_names = [
    "seed",
    "soil",
    "fertilizer",
    "water",
    "light",
    "temperature",
    "humidity",
    "location"
]

def source_to_destination(source_name, source_id, destination_name) -> int:
    for mapping in mappings[f"{source_name}-to-{destination_name}"]:
        if source_id >= mapping["source_min_id"] and source_id <= mapping["source_max_id"]:
            destination_id = mapping["destination_min_id"] + (source_id - mapping["source_min_id"])
            return destination_id

    return source_id

for line in fileinput.input():

    # should be first line, get seed ids
    if line.startswith("seeds:"):
        seed_range_info = [int(x) for x in line.replace("seeds: ", "").split()]
        for i in range(0, len(seed_range_info), 2):
            seed_id_min = int(seed_range_info[i])
            seed_id_range = int(seed_range_info[i+1])
            seed_ranges.append({
                "seed_id_min": seed_id_min,
                "seed_id_range": seed_id_range
            })
        continue

    # new mapping just dropped
    if "map:" in line:
        source = re.sub("-to-.*", "", line).strip()
        destination = re.sub(".*-to-", "", line).replace(" map:", "").strip()
        mappings[f"{source}-to-{destination}"] = []
        continue

    # some digits to parse
    if re.match(r"\d", line):
        mapping_info = line.split(" ")
        mapping = {
            "source_min_id": int(mapping_info[1]),
            "source_max_id": int(mapping_info[1]) + int(mapping_info[2]),
            "destination_min_id": int(mapping_info[0])
        }

        mappings[f"{source}-to-{destination}"].append(mapping)

# grab the first seen location id as the starting min value
min_location_id = mappings["humidity-to-location"][0]["destination_min_id"]

for seed_range in seed_ranges:
    seed_id_min = seed_range["seed_id_min"]
    seed_id_range = seed_range["seed_id_range"]
    item_ids = {
        "seed": list(range(seed_id_min, seed_id_min + seed_id_range))
    }

    for seed_id in item_ids["seed"]:
        source_name = "seed"
        source_id = seed_id

        for destination_name in item_names[1:]:
            destination_id = source_to_destination(source_name, source_id, destination_name)
            source_name = destination_name
            source_id = destination_id

        # final destination id is the resulting location id
        if destination_id < min_location_id:
            min_location_id = destination_id

print(min_location_id)
