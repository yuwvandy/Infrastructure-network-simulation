# -*- coding: utf-8 -*-
"""
Created on Sat May 23 12:24:20 2020

@author: 10624
"""
"""
This file is the main function file, which collecting and executing other specific programs.
"""

import data as dt
import Basemapset as bm
from Network import network
import Degreeborrow as db
import pandas as pd

llon, rlon = -90.2, -89.6
llat, rlat = 34.98, 35.4
Type = 'local' 
Base = bm.BaseMapSet(Type, llon, rlon, llat, rlat)

#Import the tract data of the specified area
Tract = pd.read_excel(r'Tract.xlsx')
Tractnum = len(Tract)
Tract_lat, Tract_lon, Tract_pop = np.zeros(Tractnum), np.zeros(Tractnum), np.zeros(Tractnum)
Tractx, Tracty = np.zeros(Tractnum), np.zeros(Tractnum)
area = np.zeros(Tractnum)
for i in range(Tractnum):
    Tract_lat[i] = Tract["Lat"][i]
    Tract_lon[i] = Tract["Lon"][i]
    Tractx[i], Tracty[i] = Base(Tract_lon[i], Tract_lat[i])
    Tract_pop[i] = Tract["Population"][i]
    area[i] = Tract["Area"][i]
 
#Import Basemap
#Coordinates of the boundary of the targeted area

Base = bm.BaseMapSet(Type, llon, rlon, llat, rlat)
Base.scatter(Tract_lon, Tract_lat, latlon=True,
          c=np.log10(Tract_pop), s=area*30,
          cmap='Reds', alpha=0.5)
plt.colorbar(label=r'$\log_{10}({\rm population})$', shrink=0.6)
#plt.clim(3, 7)
for a in [100, 300, 500]:
    plt.scatter([], [], c='k', alpha=0.5, s=a,
                label=str(a) + '*0.03 mi$^2$')
plt.legend(scatterpoints=1, frameon=False,
           labelspacing=1, loc='upper left')

#Base.shadedrelief()
#Base.drawrivers(color = 'blue')
#Base.drawcoastlines(color='gray')
#Base.drawcountries(color='gray')
#Base.drawstates(color='black')

#PDsub: Population Count of small square area in targeted area we specified before
d_lat = 0.01
d_lon = 0.01
lon = np.arange(llon, rlon + d_lon, d_lon) #Set up the grid on our specified area and calculate the lat and lon of each square
lat = np.arange(llat, rlat + d_lat, d_lat)

Geoy = np.zeros(len(lat))
Geox = np.zeros(len(lon))

#Transfer lon and Lat coordinates to state plane coordinates
for i in range(len(lon)):
    Geox[i], temp = Base(lon[i], 0)

for i in range(len(lat)):
    temp, Geoy[i] = Base(0, lat[i])


#Network initialization
Water = network(dt.name1, dt.supply1, dt.transmission1, dt.demand1, dt.nodenum1, dt.supplynum1, dt.trannum1, dt.demandnum1, dt.color1)

#Decision of facility location
Water.Nodelocation(Geox, Geoy, Tract_pop, Tractx, Tracty)
Water.drawlocation(Type, llon, rlon, llat, rlat)

#Decision of facility connection
##Degree distribution fit
path = r'C:\Users\10624\OneDrive - Vanderbilt\Research\Data\Shelby County Water.xlsx'
nodenum = 49
Degree, Ndegree = db.NDegree(49, path)
unisequence, pdfseq, cdfseq, fitpdfseq, fitcdfseq, a, b = degreefit(Ndegree)

sampleseqnei = np.random.poisson(a, size = 49)
while(1):
    sampleseq = np.random.poisson(b, size = 49)
    if(sampleseq.any() != 0):
        break

##Network connection simulation
