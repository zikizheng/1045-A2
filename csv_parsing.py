"""
This file is part of Assignment 2 of FIT1045, S1 2023.

It contains a parser that reads a CSV file and creates instances 
of the class City and the class Country.

@file city_country_csv_reader.py
"""
import csv
from city import City
from country import *

def create_cities_countries_from_csv(path_to_csv: str) -> None:
	"""
	Reads a CSV file given its path and creates instances of City and Country for each line.

	:param path_to_csv: The path to the CSV file.
	"""
	file = open(path_to_csv, encoding="utf8")

	# create a reader to read in the csv file into a dictionary
	reader = csv.DictReader(file)
	for line in reader:
		# compose a city from the fields in the csv file and add it to the corresponding country
		add_city_to_country(
			City(
				line["city_ascii"], # ascii representation of city's name
				(float(line["lat"]), float(line["lng"])), # coordinates (latitude, longitude) as float
				line["capital"], # whether or not city is a capital
				int(line["population"]) if line["population"] else 0, # population of city as integer
				int(line["id"]) # city id as an integer
				),
			line["country"], line["iso3"]) # name and code of country

if __name__ == "__main__":
    create_cities_countries_from_csv("worldcities_truncated.csv")
    for country in Country.name_to_countries.values():
        country.print_cities()
