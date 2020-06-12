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
while(Temp <= 10):
    Water = network(dt.water1para, Geox, Geoy)
    Power = network(dt.power1para, Geox, Geoy)
    Gas = network(dt.gas1para, Geox, Geoy)
    
    Network_obj = [Water, Power, Gas]
    
    ##For each of three networks: Water, Power, Gas
    for i in range(len(Network_obj)):
        #Decision of facility location of three networks
        Network = Network_obj[i]
        Network.Nodelocation(Tract_density, Tractx, Tracty)
#        Network.Nodelocation(Tract_pop, Tractx, Tracty)
#        Network.drawlocation(dt.Type1, dt.llon, dt.rlon, dt.llat, dt.rlat)
        Network.Distmatrix()
    
        #Decision of network adjacent matrix of three networks
        while(1):
            Network.sampleseq = np.random.poisson(dt.fitdegree[i], size = Network.nodenum)
            if(Network.sampleseq.all() != 0):
                #if(np.max(Network.sampleseq) >= 5):
                    #continue
                break
                
        Network.connection(Network.sampleseq, dt.num)
        Network.degree, Network.Ndegree = sf.degreeNdegree(Network.Adjmatrix)
        
        #Plot each single infrastructure network
#        Network.drawnetwork(dt.Type1, dt.llon, dt.rlon, dt.llat, dt.rlat)
        #plt.savefig("{} network.png".format(Network.name), dpi = 2000)
        
        ##Calculate the network topology features
        Network.cal_topology_feature()
        Network.cost_cal(dt.Type2, Tract_density, Tractx, Tracty)
#        Network.cost_cal(dt.Type2, Tract_pop, Tractx, Tracty)
        
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
        
        Network.Nodeloc()
        Network.Connect(dt.m)
        
        Network.degreeNdegree()
    #    Network.plotnetwork(dt.Type1, dt.llon, dt.rlon, dt.llat, dt.rlat)
        
        ##Calculate the network topology features
        Network.cal_topology_feature()
#        Network.cost_cal(dt.Type2, Tract_pop, Tractx, Tracty)
        Network.cost_cal(dt.Type2, Tract_density, Tractx, Tracty)
        
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
sf.plotdistcompare([cost1[0], 'royalblue', 'Method 1', 'Cost'], [cost2[0], 'deepskyblue', 'Method 2', 'Cost'], [[Shelby_Water.cost]*2, [0, 1.4], 'blue'])
sf.plotdistcompare([cost1[1], 'maroon', 'Method 1', 'Cost'], [cost2[1], 'darkorange', 'Method 2', 'Cost'], [[Shelby_Power.cost]*2, [0, 1.4], 'red'])
sf.plotdistcompare([cost1[2], 'darkgreen', 'Method 1', 'Cost'], [cost2[2], 'lime', 'Method 2', 'Cost'],  [[Shelby_Gas.cost]*2, [0, 1.4], 'green'])
cost1_ave = [np.mean(cost1[0]), np.mean(cost1[1]), np.mean(cost1[2])]
cost1_std = [np.std(cost1[0]), np.std(cost1[1]), np.std(cost1[2])]
cost1_cv = [scipy.stats.variation(cost1[0]), scipy.stats.variation(cost1[1]), scipy.stats.variation(cost1[2])]

cost2_ave = [np.mean(cost2[0]), np.mean(cost2[1]), np.mean(cost2[2])]
cost2_std = [np.std(cost2[0]), np.std(cost2[1]), np.std(cost2[2])]
cost2_cv = [scipy.stats.variation(cost2[0]), scipy.stats.variation(cost2[1]), scipy.stats.variation(cost2[2])]


value_cost = [Shelby_Water.cost, Shelby_Power.cost, Shelby_Gas.cost]
sf.plotboxcompare(value_cost, cost1, cost2, key1, key2)



