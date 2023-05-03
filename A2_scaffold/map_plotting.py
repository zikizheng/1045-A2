"""
This file is part of Assignment 2 of FIT1045, S1 2023.

It allows plotting an Itinerary as the picture of a map.

@file map_plotting.py
"""
from mpl_toolkits.basemap import Basemap #have to do 'pip install basemap'
import matplotlib.pyplot as plt
from itinerary import Itinerary
from city import City

def plot_itinerary(itinerary: Itinerary, projection = 'robin', line_width=2, colour='b') -> None:
    """
    Plots an itinerary on a map and writes it to a file.
    Ensures a size of at least 50 degrees in each direction.
    Ensures the cities are not on the edge of the map by padding by 5 degrees.
    The name of the file is map_city1_city2_city3_..._cityX.png.

    :param itinerary: The itinerary to plot.
    :param projection: The map projection to use.
    :param line_width: The width of the line to draw.
    :param colour: The colour of the line to draw.
    """

    # find the locations of the furthest cities in each direction
    minlon = None
    maxlon = None
    minlat = None
    maxlat = None
    for city in itinerary.cities:
        if not minlon or city.coordinates[1] < minlon:
            minlon = city.coordinates[1]
        if not maxlon or city.coordinates[1] > maxlon:
            maxlon = city.coordinates[1]
        if not minlat or city.coordinates[0] < minlat:
            minlat = city.coordinates[0]
        if not maxlat or city.coordinates[0] > maxlat:
            maxlat = city.coordinates[0]
    
    # add padding of 5 degrees
    minlon -= 5
    maxlon += 5
    minlat -= 5
    maxlat += 5

    # if necessary, extend the boundaries so that they span 50° of
    # longitude and latitude
    if maxlon-minlon < 50:
        extend = 50-(maxlon-minlon)
        minlon -= extend/2
        maxlon += extend/2
    if maxlat-minlat < 50:
        extend = 50-(maxlat-minlat)
        minlat -= extend/2
        maxlat += extend/2

    # make sure values are in range
    minlon = max(min(180, minlon), -180)
    maxlon = max(min(180, maxlon), -180)
    minlat = max(min(90, minlat), -90)
    maxlat = max(min(90, maxlat), -90)

    # create the map
    m = Basemap(projection=projection, lon_0=0, lat_0=0,
                llcrnrlon=minlon,llcrnrlat=minlat,urcrnrlon=maxlon,urcrnrlat=maxlat)

    # draw and colour it
    m.drawmapboundary(fill_color='aqua')
    m.fillcontinents(lake_color='aqua')
    m.drawcoastlines()

    # for each city n, draw a line on the map from city n-1 to city n
    for i in range(1, len(itinerary.cities)):
        city = itinerary.cities[i]
        prev = itinerary.cities[i-1]

        # plot with latlon=True takes latitude in argument one and
        # longitude in argument two. to draw a line between two points,
        # give a list containing the two latitudes followed by the two
        # longitudes.

        # the city stores its coordinate with latitudes in index 1 and
        # longitudes in index 0

        m.plot([city.coordinates[1], prev.coordinates[1]], [city.coordinates[0], prev.coordinates[0]],
               latlon=True, color=colour, linewidth=line_width)

    # save the figure to an appropriately named file
    plt.savefig("map_" + "_".join([city.name.lower() for city in itinerary.cities]) + ".png")

if __name__ == "__main__":
    # create some cities
    city_list = list()

    city_list.append(City("Melbourne", (-37.8136, 144.9631), "primary", 4529500, 1036533631))
    city_list.append(City("Sydney", (-33.8688, 151.2093), "primary", 4840600, 1036074917))
    city_list.append(City("Brisbane", (-27.4698, 153.0251), "primary", 2314000, 1036192929))
    city_list.append(City("Perth", (-31.9505, 115.8605), "1992000", 2039200, 1036178956))

    # plot itinerary
    plot_itinerary(Itinerary(city_list))
