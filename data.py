# -*- coding: utf-8 -*-
"""
Created on Sat May 23 12:20:34 2020

@author: 10624
"""
##-------------------------------------Data for network data
##Data for water network
water1para = {"name": "Water",
              "supplyname": "Pumping Station",
              "transmissionname": "Storage Tank",
              "demandname": "Deliver Station",
              "nodenum": 49,
              "supplynum": 9,
              "trannum": 6,
              "demandnum": 34,
              "color": "blue",
              "edgediameter": 0.6
              }

##Data for power network
power1para = {"name": "Power",
              "supplyname": "Power Plant",
              "transmissionname": "12 or 23kV substation",
              "demandname": "Deliver Station",
              "nodenum": 60,
              "supplynum": 9,
              "trannum": 14,
              "demandnum": 37,
              "color": "red",
              "edgediameter": 5
              }

##Data for gas network
gas1para = {"name": "Gas",
              "supplyname": "Gas Pumping Station",
              "transmissionname": "Intermediate Station",
              "demandname": "Deliver Station",
              "nodenum": 16,
              "supplynum": 3,
              "trannum": 7,
              "demandnum": 6,
              "color": "green",
              "edgediameter": 0.7
              }
              

#Fit by MATLAB: degreefit poisson
fitdegree = [2.85714, 2.53333, 2.25]
#fitdegree single edge in Shelby County
#fitdegree = [1.42857, 1.25, 1.125]



##-------------------------------------Data for Basemap
llon, rlon = -90.2, -89.6
llat, rlat = 34.98, 35.4
d_lat, d_lon = 0.01, 0.01
Type1 = 'local'

Tractfile = r'.\data\Tract.xlsx'

##-----------------------------------parameter for connecting networks
num = 1

##-----------------------------------data for generating networks using method in ouyangmin paper
m = 3 #how many nodes nearest are connected to the node
cnum = 2
Type2 = 'Population'

water2para = {"name": "Water2",
              "supplyname": "Pumping Station",
              "demandname": "Deliver Station",
              "nodenum": 43,
              "supplynum": 9,
              "demandnum": 34,
              "color": "blue"
              }

##Data for power network in ouyangmin
power2para = {"name": "Power2",
              "supplyname": "Power Plant",
              "demandname": "Deliver Station",
              "nodenum": 46,
              "supplynum": 9,
              "demandnum": 37,
              "color": "red"
              }

##Data for gas network in ouyangmin
gas2para = {"name": "Gas2",
              "supplyname": "Gas Pumping Station",
              "demandname": "Deliver Station",
              "nodenum": 9,
              "supplynum": 3,
              "demandnum": 6,
              "color": "green"
              }

##---------------------------------data for the real Shleby County networks
WNpath, WEpath = ".\data\WaterNodes.xlsx", ".\data\WaterEdges.xlsx"
PNpath, PEpath = ".\data\PowerNodes.xlsx", ".\data\PowerEdges.xlsx"
GNpath, GEpath = ".\data\GasNodes.xlsx", ".\data\GasEdges.xlsx"

watername1, watername2 = "START WATER NODE ID", "END WATER NODE ID"
powername1, powername2 = "START POWER NODE ID", "END POWER NODE ID"
gasname1, gasname2 = "START GAS NODE ID", "END GAS NODE ID"

##Data for water network
water0para = {"name": "Water0",
              "supplyname": "Pumping Station",
              "transmissionname": "Storage Tank",
              "demandname": "Deliver Station",
              "nodenum": 49,
              "supplynum": 9,
              "trannum": 6,
              "demandnum": 34,
              "color": "blue"
              }

##Data for power network
power0para = {"name": "Power0",
              "supplyname": "Power Plant",
              "transmissionname": "12 or 23kV substation",
              "demandname": "Deliver Station",
              "nodenum": 60,
              "supplynum": 9,
              "trannum": 14,
              "demandnum": 37,
              "color": "red"
              }

##Data for gas network
gas0para = {"name": "Gas0",
              "supplyname": "Gas Pumping Station",
              "transmissionname": "Intermediate Station",
              "demandname": "Deliver Station",
              "nodenum": 16,
              "supplynum": 3,
              "trannum": 7,
              "demandnum": 6,
              "color": "green"
              }

##---------------------------------Data for plot the comparison of the distribution and plot the comparison of the box
num_compare = 3
color_compare = [['royalblue', 'deepskyblue', 'blue'], ['maroon', 'darkorange', 'red'], ['darkgreen', 'lime', 'green']]

##--------------------------------Interdependency between several networks
para_gdemand2psupply = {"Name": "gdemand2psupply",
                        "dependnum": 4}

para_wdemand2psupply = {"Name": "wdemand2psupply", 
                        "dependnum": 4}

para_pdemand2glink = {"Name": "pdemand2glink", 
                        "dependnum": 4}

para_pdemand2wlink = {"Name": "pdemand2wlink", 
                        "dependnum": 4}

para_pdemand2wpinterlink = {"Name": "pdemand2wpinterlink",
                       "dependnum": 4}


para_pdemand2gpinterlink = {"Name": "pdemand2gpinterlink",
                       "dependnum": 4}