sf.plotdistcompare([cluster_coeff1[0], 'royalblue', 'Method 1', 'Cluster coefficient'], [cluster_coeff2[0], 'deepskyblue', 'Method 2', 'Cluster coefficient'], [[Shelby_Water.cluster_coeff]*2, [0, 14], 'blue'])
sf.plotdistcompare([cluster_coeff1[1], 'maroon', 'Method 1', 'Cluster coefficient'], [cluster_coeff2[1], 'darkorange', 'Method 2', 'Cluster coefficient'], [[Shelby_Power.cluster_coeff]*2, [0, 14], 'red'])
sf.plotdistcompare([cluster_coeff1[2], 'darkgreen', 'Method 1', 'Cluster coefficient'], [cluster_coeff2[2], 'lime', 'Method 2', 'Cluster coefficient'],  [[Shelby_Gas.cluster_coeff]*2, [0, 6], 'green'])
cluster_coeff1_ave = [np.mean(cluster_coeff1[0]), np.mean(cluster_coeff1[1]), np.mean(cluster_coeff1[2])]
cluster_coeff1_std = [np.std(cluster_coeff1[0]), np.std(cluster_coeff1[1]), np.std(cluster_coeff1[2])]
cluster_coeff1_cv = [scipy.stats.variation(cluster_coeff1[0]), scipy.stats.variation(cluster_coeff1[1]), scipy.stats.variation(cluster_coeff1[2])]

cluster_coeff2_ave = [np.mean(cluster_coeff2[0]), np.mean(cluster_coeff2[1]), np.mean(cluster_coeff2[2])]
cluster_coeff2_std = [np.std(cluster_coeff2[0]), np.std(cluster_coeff2[1]), np.std(cluster_coeff2[2])]
cluster_coeff2_cv = [scipy.stats.variation(cluster_coeff2[0]), scipy.stats.variation(cluster_coeff2[1]), scipy.stats.variation(cluster_coeff2[2])]


value_cluster_coeff = [Shelby_Water.cluster_coeff, Shelby_Power.cluster_coeff, Shelby_Gas.cluster_coeff]
sf.plotboxcompare(value_cluster_coeff, cluster_coeff1, cluster_coeff2, key1, key2)



sf.plotdistcompare([eff1[0], 'royalblue', 'Method 1', 'Spatial efficiency'], [eff2[0], 'deepskyblue', 'Method 2', 'Spatial efficiency'], [[Shelby_Water.efficiency]*2, [0, 160], 'blue'])
sf.plotdistcompare([eff1[1], 'maroon', 'Method 1', 'Spatial efficiency'], [eff2[1], 'darkorange', 'Method 2', 'Spatial efficiency'], [[Shelby_Power.efficiency]*2, [0, 140], 'red'])
sf.plotdistcompare([eff1[2], 'darkgreen', 'Method 1', 'Spatial efficiency'], [eff2[2], 'lime', 'Method 2', 'Spatial efficiency'],  [[Shelby_Gas.efficiency]*2, [0, 50], 'green'])
eff1_ave = [np.mean(eff1[0]), np.mean(eff1[1]), np.mean(eff1[2])]
eff1_std = [np.std(eff1[0]), np.std(eff1[1]), np.std(eff1[2])]
eff1_cv = [scipy.stats.variation(eff1[0]), scipy.stats.variation(eff1[1]), scipy.stats.variation(eff1[2])]

eff2_ave = [np.mean(eff2[0]), np.mean(eff2[1]), np.mean(eff2[2])]
eff2_std = [np.std(eff2[0]), np.std(eff2[1]), np.std(eff2[2])]
eff2_cv = [scipy.stats.variation(eff2[0]), scipy.stats.variation(eff2[1]), scipy.stats.variation(eff2[2])]


value_eff = [Shelby_Water.efficiency, Shelby_Power.efficiency, Shelby_Gas.efficiency]
sf.plotboxcompare(value_eff, eff1, eff2, key1, key2)


sf.plotdistcompare([topo_eff1[0], 'royalblue', 'Method 1', 'Topological efficiency'], [topo_eff2[0], 'deepskyblue', 'Method 2', 'Topological efficiency'], [[Shelby_Water.topo_efficiency]*2, [0, 25], 'blue'])
sf.plotdistcompare([topo_eff1[1], 'maroon', 'Method 1', 'Topological efficiency'], [topo_eff2[1], 'darkorange', 'Method 2', 'Topological efficiency'], [[Shelby_Power.topo_efficiency]*2, [0, 25], 'red'])
sf.plotdistcompare([topo_eff1[2], 'darkgreen', 'Method 1', 'Topological efficiency'], [topo_eff2[2], 'lime', 'Method 2', 'Topological efficiency'],  [[Shelby_Gas.topo_efficiency]*2, [0, 6], 'green'])
topoeff1_ave = [np.mean(topo_eff1[0]), np.mean(topo_eff1[1]), np.mean(topo_eff1[2])]
topoeff1_std = [np.std(topo_eff1[0]), np.std(topo_eff1[1]), np.std(topo_eff1[2])]
topoeff1_cv = [scipy.stats.variation(topo_eff1[0]), scipy.stats.variation(topo_eff1[1]), scipy.stats.variation(topo_eff1[2])]


