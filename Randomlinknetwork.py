# -*- coding: utf-8 -*-
"""
Created on Mon May 25 21:03:35 2020

@author: 10624
"""
import numpy as np
import Sharefunction as sf

def Nodeloc(Geox, Geoy, num):
    """Generate the location of the network using method discussed in paper ouyang min and two other guys
    Input: Geox - the X coordinates of the Basemap
           Geoy - the y coordinates of the Basemap
           num - the number of vertices to be located
    
    Output: the interger location of the vertices
    """
    loc = []
    
    for i in range(num):
        loc.append([np.random.randint(0, len(Geoy)), np.random.randint(0, len(Geox))])
    
    return np.array(loc)
    
def Connect(loc, m, sourcenum):
    """Connect the vertices generated in Function Nodeloc - generate the adjacent matrix
    Input: loc - vertex location geographically
           m - the most m cloest facilities to be connected
           
    Output: distmatrix - the distance matrix of the vertices
            adjmatrix - the adjacent matrix of the vertices
    """
    distmatrix = np.zeros([len(loc), len(loc)])
    
    for i in range(len(loc)):
        for j in range(len(loc)):
            distmatrix[i, j] = sf.dist(loc[i, 0], loc[i, 1], loc[j, 0], loc[j, 1])
    
    #Calculate the adjacent matrix
    adjmatrix = np.zeros([len(loc), len(loc)])
    
    for i in range(len(distmatrix) - sourcenum):
        index = sorted(range(len(distmatrix[i + sourcenum, :])), key=lambda k: distmatrix[i + sourcenum, :][k])
        adjmatrix[i + sourcenum, index[0:m]] = 1
        adjmatrix[index[0:m], i + sourcenum] = 1
        
    return distmatrix, adjmatrix