# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 14:23:34 2020

@author: 10624
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import data as dt

def loadcsvtimedata(name, num, season):
    """ Load the data through the time
    name: the type of the data we want to load
    num: num of the point
    season: string, spring, summer, autumn, winter
    """
    data = np.empty((num, 24), dtype = float)
    
    for i in range(24):
        tempdata = pd.read_csv("./optimized_result/" + season + "/" + name + str(i) + ".csv", header = None)
        for j in range(num):
            data[j, i] = tempdata[0][j]
    
    return data

def visualchangeday(data, changeunit, ylabel, xlabel, curvelabel):
    """ Visualize the change of decision variables throughout a day
    Input: data - 2D numpy array of float64 entry, 1st D - the number of the facilities or pipelines, 2nd D - the daytime
    """
    for i in range(len(data)):
        plt.plot(np.arange(0, 24, 1), data[i]*changeunit, label = curvelabel+ " " +str(i+1), marker = 'o')

    # plt.xlabel(xlabel, fontsize = 15, fontweight = "bold")
    # plt.ylabel(ylabel, fontsize = 15, fontweight = "bold")
    # plt.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1, fontsize = 12, frameon = 0)
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.grid()
    

def iterjulia2python(path):
    """ Convert the julia optimization results along the time to python array to be easily visualize
    Input:
        path - the path of the julia optimization result
    """
    import numpy as np
    
    A = np.loadtxt(path, dtype = object)
    data = []
    for i in range(len(A)):
        if(A[i,0] == 'iter' or A[i, 0] == 'In'):
            continue
        
        data.append([float(A[i, 1]), float(A[i, 2]), float(A[i, 3]), float(A[i, 4])])
    
    return np.array(data)


#Pload
sea = "summer"
data = loadcsvtimedata("Pload", 9, "winter")
visualchangeday(data, 3600*1000/1000000, "Power load (MW)", "Time (hours)", "Power plant")
plt.plot(np.arange(0,24,1), dt.Powerconsum_TN_Winter, lw = 8, label = 'Power consumption in Winter', alpha = 0.7, linestyle = '--', color = 'k')
# plt.plot(np.arange(0,24,1), Powerconsum_TN_Summer, lw = 8, label = 'Power consumption in Summer', alpha = 0.7, linestyle = ':', color = 'k')
# plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.35), ncol=3, shadow=False, frameon = 0)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.title("Power Load of Gate Stations (MW)", fontsize = 15, fontweight = 'bold')
plt.savefig("./powerloadchangedaywinter.pdf", dpi = 1500, bbox_inches='tight', pad_inches=0)

###opt num = 5
optnum = 5
for i in range(optnum):
    data = iterjulia2python('./optimized_result/optiter' + str(i + 1) + '.txt')
    plt.plot(np.arange(0, len(data[:, 0]), 1), np.log(data[:, 0]), label = str(i + 1) + ' - optimization')
plt.xlabel('Iteration number', fontsize = 15, fontweight = 'bold')
plt.ylabel('Objective value (log scale)', fontsize = 15, fontweight = 'bold')
plt.legend(fontsize = 14, frameon = 0)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.grid()
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.savefig("./Objectivevalue.pdf", dpi = 1500, bbox_inches='tight', pad_inches=0)

###opt num = 5
optnum = 5
for i in range(optnum):
    data = iterjulia2python('./optimized_result/optiter' + str(i + 1) + '.txt')
    plt.plot(np.arange(0, len(data[500:, 0]), 1), data[500:, 0], label = str(i) + ' - optimization')
plt.xlabel('Iteration number', fontsize = 15, fontweight = 'bold')
plt.ylabel('Objective value', fontsize = 15, fontweight = 'bold')
# plt.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1, fontsize = 12, frameon = 0)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.grid()


#Wflow
Wflow = loadcsvtimedata("Wflow", 109, "winter")
for i in range(len(Wflow)):
    plt.plot(np.arange(0, len(Wflow[i, :]), 1), Wflow[i, :], marker = 'o')
plt.xlabel('Time (hours)', fontsize = 15, fontweight = 'bold')
plt.ylabel('Water flow (m^3/s)', fontsize = 15, fontweight = 'bold')
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
red_patch = mpatches.Patch(color = 'k', label = 'The capacity of the 0.6m(dia) pipeline (black)')
black_patch = mpatches.Patch(color = 'r', label = 'Water flow (all other color)')
# plt.legend(handles = [red_patch], loc='upper center', bbox_to_anchor=(0.5, 1.12), ncol=3, shadow=False, frameon = 0)

plt.grid()
# plt.plot(np.arange(0, len(Wflow[i, :]), 1), [1.1356]*len(Wflow[i, :]), lw = 8, linestyle = '--', color = 'k')
plt.savefig("./Waterflowwinter.pdf", dpi = 1500, bbox_inches='tight', pad_inches=0)



#WPflow
WPflow = loadcsvtimedata("WPflow", 18, "winter")
for i in range(len(WPflow)):
    plt.plot(np.arange(0, len(WPflow[i, :]), 1), WPflow[i, :], marker = 'o')
# plt.plot(np.arange(0, len(Wflow[i, :]), 1), [1.1356]*len(Wflow[i, :]), lw = 8, linestyle = '--', color = 'k')
red_patch = mpatches.Patch(color = 'k', label = 'The capacity of the 0.6m(dia) pipeline (black)')
black_patch = mpatches.Patch(color = 'r', label = 'Water flow (all other color)')
# plt.legend(handles = [red_patch], loc='upper center', bbox_to_anchor=(0.5, 1.12), ncol=3, shadow=False, frameon = 0)
# plt.xlabel('Time (hours)', fontsize = 15, fontweight = 'bold')
# plt.ylabel('Water flow(m^3/s)', fontsize = 15, fontweight = 'bold')
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.grid()
plt.title("Water Flow along Water Pipelines (m^3/s)", fontsize = 15, fontweight = 'bold')
plt.savefig("./Waterpowerflowwinter.pdf", dpi = 1500, bbox_inches='tight', pad_inches=0)


    
#Gpr
Gpr = loadcsvtimedata("Gpr", 16, "winter")
for i in range(len(Gpr)):
    plt.plot(np.arange(0, len(Gpr[i, :]), 1), Gpr[i, :], marker = 'o')
# plt.plot(np.arange(0, len(Gpr[i, :]), 1), [200]*len(Gpr[i, :]), lw = 5, linestyle = ':', color = 'k', label = 'Gas pressure lower bound')
# plt.plot(np.arange(0, len(Gpr[i, :]), 1), [1500]*len(Gpr[i, :]), lw = 5, linestyle = '--', color = 'k', label = 'Gas pressure upper bound')
plt.xlabel('Time (hours)', fontsize = 15, fontweight = 'bold')
# plt.ylabel('Gas pressure(psi)', fontsize = 15, fontweight = 'bold')
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.grid()
plt.title("Gas Pressure along Gas Pipelines (psi)", fontsize = 15, fontweight = 'bold')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3, shadow=False, frameon = 0)
plt.savefig("./Gaspressurewinter.pdf", dpi = 1500, bbox_inches='tight', pad_inches=0)

    