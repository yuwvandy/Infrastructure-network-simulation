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
from Networkouyang import Network2

#--------------------Set up the Basemap where all networks and systems are set up
Base = bm.BaseMapSet(dt.Type1, dt.llon, dt.rlon, dt.llat, dt.rlat)

#--------------------Import the tract data of the specified area and visualize it
Tract_lat, Tract_lon, Tractx, Tracty, Tract_pop, Tract_area = Tract.Tractdata(dt.Tractfile, Base)
Tract.Pop_Visual(Tract_lat, Tract_lon, Tractx, Tracty, Tract_pop, Tract_area)


#PDsub: Population Count of small square area in targeted area we specified before
d_lat = 0.01
d_lon = 0.01
lon = np.arange(dt.llon, dt.rlon + dt.d_lon, dt.d_lon) #Set up the grid on our specified area and calculate the lat and lon of each square
lat = np.arange(dt.llat, dt.rlat + dt.d_lat, dt.d_lat)
Geoy = np.zeros(len(lat))
Geox = np.zeros(len(lon))

#Transfer lon and Lat coordinates to state plane coordinates
for i in range(len(lon)):
    Geox[i], temp = Base(lon[i], 0)

for i in range(len(lat)):
    temp, Geoy[i] = Base(0, lat[i])


#----------------------------------------------------Network initialization
Water = network(dt.name1, dt.supply1, dt.transmission1, dt.demand1, dt.nodenum1, dt.supplynum1, dt.trannum1, dt.demandnum1, dt.color1)
Power = network(dt.name2, dt.supply2, dt.transmission2, dt.demand2, dt.nodenum2, dt.supplynum2, dt.trannum2, dt.demandnum2, dt.color2)
Gas = network(dt.name3, dt.supply3, dt.transmission3, dt.demand3, dt.nodenum3, dt.supplynum3, dt.trannum3, dt.demandnum3, dt.color3)

Network_obj = [Water, Power, Gas]

##For each of three networks: Water, Power, Gas
for i in range(len(Network_obj)):
    #Decision of facility location of three networks
    Network = Network_obj[i]
    Network.Nodelocation(Geox, Geoy, Tract_pop, Tractx, Tracty)
    Network.drawlocation(dt.Type1, llon, rlon, llat, rlat)
    Network.Distmatrix()

    #Decision of network adjacent matrix of three networks
    while(1):
        Network.sampleseq = np.random.poisson(2.5333, size = Network.nodenum)
        if(Network.sampleseq.all() != 0):
            #if(np.max(Network.sampleseq) >= 5):
                #continue
            break
            
    Network.connection(Network.sampleseq, dt.num)
    Network.degree, Network.Ndegree = sf.degreeNdegree(Network.Adjmatrix)
    
    #Plot each single infrastructure network
    Network.drawnetwork(dt.Type1, dt.llon, dt.rlon, dt.llat, dt.rlat)
    #plt.savefig("{} network.png".format(Network.name), dpi = 2000)
    
    ##Calculate the network topology features
    Network.NPL()
    Network.topo_efficiency_cal()
    Network.efficiency_cal()
    Network.cluster_cal()
    Network.topo_diameter()
    Network.spatial_diameter()
    Network.cost_cal(dt.Type2, Tract_pop, Tractx, Tracty)
    

    
###-------------------------------------------Network initialization2
#location                                     
Water2 = Network2('Water2', Geox, Geoy, dt.wnodenum2, dt.wsupplynum2, dt.wdemandnum2, dt.supply1, dt.demand1, dt.color1)
Power2 = Network2('Power2', Geox, Geoy, dt.pnodenum2, dt.psupplynum2, dt.pdemandnum2, dt.supply2, dt.demand2, dt.color2)
Gas2 = Network2('Gas2', Geox, Geoy, dt.gnodenum2, dt.gsupplynum2, dt.gdemandnum2, dt.supply3, dt.demand3, dt.color3)

