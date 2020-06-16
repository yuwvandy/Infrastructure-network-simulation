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
import Tract
import Sharefunction as sf
import Randomlinknetwork as rn
import annealsimulation as ans
from Networkouyang import network2
import numpy as np
import seaborn as sns
import scipy

#--------------------Set up the Basemap where all networks and systems are set up
Base = bm.BaseMapSet(dt.Type1, dt.llon, dt.rlon, dt.llat, dt.rlat)

#--------------------Import the tract data of the specified area and visualize it
Tract_lat, Tract_lon, Tractx, Tracty, Tract_pop, Tract_area = Tract.Tractdata(dt.Tractfile, Base)
Tract_density = Tract_pop/(Tract_area*1.6**2) #person/km**2
Tract.Pop_Visual(Tract_lat, Tract_lon, Tractx, Tracty, Tract_pop, Tract_area)


#PDsub: Population Count of small square area in targeted area we specified before
lon = np.arange(dt.llon, dt.rlon + dt.d_lon, dt.d_lon) #Set up the grid on our specified area and calculate the lat and lon of each square
lat = np.arange(dt.llat, dt.rlat + dt.d_lat, dt.d_lat)
Geoy = np.zeros(len(lat))
Geox = np.zeros(len(lon))

#Transfer lon and Lat coordinates to state plane coordinates
for i in range(len(lon)):
    Geox[i], temp = Base(lon[i], 0)

for i in range(len(lat)):
    temp, Geoy[i] = Base(0, lat[i])

topo_eff1, topo_eff2 = [[], [], []], [[], [], []]

eff1, eff2 = [[], [], []], [[], [], []]

cluster_coeff1, cluster_coeff2 = [[], [], []], [[], [], []]

topodiameter1, topodiameter2 = [[], [], []], [[], [], []]

diameter1, diameter2 = [[], [], []], [[], [], []]

cost1, cost2 = [[], [], []], [[], [], []]

degree1, degree2 = [[], [], []], [[], [], []]
    
#----------------------------------------------------Network initialization
Temp = 0
while(Temp <= 50):
    Water = network(dt.water1para, Geox, Geoy)
    Power = network(dt.power1para, Geox, Geoy)
    Gas = network(dt.gas1para, Geox, Geoy)
    
    Network_obj = [Water, Power, Gas]
    
    ##For each of three networks: Water, Power, Gas
    for i in range(len(Network_obj)):
        #Decision of facility location of three networks
        Network = Network_obj[i]
        Network.network_setup(Tract_density, Tractx, Tracty, i)
        
        topo_eff1[i].append(Network.topo_efficiency)
        eff1[i].append(Network.efficiency)
        cluster_coeff1[i].append(Network.cluster_coeff)
        topodiameter1[i].append(Network.topodiameter)
        diameter1[i].append(Network.diameter)
        cost1[i].append(Network.cost)
        degree1[i].append(Network.degree)
        
    
        
    ###-------------------------------------------Network initialization2
    #location                                     
    Water2 = network2(dt.water2para, Geox, Geoy)
    Power2 = network2(dt.power2para, Geox, Geoy)
    Gas2 = network2(dt.gas2para, Geox, Geoy)
    
    Network2object = [Water2, Power2, Gas2]
    for i in range(len(Network2object)):
        Network = Network2object[i]
        
        Network.network_setup(Tract_density, Tractx, Tracty)
        
        topo_eff2[i].append(Network.topo_efficiency)
        eff2[i].append(Network.efficiency)
        cluster_coeff2[i].append(Network.cluster_coeff)
        topodiameter2[i].append(Network.topodiameter)
        diameter2[i].append(Network.diameter)
        cost2[i].append(Network.cost)
        degree2[i].append(Network.degree)
    
    Temp += 1
    print(Temp)




##Remove the element of the infinity value in list network.efficiency
eff1 = [sf.Removeinf(eff1[0]), sf.Removeinf(eff1[1]), sf.Removeinf(eff1[2])] 
key1,  key2 = ['Method1', 'Method2', 'The real network'], ['Water', 'Power', 'Gas']

    
#Compare several features of networks genering using different methods and original networks
##Cost: demand - population
value = [Shelby_Water.cost, Shelby_Power.cost, Shelby_Gas.cost]
cost1_ave, cost2_ave, cost1_std, cost2_std, cost1_cv, cost2_cv = sf.statistical_analysis('Cost', cost1, cost2, value, dt.color_compare, dt.num_compare, key1, key2)


