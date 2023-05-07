"""
This file is part of Assignment 2 of FIT1045, S1 2023.

It puts together all parts of the assignment.

@file onboard_navigation.py
"""
import vehicles
import country
import city
import path_finding
import csv_parsing
import map_plotting

if __name__ == "__main__":
	vehicle_list = vehicles.create_example_vehicles()
	match = ""
	matches = 0

	# allow the user to select a vehicle from the provided options
	print("Select a vehicle from the following:")
	while True:
		try:
			for i in range(len(vehicle_list)):
				print(f"{i}) {vehicle_list[i].__str__().split(' ')[0]}")

			inp = input("> ").strip().lower()
		except:
			print("\nInvalid input")
			continue

		if len(inp) == 0:
			continue

		try:
			# select by number
			inp_int = int(float(inp))
			if inp_int < 0 or inp_int >= len(vehicle_list):
				print("Integer out of range")
				continue
			match = vehicle_list[inp_int]
			break
		except:
			pass

		# select by string. only part of the desired option needs to be input. if the input matches
		# the first n characters of one option, that option will be selected. otherwise, if there
		# is more than one match, the user will have to select again
		matches = 0
		for n in vehicle_list:
			if inp == n.__str__().split(' ')[0][:len(inp)].lower():
				matches += 1
				match = n
		if matches == 1:
			break
		if matches > 1:
			print("Ambiguous input")
		print("No matches found. Try again")

	selected_vehicle = match
	print(f"Selected vehicle {selected_vehicle.__str__().split(' ')[0]}.")

	# parse the csv file containing the city data
	csv_parsing.create_cities_countries_from_csv("worldcities_truncated.csv")
	cities_set = 0
	cities = []

	# allow the user to select two cities
	print("Select two cities:")
	while True:
		try:
			inp = input("> ").strip().lower()
		except:
			print("\nInvalid input")
			continue

		if len(inp) == 0:
			continue

		# select by string. only part of the desired option needs to be input. if the input matches
		# the first n characters of one option, that option will be selected. otherwise, if there
		# is more than one match, the user will have to select again
		matches = 0
		for ctry in country.Country.name_to_countries.values():
			for city in ctry.cities:
				if inp == city.name[:len(inp)].lower():
					# the input matches the beginning of this city's name
					matches += 1
					match = city
		if matches == 1:
			cities_set += 1
			if cities_set == 2:
				print(f"Selected {match.name} as city 2.")
				cities.append(match)
				# both cities have been selected, now exit this loop
				break
			print(f"Selected {match.name} as city 1. Pick another")
			cities.append(match)
			continue
		if matches > 1:
			print(f"Ambiguous input ({matches} matches)")
			continue

		print("No matches found. Try again")

	# find the shortest path between the two cities, if there is one
	path = path_finding.find_shortest_path(selected_vehicle, cities[0], cities[1])
	if not path:
		print(f"There is no path between {cities[0].name} and {cities[1].name}")
		exit(0)

	# create a map and save it to an appropriately named file
	map_plotting.plot_itinerary(path)
