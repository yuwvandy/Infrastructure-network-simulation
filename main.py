# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 10:21:25 2020

@author: 10624
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
from interdependency import phynode2node, phynode2link, phynode2interlink
import os
import matplotlib.pyplot as plt

#--------------------Set up the Basemap where all networks and systems are set up
Base = bm.BaseMapSet(dt.Type1, dt.llon, dt.rlon, dt.llat, dt.rlat)

#--------------------Import the tract data of the specified area and visualize it
Tract_lat, Tract_lon, Tractx, Tracty, Tract_pop, Tract_area = Tract.Tractdata(dt.Tractfile, Base)
Tract_density = Tract_pop/(Tract_area*1.6**2) #person/km**2
Tract.Pop_Visual(Tract_lat, Tract_lon, Tractx, Tracty, Tract_pop, Tract_area)
plt.savefig("./population distribution.pdf", dpi = 1500, bbox_inches='tight', pad_inches=0)

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
    

##population density interpolation
Tract_pop[-4] = Tract_pop[-5]
Tract_density2 = Tract_pop/(Tract_area*1.6**2) #Since Tractdensity equals 0 at that location
tck = scipy.interpolate.bisplrep(Tractx, Tracty, np.log(Tract_density2), s = 110)
density_new = np.exp(scipy.interpolate.bisplev(Geox, Geoy, tck))
Tract_pop2 = density_new
Geoxx, Geoyy = np.meshgrid(Geox, Geoy)
Geoxx, Geoyy = Geoxx.flatten(), Geoyy.flatten()
Base = bm.BaseMapSet(dt.Type1, dt.llon, dt.rlon, dt.llat, dt.rlat)
Base.scatter(Geoxx, Geoyy, c = np.log10(Tract_pop2), cmap = 'Reds', alpha = 0.5, s = 120, edgecolor = 'none', marker = 's')
plt.colorbar(label=r'$\log_{10}({\rm density})$', shrink=0.6)

Temp = 106
while(Temp <= 106):
    os.makedirs('./p2jdata/adjdist/' + str(Temp))
    os.makedirs('./p2jdata/networkinfo/' + str(Temp))
    #Initialize the water, power and gas network objects
    Water = network(dt.water1para, Geox, Geoy)
    Power = network(dt.power1para, Geox, Geoy)
    Gas = network(dt.gas1para, Geox, Geoy)
    networklist = [Water, Power, Gas]
    
    #Calculate the node locations and topology features
    for i in range(len(networklist)):
        Network = networklist[i]
        Network.network_setup(Tract_pop, Tractx, Tracty, i, lon, lat, dt.cnum)
    
    #Initialilze the dependency of power supply nodes on gas demand nodes for generating electricity
    gdemand2psupply = phynode2node(Gas, Power, dt.para_gdemand2psupply)
    
    #Initialilze the dependency of power supply nodes on water demand nodes for cooling effects
    wdemand2psupply = phynode2node(Water, Power, dt.para_wdemand2psupply)
    
    #Initialilze the dependency of gas links on power demand nodes for increasing pressure
    pdemand2glink = phynode2link(Power, Gas, dt.para_pdemand2glink)
    
    #Initialilze the dependency of water links on power demand nodes for overcome energy loss
    pdemand2wlink = phynode2link(Power, Water, dt.para_pdemand2wlink)
    
    #Initialilze the dependency of water-power links on power demand nodes for overcome energy loss
    pdemand2wpinterlink = phynode2interlink(wdemand2psupply, Power, dt.para_pdemand2wpinterlink)
    
    #Initialilze the dependency of gas-power links on power demand nodes for increasing pressure
    pdemand2gpinterlink = phynode2interlink(gdemand2psupply, Power, dt.para_pdemand2gpinterlink)
    
    interdependency = [gdemand2psupply, wdemand2psupply, pdemand2glink, pdemand2wlink, pdemand2wpinterlink, pdemand2gpinterlink]
    
    #Save all data required for solving nonlinear optimization in julia
    #Network information
    for Network in networklist:
        Network.datacollection()
        sf.savenetworkfeature(Network, Temp)
    
    #interdependency
    for i in range(len(interdependency)):
        path1 = './p2jdata/adjdist/' + str(Temp) + '/' + interdependency[i].name + 'adj.csv'
        path2 = './p2jdata/adjdist/' + str(Temp) + '/' + interdependency[i].name + 'distnode2node.csv'  
        
        np.savetxt(path1, interdependency[i].adjmatrix, delimiter = ',')
        np.savetxt(path2, interdependency[i].distmatrix, delimiter = ',')
        
        if(i >= 2):
            path3 = './p2jdata/adjdist/' + str(Temp) + '/' + interdependency[i].name + 'link2nodeid.csv'
            np.savetxt(path3, interdependency[i].link2nodeid + 1, delimiter = ',')
    
        
    #network adjmatrix
    for i in range(len(networklist)):
        path1 = './p2jdata/adjdist/' + str(Temp) + '/'+ networklist[i].name + 'adj.csv'
        path2 = './p2jdata/adjdist/' + str(Temp) + '/' + networklist[i].name + 'distnode2node.csv'
        np.savetxt(path1, networklist[i].Adjmatrix, delimiter = ',')
        np.savetxt(path2, networklist[i].Dismatrix, delimiter = ',')
    
    Temp += 1
    print(Temp)
    