##Cluster_coeff
value = [Shelby_Water.cluster_coeff, Shelby_Power.cluster_coeff, Shelby_Gas.cluster_coeff]
cluster1_ave, cluster2_ave, cluster1_std, cluster2_std, cluster1_cv, cluster2_cv = sf.statistical_analysis('Cluster coefficient', cluster_coeff1, cluster_coeff2, value, dt.color_compare, dt.num_compare, key1, key2)


##Spatial efficiency
value = [Shelby_Water.efficiency, Shelby_Power.efficiency, Shelby_Gas.efficiency]
eff1_ave, eff2_ave, eff1_std, eff2_std, eff1_cv, eff2_cv = sf.statistical_analysis('Spatial efficiency', eff1, eff2, value, dt.color_compare, dt.num_compare, key1, key2)


##Topological efficiency
value = [Shelby_Water.topo_efficiency, Shelby_Power.topo_efficiency, Shelby_Gas.topo_efficiency]
topoeff1_ave, topoeff2_ave, topoeff1_std, topoeff2_std, topoeff1_cv, topoeff2_cv = sf.statistical_analysis('Topological efficiency', topo_eff1, topo_eff2, value, dt.color_compare, dt.num_compare, key1, key2)


##Spatial diameter
value = [Shelby_Water.diameter, Shelby_Power.diameter, Shelby_Gas.diameter]
diameter1_ave, diameter2_ave, diameter1_std, diameter2_std, diameter1_cv, diameter2_cv = sf.statistical_analysis('Spatial diameter', diameter1, diameter2, value, dt.color_compare, dt.num_compare, key1, key2)


##Topological diameter
value = [Shelby_Water.topodiameter, Shelby_Power.topodiameter, Shelby_Gas.topodiameter]
topodiameter1_ave, topodiameter2_ave, topodiameter1_std, topodiameter2_std, topodiameter1_cv, topodiameter2_cv = sf.statistical_analysis('Spatial diameter', topodiameter1, topodiameter2, value, dt.color_compare, dt.num_compare, key1, key2)




##Cost comparison
#plt.figure(figsize = (10, 6))
#plt.plot(np.arange(1, len(Water.demandc)+1, 1), Water.demandc, color = 'blue', label= 'Water cost')
#plt.plot(np.arange(1, len(Power.demandc)+1, 1), Power.demandc, color = 'red', label= 'Power cost')
#plt.plot(np.arange(1, len(Gas.demandc)+1, 1), Gas.demandc, color = 'green', label= 'Gas cost')
#
#plt.plot(np.arange(1, len(Water.demandc)+1, 1), [Water2cost]*len(Water.demandc), color = 'blue', label= 'Water cost 2', lw = 5, linestyle = '-.')
#plt.plot(np.arange(1, len(Power.demandc)+1, 1), [Power2cost]*len(Power.demandc), color = 'red', label= 'Power cost 2', lw = 5, linestyle = '-.')
#plt.plot(np.arange(1, len(Gas.demandc)+1, 1), [Gas2cost]*len(Gas.demandc), color = 'green', label= 'Gas cost 2', lw = 5, linestyle = '-.')
#plt.legend(bbox_to_anchor=(1, 1), loc='upper right', ncol=1, fontsize = 15, frameon = 0)
#plt.xlabel('Iteration number', fontsize = 20)
#plt.ylabel('Overall distance (normalized)', fontsize = 20)
#plt.show()  
#
#plt.figure(figsize = (10, 6))
#plt.plot(np.arange(1, len(Water.demandc)+1, 1), Water.demandc, color = 'blue', label= 'Water cost')
#plt.plot(np.arange(1, len(Power.demandc)+1, 1), Power.demandc, color = 'red', label= 'Power cost')
#plt.plot(np.arange(1, len(Water.demandc)+1, 1), [Water2cost]*len(Water.demandc), color = 'blue', label= 'Water cost 2', lw = 5, linestyle = '-.')
#plt.plot(np.arange(1, len(Power.demandc)+1, 1), [Power2cost]*len(Power.demandc), color = 'red', label= 'Power cost 2', lw = 5, linestyle = '-.')
#plt.legend(bbox_to_anchor=(1, 1), loc='upper right', ncol=1, fontsize = 15, frameon = 0)
#plt.xlabel('Iteration number', fontsize = 20)
#plt.ylabel('Overall distance (normalized)', fontsize = 20)
#plt.show()  







