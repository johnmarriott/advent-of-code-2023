#!/usr/bin/env python

import fileinput
import pandas as pd
import re

item_ids = {}
mappings = {}

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
        item_ids["seed"] = [int(x) for x in line.replace("seeds: ", "").split()]
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

source_name = item_names[0]
for destination_name in item_names[1:]:
    destination_ids = []
    for source_id in item_ids[source_name]:
        destination_id = source_to_destination(source_name, source_id, destination_name)
        destination_ids.append(destination_id)

    item_ids[destination_name] = destination_ids
    source_name = destination_name

mapping_table = pd.DataFrame(item_ids)

print(mapping_table)
print(f"\nanswer: {mapping_table['location'].min()}")
