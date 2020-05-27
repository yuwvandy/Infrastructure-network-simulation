# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:54:42 2020

@author: 10624
"""
import pandas as pd
import numpy as np
import Basemapset as bm
import data as dt
from matplotlib import pyplot as plt

def Tractdata(filename, Base):
    """Import and rearrange the tract data
    Input: filename - the name of the file containing tract data
           Base - the Basemap which is imported in the main function
    Output: Tract_lat, Tract_lon, Tracx, Tracty, Tract_pop, Tract_area
    """
    Tract = pd.read_excel(filename)
    Tractnum = len(Tract)
    Tract_lat, Tract_lon, Tract_pop = np.zeros(Tractnum), np.zeros(Tractnum), np.zeros(Tractnum)
    Tractx, Tracty = np.zeros(Tractnum), np.zeros(Tractnum)
    Tract_area = np.zeros(Tractnum)
    
    for i in range(Tractnum):
        Tract_lat[i] = Tract["Lat"][i]
        Tract_lon[i] = Tract["Lon"][i]
        Tractx[i], Tracty[i] = Base(Tract_lon[i], Tract_lat[i])
        Tract_pop[i] = Tract["Population"][i]
        Tract_area[i] = Tract["Area"][i]
    
    return Tract_lat, Tract_lon, Tractx, Tracty, Tract_pop, Tract_area

def Pop_Visual(Tract_lat, Tract_lon, Tractx, Tracty, Tract_pop, Tract_area):
    """Import the population data and visualize it as a heatmap
    """
    Base = bm.BaseMapSet(dt.Type1, dt.llon, dt.rlon, dt.llat, dt.rlat)
    
    Base.scatter(Tract_lon, Tract_lat, latlon=True,
              c=np.log10(Tract_pop), s=Tract_area*30,
              cmap='Reds', alpha=0.5)
    
    plt.colorbar(label=r'$\log_{10}({\rm population})$', shrink=0.6)

    for a in [100, 300, 500]:
        plt.scatter([], [], c='k', alpha=0.5, s=a,
                    label=str(a) + '*0.03 mi$^2$')
        
    plt.legend(scatterpoints=1, frameon=False,
               labelspacing=1, loc='upper left')