Network2object = [Water2, Power2, Gas2]
for i in range(len(Network2object)):
    Network = Network2object[i]
    
    Network.Nodeloc()
    Network.Connect(dt.m)
    
    Network.degreeNdegree()
#    Network.plotnetwork(dt.Type1, dt.llon, dt.rlon, dt.llat, dt.rlat)
    
    ##Calculate the network topology features
    Network.NPL()
    Network.topo_efficiency_cal()
    Network.efficiency_cal()
    Network.cluster_cal()
    Network.topo_diameter()
    Network.spatial_diameter()
    Network.cost_cal(dt.Type2, Tract_pop, Tractx, Tracty)
    


#Cost comparison
plt.figure(figsize = (10, 6))
plt.plot(np.arange(1, len(Water.demandc)+1, 1), Water.demandc, color = 'blue', label= 'Water cost')
plt.plot(np.arange(1, len(Power.demandc)+1, 1), Power.demandc, color = 'red', label= 'Power cost')
plt.plot(np.arange(1, len(Gas.demandc)+1, 1), Gas.demandc, color = 'green', label= 'Gas cost')

plt.plot(np.arange(1, len(Water.demandc)+1, 1), [Water2cost]*len(Water.demandc), color = 'blue', label= 'Water cost 2', lw = 5, linestyle = '-.')
plt.plot(np.arange(1, len(Power.demandc)+1, 1), [Power2cost]*len(Power.demandc), color = 'red', label= 'Power cost 2', lw = 5, linestyle = '-.')
plt.plot(np.arange(1, len(Gas.demandc)+1, 1), [Gas2cost]*len(Gas.demandc), color = 'green', label= 'Gas cost 2', lw = 5, linestyle = '-.')
plt.legend(bbox_to_anchor=(1, 1), loc='upper right', ncol=1, fontsize = 15, frameon = 0)
plt.xlabel('Iteration number', fontsize = 20)
plt.ylabel('Overall distance (normalized)', fontsize = 20)
plt.show()  

plt.figure(figsize = (10, 6))
plt.plot(np.arange(1, len(Water.demandc)+1, 1), Water.demandc, color = 'blue', label= 'Water cost')
plt.plot(np.arange(1, len(Power.demandc)+1, 1), Power.demandc, color = 'red', label= 'Power cost')
plt.plot(np.arange(1, len(Water.demandc)+1, 1), [Water2cost]*len(Water.demandc), color = 'blue', label= 'Water cost 2', lw = 5, linestyle = '-.')
plt.plot(np.arange(1, len(Power.demandc)+1, 1), [Power2cost]*len(Power.demandc), color = 'red', label= 'Power cost 2', lw = 5, linestyle = '-.')
plt.legend(bbox_to_anchor=(1, 1), loc='upper right', ncol=1, fontsize = 15, frameon = 0)
plt.xlabel('Iteration number', fontsize = 20)
plt.ylabel('Overall distance (normalized)', fontsize = 20)
plt.show()  

##Degree sequence comparison
Water1para = 6.81633
Water1list1, Water1list2, Water1list3, Water1list4, Water1list5 = degreefit(Water.Ndegree, Water1para)

Power1para = 5.4 
Power1list1, Power1list2, Power1list3, Power1list4, Power1list5 = degreefit(Power.Ndegree, Power1para)

Gas1para = 6.8125
Gas1list1, Gas1list2, Gas1list3, Gas1list4, Gas1list5 = degreefit(Gas.Ndegree, Gas1para)

Water2para = 10.7755
Water2list1, Water2list2, Water2list3, Water2list4, Water2list5 = degreefit(Water2Ndegree, Water2para)

Power2para = 11.6833
Power2list1, Power2list2, Power2list3, Power2list4, Power2list5 = degreefit(Power2Ndegree, Power2para)

Gas2para = 10.9375
Gas2list1, Gas2list2, Gas2list3, Gas2list4, Gas2list5 = degreefit(Gas2Ndegree, Gas2para)
    






