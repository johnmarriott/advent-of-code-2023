#!/usr/bin/env python

# assume pgsql db named advent with user postgres/postgres and schema.sql is there

# this isn't faster than the python version

import fileinput
import pandas as pd
import re
import psycopg2

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

conn = psycopg2.connect(
    database="advent", 
    host="localhost",
    user="postgres",
    password="postgres",
    port="5432"
)
conn.autocommit = True
db = conn.cursor()

# truncate each table
source_name = item_names[0]
for destination_name in item_names[1:]:
    sql = f"truncate table {source_name}_to_{destination_name}"
    db.execute(sql)
    source_name = destination_name

seed_ids = []
for line in fileinput.input():

    # should be first line, get seed ids
    if line.startswith("seeds:"):
        seed_ids = line.replace("seeds: ", "").split()
        continue

    # new mapping just dropped
    if "map:" in line:
        source = re.sub("-to-.*", "", line).strip()
        destination = re.sub(".*-to-", "", line).replace(" map:", "").strip()
        continue

    # some digits to parse
    if re.match(r"\d", line):
        mapping_info = line.split(" ")
        source_min_id = int(mapping_info[1])
        destination_min_id = int(mapping_info[0])
        id_range = int(mapping_info[2])

        sql = f"""
            insert into {source}_to_{destination} ({source}_id, {destination}_id)
            select
                {source_min_id} + i,
                {destination_min_id} + i
            from generate_series(0, {id_range - 1}) as t(i)
        """
        db.execute(sql)

seed_ids_paren_string = "(" + "), (".join(seed_ids) + ")"
sql = f"""
with seed_ids (seed_id) as (
	values {seed_ids_paren_string}
),
soil_ids as (
	select
		coalesce(seed_to_soil.soil_id, seed_ids.seed_id) as soil_id
	from seed_ids
		left join seed_to_soil on seed_ids.seed_id = seed_to_soil.seed_id
),
fertilizer_ids as (
	select
		coalesce(soil_to_fertilizer.fertilizer_id, soil_ids.soil_id) as fertilizer_id
	from soil_ids
	  left join soil_to_fertilizer on soil_ids.soil_id = soil_to_fertilizer.soil_id
),
water_ids as (
	select
		coalesce(fertilizer_to_water.water_id, fertilizer_ids.fertilizer_id) as water_id
	from fertilizer_ids
	  left join fertilizer_to_water on fertilizer_ids.fertilizer_id = fertilizer_to_water.fertilizer_id
),
light_ids as (
	select
		coalesce(water_to_light.light_id, water_ids.water_id) as light_id
	from water_ids
	  left join water_to_light on water_ids.water_id = water_to_light.water_id
),
temperature_ids as (
	select
		coalesce(light_to_temperature.temperature_id, light_ids.light_id) as temperature_id
	from light_ids
	  left join light_to_temperature on light_ids.light_id = light_to_temperature.light_id
),
humidity_ids as (
	select
		coalesce(temperature_to_humidity.humidity_id, temperature_ids.temperature_id) as humidity_id
	from temperature_ids
	  left join temperature_to_humidity on temperature_ids.temperature_id = temperature_to_humidity.temperature_id
),
location_ids as (
	select
		coalesce(humidity_to_location.location_id, humidity_ids.humidity_id) as location_id
	from humidity_ids
	  left join humidity_to_location on humidity_ids.humidity_id = humidity_to_location.humidity_id
)
select
	min(location_id) as min_location_id
from location_ids
"""

db.execute(sql)
result = db.fetchone()
print(result[0])