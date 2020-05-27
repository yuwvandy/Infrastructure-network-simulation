# -*- coding: utf-8 -*-
"""
Created on Sat May 23 12:05:38 2020

@author: 10624
"""
"""
This file contains function shared by all other program files. All functions here are the general functions
"""
import numpy as np
from matplotlib import pyplot as plt
import Basemapset as bm

def FeatureScaling(A):
    return ((A-np.min(A))/(np.max(A)-np.min(A)))

def dist(node1y, node1x, node2y, node2x):
    return ((node1y - node2y)**2+(node1x - node2x)**2)**0.5/1000 #m -> km

def minimumk(sequence, k):
    """return the minimum k elements in the sequence
    """
    list1 = []
    sequence2 = np.sort(sequence)
    for i in range(k):
        element = sequence2[i]
        list1.append(list(sequence).index(element))
    
    return list1

def degreeNdegree(Adjmatrix):
    """Given the adjacent matrix of a network, return the degree and nodal neighborhood degree sequence
    """
    degree = np.sum(Adjmatrix, axis = 1)
    Ndegree = np.zeros(len(degree), dtype = int)
    for i in range(len(degree)):
        Temp = 0
        for j in range(len(degree)):
            Temp += degree[j]*Adjmatrix[i, j]
        Ndegree[i] = Temp
    
    return degree, Ndegree

def scatternetwork(geoloc, supplynum, color, supplyname, demandname):
    """Scatter the facility on the basemap
    """
    plt.scatter(geoloc[0:supplynum, 1], geoloc[0:supplynum, 0], 400, color, marker = '+', label = supplyname)
    plt.scatter(geoloc[supplynum:, 1], geoloc[supplynum:, 0], 100, color, marker = 'o', label = demandname)

    plt.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1, fontsize = 25, frameon = 0)
    
    plt.show()
    
def plotnetwork(geoloc, supplynum, color, supplyname, demandname, adjmatrix):
    """Plot the figure of the networks
    """
    plt.scatter(geoloc[0:supplynum, 1], geoloc[0:supplynum, 0], 400, color, marker = '+', label = supplyname)
    plt.scatter(geoloc[supplynum:, 1], geoloc[supplynum:, 0], 100, color, marker = 'o', label = demandname)

    for i in range(len(adjmatrix)):
        for j in range(len(adjmatrix)):
            if(adjmatrix[i, j] == 1):
                plt.plot([geoloc[i, 1], geoloc[j, 1]], [geoloc[i, 0], geoloc[j, 0]], 'black', lw = 1)

    plt.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1, fontsize = 25, frameon = 0)
    
#def decompose(degree, d):
#    """Given the number of the total degree and the number of vertices, output the degree list
#    """
#    import math
#    
#    degreelist = np.zeros(d)
#    temp = math.floor(degree/d)
#    Temp = 0
#    for i in range(d - 1):
#        if(i%2 == 0):
#            degreelist[i] = temp
#            Temp += temp
#        else:
#            degreelist[i] = temp + 1
#            Temp += temp + 1
#            
#    degreelist[-1] = degree - Temp
#    print(degreelist)
#    
#    return degreelist
