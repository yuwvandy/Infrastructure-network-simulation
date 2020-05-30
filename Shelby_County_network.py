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
WN = pd.read_excel (r'C:\Users\wany105\OneDrive - Vanderbilt\Research\ShelbyCounty_DataRead\WaterNodes.xlsx') #for an earlier version of Excel, you may need to use the file extension of 'xls'
WE = pd.read_excel (r'C:\Users\wany105\OneDrive - Vanderbilt\Research\ShelbyCounty_DataRead\WaterEdges.xlsx') #for an earlier version of Excel, you may need to use the file extension of 'xls'
PN = pd.read_excel (r'C:\Users\wany105\OneDrive - Vanderbilt\Research\ShelbyCounty_DataRead\PowerNodes.xlsx') #for an earlier version of Excel, you may need to use the file extension of 'xls'
PE = pd.read_excel (r'C:\Users\wany105\OneDrive - Vanderbilt\Research\ShelbyCounty_DataRead\PowerEdges.xlsx') #for an earlier version of Excel, you may need to use the file extension of 'xls'
GN = pd.read_excel (r'C:\Users\wany105\OneDrive - Vanderbilt\Research\ShelbyCounty_DataRead\GasNodes.xlsx') #for an earlier version of Excel, you may need to use the file extension of 'xls'
GE = pd.read_excel (r'C:\Users\wany105\OneDrive - Vanderbilt\Research\ShelbyCounty_DataRead\GasEdges.xlsx') #for an earlier version of Excel, you may need to use the file extension of 'xls'

Wlat, Wlon, Wtype = np.array(WN["Lat"]), np.array(WN["Long"]), np.array(WN["NODE CLASS"])
Plat, Plon, Ptype = np.array(PN["Lat"]), np.array(PN["Long"]), np.array(PN["NODE CLASS"])
Glat, Glon, Gtype = np.array(GN["Lat"]), np.array(GN["Long"]), np.array(GN["NODE CLASS"])

Wateredge = np.stack((np.array(WE["START WATER NODE ID"]) - 1, np.array(WE["END WATER NODE ID"]) - 1)).transpose()
Poweredge = np.stack((np.array(PE["START POWER NODE ID"]) - 1, np.array(PE["END POWER NODE ID"]) - 1)).transpose()
Gasedge = np.stack((np.array(GE["START GAS NODE ID"]) - 1, np.array(GE["END GAS NODE ID"]) - 1)).transpose()

plt.figure(figsize = (20, 12))
Base = BaseMapSet('local')
Wx, Wy = Base(Wlon, Wlat)
Px, Py = Base(Plon, Plat)
Gx, Gy = Base(Glon, Glat)

##Water network
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

