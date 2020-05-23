# -*- coding: utf-8 -*-
"""
Created on Sat May 23 10:52:58 2020

@author: 10624
"""
"""
This file is to initialize the environment and specify the base map
"""

import os
os.environ['PROJ_LIB'] = r'E:\Anaconda\pkgs\proj4-5.2.0-ha925a31_1\Library\share' #For laptop
#For desktop os.environ['PROJ_LIB'] = r'C:\Users\wany105\AppData\Local\Continuum\anaconda3\pkgs\proj4-5.2.0-ha925a31_1\Library\share'

from mpl_toolkits.basemap import Basemap ##Basemap package is used for creating geography map
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from matplotlib import pyplot as plt
import math
import csv

##Color Setting, different value on the map will have different color
def custom_div_cmap(numcolors, mincol, midlowcol, midcol, midhighcol, maxcol):
    from matplotlib.colors import LinearSegmentedColormap

    cmap = LinearSegmentedColormap.from_list(numcolors, colors = [mincol, midlowcol, midcol, midhighcol, maxcol], N = numcolors)

    return cmap
cmap = colors.ListedColormap(['darkblue', 'mediumblue', 'skyblue', 'lightgray', 'khaki', 'yellow', 'orange', 'coral', 'orangered', 'red', 'darkred', 'maroon'])
bounds=[3, 15, 27, 31, 2174, 4318, 6462, 8606, 10750, 12893, 17181, 21469] ##Need to be adjusted to different value
norm = colors.BoundaryNorm(bounds, cmap.N)


# Open the population data file and make sure it is in the same folder with current program file
# The file can be found on the website: https://daac.ornl.gov/ISLSCP_II/guides/global_population_xdeg.html (Population density, population and area of each area)
filename = 'people_count_1995.asc' #Population map, not density!
with open(filename) as f:
    reader = csv.reader(f)
    line_count = 0
    Title = []
    #Set up the grid and split the whole map into small squares: Latitude, 90*2*4; longitude: 180*2*4.
    #PD: Population Count of each small square area.
    PD = np.zeros([720, 1440]) 
    for row in reader:
        if(line_count <= 5):
            Title.append(row)
            line_count += 1
        else:
            Temp = row[0].split()
            temp2 = 0
            for temp in Temp:
                if((float(temp) == -88) or (float(temp) == -99)):
                    PD[719 - (line_count - 6)][temp2] = 0
                else:
                    PD[719 - (line_count - 6)][temp2] = temp
                temp2 += 1
            line_count += 1

#Basemap
def BaseMapSet(Type, llon, rlon, llat, rlat):
    plt.figure(figsize = (12, 12))
    if(Type == 'local'):
        Base = Basemap(projection = 'merc', resolution = 'l', area_thresh = 1000.0, lat_0=0, lon_0=0, llcrnrlon=llon, llcrnrlat=llat, urcrnrlon=rlon, urcrnrlat=rlat)
    elif(Type == 'whole'):
        Base = Basemap(resolution = 'l', area_thresh = 1000.0, lat_0=0, lon_0=0, llcrnrlon=llon, llcrnrlat=llat, urcrnrlon=rlon, urcrnrlat=rlat)
    Base.drawcoastlines()
    Base.drawcountries()
    Base.drawmapboundary()
    parallels = np.arange(-90, 90, 10)
    Base.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
    merid_values = np.arange(-180, 180., 10)
    meridians = Base.drawmeridians(merid_values,labels=[0,0,0,1],fontsize=10)  
    
    return Base



##Coordinates of the boundary of the targeted area
llon, rlon = -97.5, -82.5
llat, rlat = 27.5, 42.5
Type = 'local' 
Base = BaseMapSet(Type, llon, rlon, llat, rlat)

#PDsub: Population Count of small square area in targeted area we specified before
d_lat = 0.25
d_lon = 0.25
PDsub = np.zeros([int((rlat-llat)/0.25), int((rlon - llon)/0.25)])
PDsub = PD[int(math.floor((llat-(-90))/d_lat)):int(math.floor((rlat-(-90))/d_lat)), int(math.floor((llon-(-180))/d_lon)):int(math.floor((rlon-(-180))/d_lon))]
lon = np.arange(llon, rlon + d_lon, d_lon) #Set up the grid on our specified area and calculate the lat and lon of each square
lat = np.arange(llat, rlat + d_lat, d_lat)

#Transfer lon and Lat coordinates to state plane coordinates
for i in range(len(lon)):
    lon[i], temp = eq_map(lon[i], 0)

for i in range(len(lat)):
    temp, lat[i] = eq_map(0, lat[i])


BaseMapSet('local', llon, rlon, llat, rlat)