topoeff2_ave = [np.mean(topo_eff2[0]), np.mean(topo_eff2[1]), np.mean(topo_eff2[2])]
topoeff2_std = [np.std(topo_eff2[0]), np.std(topo_eff2[1]), np.std(topo_eff2[2])]
topoeff2_cv = [scipy.stats.variation(topo_eff2[0]), scipy.stats.variation(topo_eff2[1]), scipy.stats.variation(topo_eff2[2])]


value_topo_eff = [Shelby_Water.topo_efficiency, Shelby_Power.topo_efficiency, Shelby_Gas.topo_efficiency]
sf.plotboxcompare(value_topo_eff, topo_eff1, topo_eff2, key1, key2)



sf.plotdistcompare([diameter1[0], 'royalblue', 'Method 1', 'Spatial diameter'], [diameter2[0], 'deepskyblue', 'Method 2', 'Spatial diameter'], [[Shelby_Water.diameter]*2, [0, 0.035], 'blue'])
sf.plotdistcompare([diameter1[1], 'maroon', 'Method 1', 'Spatial diameter'], [diameter2[1], 'darkorange', 'Method 2', 'Spatial diameter'], [[Shelby_Power.diameter]*2, [0, 0.035], 'red'])
sf.plotdistcompare([diameter1[2], 'darkgreen', 'Method 1', 'Spatial diameter'], [diameter2[2], 'lime', 'Method 2', 'Spatial diameter'],  [[Shelby_Gas.diameter]*2, [0, 0.035], 'green'])
diameter1_ave = [np.mean(diameter1[0]), np.mean(diameter1[1]), np.mean(diameter1[2])]
diameter1_std = [np.std(diameter1[0]), np.std(diameter1[1]), np.std(diameter1[2])]
diameter1_cv = [scipy.stats.variation(diameter1[0]), scipy.stats.variation(diameter1[1]), scipy.stats.variation(diameter1[2])]

diameter2_ave = [np.mean(diameter2[0]), np.mean(diameter2[1]), np.mean(diameter2[2])]
diameter2_std = [np.std(diameter2[0]), np.std(diameter2[1]), np.std(diameter2[2])]
diameter2_cv = [scipy.stats.variation(diameter2[0]), scipy.stats.variation(diameter2[1]), scipy.stats.variation(diameter2[2])]


value_diameter = [Shelby_Water.diameter, Shelby_Power.diameter, Shelby_Gas.diameter]
sf.plotboxcompare(value_diameter, diameter1, diameter2, key1, key2)


sf.plotdistcompare([topodiameter1[0], 'royalblue', 'Method 1', 'Topological diameter'], [topodiameter2[0], 'deepskyblue', 'Method 2', 'Topological diameter'], [[Shelby_Water.topodiameter]*2, [0, 0.4], 'blue'])
sf.plotdistcompare([topodiameter1[1], 'maroon', 'Method 1', 'Topological diameter'], [topodiameter2[1], 'darkorange', 'Method 2', 'Topological diameter'], [[Shelby_Power.topodiameter]*2, [0, 1.0], 'red'])
sf.plotdistcompare([topodiameter1[2], 'darkgreen', 'Method 1', 'Topological diameter'], [topodiameter2[2], 'lime', 'Method 2', 'Topological diameter'],  [[Shelby_Gas.topodiameter]*2, [0, 1.0], 'green'])
topodiameter1_ave = [np.mean(topodiameter1[0]), np.mean(topodiameter1[1]), np.mean(topodiameter1[2])]
topodiameter1_std = [np.std(topodiameter1[0]), np.std(topodiameter1[1]), np.std(topodiameter1[2])]
topodiameter1_cv = [scipy.stats.variation(topodiameter1[0]), scipy.stats.variation(topodiameter1[1]), scipy.stats.variation(topodiameter1[2])]

topodiameter2_ave = [np.mean(topodiameter2[0]), np.mean(topodiameter2[1]), np.mean(topodiameter2[2])]
topodiameter2_std = [np.std(topodiameter2[0]), np.std(topodiameter2[1]), np.std(topodiameter2[2])]
topodiameter2_cv = [scipy.stats.variation(topodiameter2[0]), scipy.stats.variation(topodiameter2[1]), scipy.stats.variation(topodiameter2[2])]


value_topo_diameter = [Shelby_Water.topodiameter, Shelby_Power.topodiameter, Shelby_Gas.topodiameter]
sf.plotboxcompare(value_topo_diameter, topodiameter1, topodiameter2, key1, key2)



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







