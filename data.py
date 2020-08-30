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
              "demandname": "Intermediate Delivery Stations",
              "nodenum": 49,
              "supplynum": 9,
              "trannum": 6,
              "demandnum": 34,
              "color": "blue",
              "edgediameter": 0.6
              }

##Data for power network
power1para = {"name": "Power",
              "supplyname": "Power Gate Station",
              "transmissionname": "23kv Substation",
              "demandname": "12kv Substation",
              "nodenum": 60,
              "supplynum": 9,
              "trannum": 14,
              "demandnum": 37,
              "color": "red",
              "edgediameter": 5
              }

##Data for gas network
gas1para = {"name": "Gas",
              "supplyname": "Gas Gate Station",
              "transmissionname": "Regulator Station",
              "demandname": "Other",
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

Tractfile = r'.\data\Tract.xlsx' #the file is from https://www.usboundary.com/Areas/Census%20Tract/Tennessee/Shelby%20County

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
              "supplyname": "Power Gate Station",
              "demandname": "Power Deliver Station",
              "nodenum": 46,
              "supplynum": 9,
              "demandnum": 37,
              "color": "red"
              }

##Data for gas network in ouyangmin
gas2para = {"name": "Gas2",
              "supplyname": "Gas Gate Station",
              "demandname": "Gas Deliver Station",
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
                        "dependnum": 2}

para_wdemand2psupply = {"Name": "wdemand2psupply", 
                        "dependnum": 2}

para_pdemand2glink = {"Name": "pdemand2glink", 
                        "dependnum": 2}

para_pdemand2wlink = {"Name": "pdemand2wlink", 
                        "dependnum": 2}

para_pdemand2wpinterlink = {"Name": "pdemand2wpinterlink",
                       "dependnum": 2}


para_pdemand2gpinterlink = {"Name": "pdemand2gpinterlink",
                       "dependnum": 2}


##empirical data consumption of Tennessee residents:
Powerconsum_TN_Summer = [138.397, 128.021, 120.934, 115.901, 112.241, 111.863, 115.040, 121.131, 128.783, 136.020, 143.174, 151.053, 158.252, 166.463, 173.149, 176.206, 178.115, 178.175, 177.911, 176.168, 173.044, 167.535, 165.256, 158.750]
Powerconsum_TN_Spring = [105.517, 101.261, 98.33983, 97.02672, 97.05691, 100.2944, 106.1053, 119.5609, 131.4996, 133.6353, 130.7299, 128.0508, 126.466, 123.2436, 121.2362, 119.2439, 117.6893, 116.829, 117.2441, 117.9233, 119.3647, 124.2775, 126.2472, 120.791]
Powerconsum_TN_Autumn = [106.2034, 100.4001, 96.17396, 93.20814, 93.28361, 93.66848, 97.85685, 105.5619, 115.8932, 117.3648, 118.2931, 119.1534, 120.8815, 120.874, 122.7229, 122.6022, 122.4739, 121.8475, 123.0927, 123.9983, 128.6244, 129.0847, 125.6133, 119.0175]
Powerconsum_TN_Winter = [113.1161, 107.0713, 102.8376, 99.77369, 99.06431, 98.69452, 100.6189, 108.9655, 118.1346, 119.9835, 119.5081, 119.9231, 121.2061, 121.1834, 120.3986, 120.4967, 120.1344, 120.5495, 123.4398, 129.9224, 129.3639, 127.2282, 124.1568, 118.3157]
