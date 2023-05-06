"""
This file is part of Assignment 2 of FIT1045, S1 2023.

It contains a function to create a path, encoded as an Itinerary, that is shortest for some Vehicle.

@file path_finding.py
"""
import math
import networkx

from country import find_country_of_city
from city import City, get_city_by_id
from itinerary import Itinerary
from vehicles import Vehicle, create_example_vehicles
from csv_parsing import create_cities_countries_from_csv

graphs = {}
    
def find_shortest_path(vehicle: Vehicle, from_city: City, to_city: City) -> Itinerary | None:
    """
    Returns a shortest path between two cities for a given vehicle as an Itinerary,
    or None if there is no path.

    :param vehicle: The vehicle to use.
    :param from_city: The departure city.
    :param to_city: The arrival city.
    :return: A shortest path from departure to arrival, or None if there is none.
    """
    #TODO
    if vehicle not in graphs:
        graph = networkx.Graph()
        cityList = City.id_to_cities.values()
        for city in cityList:
            graph.add_node(city, type=city.city_type)
        for a, cityA in enumerate(cityList):
            for b, cityB in enumerate(cityList, start = a+1):
                if str(vehicle).split()[0] == "CrappyCrepeCar":
                    graph.add_edge(cityA, cityB, time = vehicle.compute_travel_time(cityA, cityB))
                elif (str(vehicle).split()[0] == "DiplomacyDonutDinghy" and 
                     (cityA.city_type == cityB.city_type == "primary" or
                     find_country_of_city(cityA) == find_country_of_city(cityB))):
                    graph.add_edge(cityA, cityB, time = vehicle.compute_travel_time(cityA, cityB))
                elif (str(vehicle).split()[0] == "TeleportingTarteTrolley" and
                     (cityA.distance(cityB) <= vehicle.max_distance)):
                     graph.add_edge(cityA, cityB, time = vehicle.compute_travel_time(cityA, cityB))
        graphs[vehicle] = graph
    try:
        return Itinerary(networkx.shortest_path(graphs[vehicle], from_city, to_city, "time"))
    except:
        return None

if __name__ == "__main__":
    create_cities_countries_from_csv("worldcities_truncated.csv")
    vehicles = create_example_vehicles()

    from_cities = set()
    for city_id in [1036533631, 1036142029, 1458988644]:
        from_cities.add(get_city_by_id(city_id))
    #we create some vehicles
    vehicles = create_example_vehicles()
    
    to_cities = set(from_cities)
    for from_city in from_cities:
        to_cities -= {from_city}
        for to_city in to_cities:
            print(f"{from_city} to {to_city}:")
            for test_vehicle in vehicles:
                shortest_path = find_shortest_path(test_vehicle, from_city, to_city)
                print(f"\t{test_vehicle.compute_itinerary_time(shortest_path)}"
                    f" hours with {test_vehicle} with path {shortest_path}.")