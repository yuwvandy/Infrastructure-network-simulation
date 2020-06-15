# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:03:24 2020

@author: 10624
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 25 14:20:46 2020

@author: wany105
"""
import Basemapset as bm
import data as dt
from Network import network
from matplotlib import pyplot as plt
import Sharefunction as sf
import math
import numpy as np
import pandas as pd

def read(Npath, Epath):
    """Read the .xlsx files and get the node and edge lists
    """
    N, E = pd.read_excel(Npath), pd.read_excel(Epath)
    
    return N, E

def latlontypenumedge(N, E, name1, name2):
    """Read the node and edge lists, get the latitude, longitude, nodenumber and node type
    """
    lat, lon = np.array(N["Lat"]), np.array(N["Long"])
    Type = np.array(N["NODE CLASS"])
    num = len(lat)
    
    edge = np.stack((np.array(E[name1]) - 1, np.array(E[name2]) - 1)).transpose()
    
    return lat, lon, Type, num, edge

def latlon2XY(lat, lon, Base):
    """Transform the latitude and longitude to the X and Y
    """
    
    X, Y = Base(lon, lat)
    
    return X, Y

def supplytrandemandnum(Type, paralist, num):
    """Calculate the number of supply nodes, transmission nodes and demand nodes
    """
    supply, transmission, demand = 0, 0, 0
    
    for i in range(num):
        if(Type[i] == paralist["supplyname"]):
            supply += 1
        if(Type[i] == paralist["transmissionname"]):
            transmission += 1
        if(Type[i] == paralist["demandname"]):
            demand += 1
            
    return supply, transmission, demand

def supplytrandemandxy(Network):
    """Calculate the the xy of the supply, demand and transmission nodes
    """
    Network.demandx, Network.demandy = Network.x[Network.demandseries], Network.y[Network.demandseries]
    Network.tranx, Network.trany = Network.x[Network.transeries], Network.y[Network.transeries]
    Network.supplyx, Network.supplyy = Network.x[Network.supplyseries], Network.y[Network.supplyseries]

def Adjmatrix(Network, edge, Type):
    """Calculate the adjacent matrix of the given network
    """
    Network.Adjmatrix = np.zeros((Network.nodenum, Network.nodenum), dtype = int)
    for i in range(len(edge)):
        Network.Adjmatrix[edge[i, 0], edge[i, 1]] = 1
#        Network.Adjmatrix[edge[i, 1], edge[i, 0]] = 1
        if(Type[edge[i, 0]] == Type[edge[i, 1]]):
            Network.Adjmatrix[edge[i, 1], edge[i, 0]] = 1
        
def cost(Network, Tract_pop, Tractx, Tracty, Geox, Geoy):
    """Calculate the overall cost all a new solution: two type: demand-population, supply-transmission(transmission-demand)
    """
    x = sf.FeatureScaling2(Network.demandx, np.min(Geox), np.max(Geox) - np.min(Geox))
    y = sf.FeatureScaling2(Network.demandy, np.min(Geoy), np.max(Geoy) - np.min(Geoy))
    Tract_pop1 = sf.FeatureScaling(Tract_pop)
    Tractx1 = sf.FeatureScaling(Tractx)
    Tracty1 = sf.FeatureScaling(Tracty)
        
    Sum_Cost = 0
    for i in range(len(Tractx)):
        Min_Dist = math.inf
        for k in range(len(x)):
            Dist = math.sqrt((Tracty1[i] - y[k])**2 + (Tractx1[i] - x[k])**2)
            if(Dist < Min_Dist):
                Min_Dist = Dist
#                index = k
        Sum_Cost += Min_Dist*Tract_pop1[i]
                
    Network.cost = Sum_Cost

Wname = 'Swater'
Pname = 'Spower'
Gname = 'Sgas'


WNpath, WEpath = r'.\data\WaterNodes.xlsx', r'.\data\WaterEdges.xlsx'
PNpath, PEpath = r'.\data\PowerNodes.xlsx', r'.\data\PowerEdges.xlsx'
GNpath, GEpath = r'.\data\GasNodes.xlsx', r'.\data\GasEdges.xlsx'

WN, WE = read(WNpath, WEpath)
PN, PE = read(PNpath, PEpath)
GN, GE = read(GNpath, GEpath)

Wlat, Wlon, WType, Wnum, Wedge = latlontypenumedge(WN, WE, "START WATER NODE ID", "END WATER NODE ID")
Plat, Plon, PType, Pnum, Pedge = latlontypenumedge(PN, PE, "START POWER NODE ID", "END POWER NODE ID")
Glat, Glon, GType, Gnum, Gedge = latlontypenumedge(GN, GE, "START GAS NODE ID", "END GAS NODE ID")

plt.figure(figsize = (20, 12))
Base = bm.BaseMapSet(dt.Type1, dt.llon, dt.rlon, dt.llat, dt.rlat)
WX, WY = latlon2XY(Wlat, Wlon, Base)
PX, PY = latlon2XY(Plat, Plon, Base)
GX, GY = latlon2XY(Glat, Glon, Base)

Wsupply, Wtransmission, Wdemand = supplytrandemandnum(WType, dt.water1para, Wnum)
Psupply, Ptransmission, Pdemand = supplytrandemandnum(PType, dt.power1para, Pnum)
Gsupply, Gtransmission, Gdemand = supplytrandemandnum(GType, dt.gas1para, Gnum)

Shelby_Water = network(dt.water0para, Geox, Geoy)
Shelby_Power = network(dt.power0para, Geox, Geoy)
Shelby_Gas = network(dt.gas0para, Geox, Geoy)

Shelby_Water.x, Shelby_Water.y, Shelby_Water.Type = WX, WY, WType
Shelby_Power.x, Shelby_Power.y, Shelby_Power.Type = PX, PY, PType
Shelby_Gas.x, Shelby_Gas.y, Shelby_Gas.Type = GX, GY, GType

supplytrandemandxy(Shelby_Water)
supplytrandemandxy(Shelby_Power)
supplytrandemandxy(Shelby_Gas)

ShelbyNetwork = [Shelby_Water, Shelby_Power, Shelby_Gas]
edge = [Wedge, Pedge, Gedge]

for i in range(len(ShelbyNetwork)):
    Network = ShelbyNetwork[i]
    Network.Distmatrix()
    Adjmatrix(Network, edge[i], Network.Type)
    Network.degree, Network.Ndegree = sf.degreeNdegree(Network.Adjmatrix)
    Network.drawnetwork(dt.Type1, dt.llon, dt.rlon, dt.llat, dt.rlat)
    Network.cal_topology_feature()
#    cost(Network, Tract_pop, Tractx, Tracty, Geox, Geoy)
    cost(Network, Tract_density, Tractx, Tracty, Geox, Geoy)


#------------------------------------------------------------------------------
plt.figure(figsize = (20, 12))
Base = bm.BaseMapSet(dt.Type1, dt.llon, dt.rlon, dt.llat, dt.rlat)

Wx, Wy = Base(Wlon, Wlat)
Px, Py = Base(Plon, Plat)
Gx, Gy = Base(Glon, Glat)

##Water network
Wnum = len(Wlat)
Wxs, Wxm, Wxd = [], [], []
Wys, Wym, Wyd = [], [], []
for i in range(len(Wx)):
    if(Wtype[i] == "Pump Stations"):
        Wxs.append(Wx[i])
        Wys.append(Wy[i])
    if(Wtype[i] == "Storage Tanks"):
        Wxm.append(Wx[i])
        Wym.append(Wy[i])
    if(Wtype[i] == "Delivery Nodes"):
        Wxd.append(Wx[i])
        Wyd.append(Wy[i])
        
#Distance and adjacent matrix
Wadjmatrix, Wdistmatrix = np.zeros((Wnum, ))
for i in range(len())
        
plt.scatter(Wxs, Wys, 400, 'blue' , marker = '+', label = 'Pumping station')        
plt.scatter(Wxm, Wym, 200, 'blue', marker = '*', label = 'Storage tank')        
plt.scatter(Wxd, Wyd, 100, 'blue', marker = 'o', label = 'Delivery station')        
        
        
for j in range(len(Wateredge)):
    plt.plot([Wx[Wateredge[j, 0]], Wx[Wateredge[j, 1]]], [Wy[Wateredge[j, 0]], Wy[Wateredge[j, 1]]], color = 'black')
plt.legend(bbox_to_anchor=(0, 1), loc='upper left', ncol=1, fontsize = 15, frameon = 0)



##Power network
plt.figure(figsize = (20, 12))
Base = BaseMapSet('local')
Pxs, Pxm, Pxd = [], [], []
Pys, Pym, Pyd = [], [], []
for i in range(len(Px)):
    if(Ptype[i] == "Gate Station"):
        Pxs.append(Px[i])
        Pys.append(Py[i])
    if(Ptype[i] == "Intersection Point"):
        Pxm.append(Px[i])
        Pym.append(Py[i])
    if(Ptype[i] == "23kV Substation" or Ptype[i] == "12kV Substation"):
        Pxd.append(Px[i])
        Pyd.append(Py[i])
        
plt.scatter(Pxs, Pys, 400, 'red' , marker = '+', label = 'Power Plant')        
plt.scatter(Pxm, Pym, 200, 'red', marker = '*', label = '12 or 23kV Substation')        
plt.scatter(Pxd, Pyd, 100, 'red', marker = 'o', label = 'Deliver Station')        
        
        

for j in range(len(Poweredge)):
    plt.plot([Px[Poweredge[j, 0]], Px[Poweredge[j, 1]]], [Py[Poweredge[j, 0]], Py[Poweredge[j, 1]]], color = 'black')
plt.legend(bbox_to_anchor=(0, 1), loc='upper left', ncol=1, fontsize = 25, frameon = 0)
plt.savefig("Power network.png", dpi = 2000) 

##Gas network
plt.figure(figsize = (20, 12))
Base = BaseMapSet('local')
Gxs, Gxm, Gxd = [], [], []
Gys, Gym, Gyd = [], [], []
for i in range(len(Gx)):
    if(Gtype[i] == "Gate Station"):
        Gxs.append(Gx[i])
        Gys.append(Gy[i])
    if(Gtype[i] == "Regulator Station"):
        Gxm.append(Gx[i])
        Gym.append(Gy[i])
    if(Gtype[i] == "Other"):
        Gxd.append(Gx[i])
        Gyd.append(Gy[i])
        
plt.scatter(Gxs, Gys, 400, 'green' , marker = '+', label = 'Gate station')        
plt.scatter(Gxm, Gym, 200, 'green', marker = '*', label = 'Regulator Station')        
plt.scatter(Gxd, Gyd, 100, 'green', marker = 'o', label = 'Deliver Station')        
        
        

for j in range(len(Gasedge)):
    plt.plot([Gx[Gasedge[j, 0]], Gx[Gasedge[j, 1]]], [Gy[Gasedge[j, 0]], Gy[Gasedge[j, 1]]], color = 'black')
plt.legend(bbox_to_anchor=(0, 1), loc='upper left', ncol=1, fontsize = 15, frameon = 0)


####Calculate the topological features

