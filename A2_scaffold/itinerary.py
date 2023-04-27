"""
This file is part of Assignment 2 of FIT1045, S1 2023.

It contains the class Itinerary.

@file itinerary.py
"""
import math
from city import City, create_example_cities, get_cities_by_name

class Itinerary():
    """
    A sequence of cities.
    """

    def __init__(self, cities: list[City]) -> None:
        """
        Creates an itinerary with the provided sequence of cities,
        conserving order.
        :param cities: a sequence of cities, possibly empty.
        :return: None
        """
        self.cities = cities[:]

    def total_distance(self) -> int:
        """
        Returns the total distance (in km) of the itinerary, which is
        the sum of the distances between successive cities.
        :return: the total distance.
        """
        # initialise result to 0
        res = 0
        # skipping the first city, for each city n add to the resilt
        # the distance between n and n-1
        for i in range(1, len(self.cities)):
            res += self.cities[i].distance(self.cities[i-1])
        return res

    def append_city(self, city: City) -> None:
        """
        Adds a city at the end of the sequence of cities to visit.
        :param city: the city to append
        :return: None.
        """
        self.cities.append(city)

    def min_distance_insert_city(self, city: City) -> None:
        """
        Inserts a city in the itinerary so that the resulting
        total distance of the itinerary is minimised.
        :param city: the city to insert
        :return: None.
        """
        # there are no cities. simply append it to the list.
        if len(self.cities) == 0:
            self.cities.append(city)
            return

        # to minimise the distance of the itinerary following the
        # insertion of the city, the change in total distance before
        # and after the insertion will be found for each position.
        # the position which corresponds to the minimum change in distance
        # will be the position which results in the lowest total distance
        # following the insertion.

        # begin by considering the case of inserting the city before index
        # 0, i.e inserting it at the beginning of the list. the change in
        # distance is simply the distance from the inserted city to the
        # first city in the list.
        distance_change = city.distance(self.cities[0])

        # initialise the minimum to this first value
        min = (0, distance_change)

        # now, consider each value in the middle of the list. the process
        # of inserting the city before an element n (not the first or last
        # element) can be broken down into three steps:
        # 1. subtract the distance between n and n-1
        # 2. add the distance between the inserted city and city n-1
        # 3. add the distance between the inserted city and city n
        # so the change can be expressed as 
        #       distance(city, cities[n-1]) + distance(city, cities[n]) - distance(cities[n], cities[n-1])

        for i in range(1, len(self.cities)-1):
            distance_change = city.distance(self.cities[i-1]) + city.distance(self.cities[i]) - self.cities[i].distance(self.cities[i-1])
            if distance_change < min[1]:
                min = (i, distance_change)

        # finally, consider appending the city to the end of the list.
        # similarly to inserting it at the beginning, the change in
        # distance when appending to the end is simply the distance
        # between the final city in the list and the city to be inserted

        distance_change = city.distance(self.cities[-1])
        if distance_change < min[1]:
            min = (-1, distance_change)

        self.cities.insert(min[0], city)

    def __str__(self) -> str:
        """
        Returns the sequence of cities and the distance in parentheses
        For example, "Melbourne -> Kuala Lumpur (6368 km)"

        :return: a string representing the itinerary.
        """
        result = ""
        distance_sum = 0
        first = True
        for city in self.cities:
            if first:
                first = False
            else:
                result += "-> "
            result += f"{city.name} "
            prev = city
        result += f"({self.total_distance()} km)"
        return result

if __name__ == "__main__":
    create_example_cities()
    test_itin = Itinerary([get_cities_by_name("Melbourne")[0],
                           get_cities_by_name("Kuala Lumpur")[0]])
    print(test_itin)

    #we try adding a city
    test_itin.append_city(get_cities_by_name("Baoding")[0])
    print(test_itin)

    #we try inserting a city
    test_itin.min_distance_insert_city(get_cities_by_name("Sydney")[0])
    print(test_itin)

    #we try inserting another city
    test_itin.min_distance_insert_city(get_cities_by_name("Canberra")[0])
    print(test_itin)
