create table seed_to_soil (
	seed_id bigint primary key,
	soil_id bigint not null
);

create table soil_to_fertilizer (
	soil_id bigint primary key,
	fertilizer_id bigint not null
);

create table fertilizer_to_water (
	fertilizer_id bigint primary key,
	water_id bigint not null
);

create table water_to_light (
	water_id bigint primary key,
	light_id bigint not null
);

create table light_to_temperature (
	light_id bigint primary key,
	temperature_id bigint not null
);

create table temperature_to_humidity (
	temperature_id bigint primary key,
	humidity_id bigint not null
);

create table humidity_to_location (
	humidity_id bigint primary key,
	location_id bigint not null
);