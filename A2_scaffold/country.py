"""
This file is part of Assignment 2 of FIT1045, S1 2023.

It contains the class Country.

@file country.py
"""
from tabulate import tabulate
from city import City, create_example_cities

class Country():
    """
    Represents a country.
    """

    name_to_countries = dict() # a dict that associates country names to instances.

    def __init__(self, name: str, iso3: str) -> None:
        """
        Creates an instance with a country name and a country ISO code with 3 characters.

        :param country_name: The name of the country
        :param country_iso3: The unique 3-letter identifier of this country
	    :return: None
        """
        #initialize class variables
        self.name = name
        self.iso3 = iso3
        self.cities = {}

        #add {name: self} to name_to_countries
        Country.name_to_countries[name] = self

    def add_city(self, city: City) -> None:
        """
        Adds a city to the country.

        :param city: The city to add to this country
        :return: None
        """
        #add a city to cities dict
        self.cities[city] = city.city_type

    def get_cities(self, city_type: list[str] = None) -> list[City]:
        """
        Returns a list of cities of this country.

        The argument city_type can be given to specify a subset of
        the city types that must be returned.
        Cities that do not correspond to these city types are not returned.
        If None is given, all cities are returned.

        :param city_type: None, or a list of strings, each of which describes the type of city.
        :return: a list of cities in this country that have the specified city types.
        """
        #if there is city_type parameter, return all keys in cities dict that have a value that is in city_type
        #else return list of keys in cities dict
        if city_type:
            return [x for x in self.cities if self.cities[x] in city_type]
        else:
            return list(self.cities.keys())

    def print_cities(self) -> None:
        """
        Prints a table of the cities in the country, from most populous at the top
        to least populous. Use the tabulate module to print the table, with row headers:
        "Order", "Name", "Coordinates", "City type", "Population", "City ID".
        Order should start at 0 for the most populous city, and increase by 1 for each city.
        """
        #create sorted list of based on population size
        cities = sorted([x.get_table_data() for x in list(self.cities.keys())], key = lambda x : int(x[3]), reverse=True)

        #insert ranking in the front of each city in cities list
        for i in range(len(cities)):
            cities[i].insert(0, i)

        #insert row headers in front of cities list
        cities.insert(0, ["Order", "Name", "Coordinates", "City type", "Population", "City ID"])

        #print title of table
        print(f'Cities of {self}')
        #print tabluated cities list
        print(tabulate(cities, numalign='left'))

    def __str__(self) -> str:
        """
        Returns the name of the country.
        """
        return self.name


def add_city_to_country(city: City, country_name: str, country_iso3: str) -> None:
    """
    Adds a City to a country.
    If the country does not exist, create it.

    :param country_name: The name of the country
    :param country_iso3: The unique 3-letter identifier of this country
    :return: None
    """
    #check if country_name is in name_to_countries dict and the country.iso3 == country_iso3
    #if it is, then add city to country
    if country_name in Country.name_to_countries and Country.name_to_countries[country_name].iso3 == country_iso3:
        Country.name_to_countries[country_name].add_city(city)
    #else create new country object and add city
    else:
        Country(country_name, country_iso3).add_city(city)


def find_country_of_city(city: City) -> Country:
    """
    Returns the Country this city belongs to.
    We assume there is exactly one country containing this city.

    :param city: The city.
    :return: The country where the city is.
    """
    #loop over every country in name_to_countries and check if city is in the country's cities dict
    #if it is, return the country
    for country in Country.name_to_countries:
        if city in Country.name_to_countries[country].cities:
            return Country.name_to_countries[country]

def create_example_countries() -> None:
    """
    Creates a few countries for testing purposes.
    Adds some cities to it.
    """
    create_example_cities()
    malaysia = Country("Malaysia", "MAS")
    kuala_lumpur = City.name_to_cities["Kuala Lumpur"][0]
    malaysia.add_city(kuala_lumpur)

    for city_name in ["Melbourne", "Canberra", "Sydney"]:
        add_city_to_country(City.name_to_cities[city_name][0], "Australia", "AUS")

def test_example_countries() -> None:
    """
    Assuming the correct countries have been created, runs a small test.
    """
    Country.name_to_countries["Australia"].print_cities()


if __name__ == "__main__":
    create_example_countries()
    test_example_countries()
    
