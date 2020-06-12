# -*- coding: utf-8 -*-
"""
Created on Fri May 29 13:44:50 2020

@author: 10624
"""

"""This program sets up the objectives of the network generating using Ouyang's method
"""
import numpy as np
import Sharefunction as sf
import Basemapset as bm
import annealsimulation as ans
from matplotlib import pyplot as plt


class network2:
    def __init__(self, netdata,Geox, Geoy):
        
        self.name, self.supplyname, self.demandname = netdata["name"], netdata["supplyname"], netdata["demandname"]
        
        self.nodenum, self.supplynum, self.demandnum = netdata["nodenum"], netdata["supplynum"], netdata["demandnum"]
        
        self.color = netdata["color"]
        
        self.Geox = Geox
        self.Geoy = Geoy
        
        
        self.supplyseries = np.arange(0, self.supplynum, 1)
        self.demandseries = np.arange(self.supplynum + 1, self.nodenum, 1)
        
    
    def Nodeloc(self):
        """Generate the location of the network using method discussed in paper ouyang min and two other guys
        Input: Geox - the X coordinates of the Basemap
               Geoy - the y coordinates of the Basemap
               num - the number of vertices to be located
        
        Output: the interger location of the vertices
        """
        loc = []
        
        self.latl, self.lonl = [], []
        
        while(len(self.latl) != self.nodenum):
            lat = np.random.randint(len(self.Geoy) - 1)
            lon = np.random.randint(len(self.Geox) - 1)
            if(lat not in self.latl or lon not in self.lonl):
                self.latl.append(lat)
                self.lonl.append(lon)   
        
        self.loc = np.stack((np.array(self.latl), np.array(self.lonl))).transpose()
        self.Geoloc = np.stack((self.Geoy[self.loc[:, 0]], self.Geox[self.loc[:, 1]])).transpose()
        
    def Connect(self, m):
        """Connect the vertices generated in Function Nodeloc - generate the adjacent matrix
        Input:  m - the most m cloest facilities to be connected
               
        Output: distmatrix - the distance matrix of the vertices
                adjmatrix - the adjacent matrix of the vertices
        """
        self.distmatrix = np.zeros([len(self.loc), len(self.loc)])
        
        for i in range(len(self.loc)):
            for j in range(len(self.loc)):
                self.distmatrix[i, j] = sf.dist(self.Geoloc[i, 0], self.Geoloc[i, 1], self.Geoloc[j, 0], self.Geoloc[j, 1])
        
        #Calculate the adjacent matrix
        self.adjmatrix = np.zeros([len(self.loc), len(self.loc)])
        
        for i in range(len(self.demandseries)):
            minindex = np.array(sf.minimumk(self.distmatrix[:self.demandseries[i], self.demandseries[i]], m))
            self.adjmatrix[minindex, self.demandseries[i]] = 1
    
    def degreeNdegree(self):
        """Calculate the degree sequence and nodal neighborhood degree
        """
        self.degree = np.sum(self.adjmatrix, axis = 1)
        self.Ndegree = np.zeros(len(self.degree), dtype = int)
        for i in range(len(self.degree)):
            Temp = 0
            for j in range(len(self.degree)):
                Temp += self.degree[j]*self.adjmatrix[i, j]
            self.Ndegree[i] = Temp
    
    def scatternetwork(self, Type1, llon, rlon, llat, rlat):
        """Scatter the facility on the basemap
        """
        bm.BaseMapSet(Type1, llon, rlon, llat, rlat)
        
        plt.scatter(self.Geoloc[0:self.supplynum, 1], self.Geoloc[0:self.supplynum, 0], 400, self.color, marker = '+', label = self.supplyname)
        plt.scatter(self.Geoloc[self.supplynum:, 1], self.Geoloc[self.supplynum:, 0], 100, self.color, marker = 'o', label = self.demandname)
        
        plt.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1, fontsize = 25, frameon = 0)
        
        plt.show()

    def plotnetwork(self, Type1, llon, rlon, llat, rlat):
        """Plot the figure of the networks
        """
        bm.BaseMapSet(Type1, llon, rlon, llat, rlat)
        
        plt.scatter(self.Geoloc[0:self.supplynum, 1], self.Geoloc[0:self.supplynum, 0], 400, self.color, marker = '+', label = self.supplyname)
        plt.scatter(self.Geoloc[self.supplynum:, 1], self.Geoloc[self.supplynum:, 0], 100, self.color, marker = 'o', label = self.demandname)
        
        for i in range(len(self.adjmatrix)):
            for j in range(len(self.adjmatrix)):
                if(self.adjmatrix[i, j] == 1):
                    plt.plot([self.Geoloc[i, 1], self.Geoloc[j, 1]], [self.Geoloc[i, 0], self.Geoloc[j, 0]], 'black', lw = 1)
    
        plt.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1, fontsize = 25, frameon = 0)
        
    def cost_cal(self, Type, Tract_pop, Tractx, Tracty):
        """Calculate the normalized demand-population cost
        """
        Geox1 = sf.FeatureScaling(self.Geox)
        Geoy1 = sf.FeatureScaling(self.Geoy)
        Tract_pop1 = sf.FeatureScaling(Tract_pop)
        Tractx1 = sf.FeatureScaling(Tractx)
        Tracty1 = sf.FeatureScaling(Tracty)
        
        self.cost = ans.cost(self.loc[self.supplynum:, :], Geox1, Geoy1, Tract_pop1, Type, Tractx1, Tracty1)
        
    def NPL(self):
        """Calculate the normalized physical length of all edges in the network
        """
        self.edge = np.zeros((np.int(np.sum(self.adjmatrix)), 3))
        Temp = 0
        for i in range(self.nodenum):
            for j in range(self.nodenum):
                if(self.adjmatrix[i, j] == 1):
                    self.edge[Temp, 0], self.edge[Temp, 1], self.edge[Temp, 2] = i, j, self.distmatrix[i, j]
                    Temp += 1
        
        self.Totallength = ((np.max(self.Geox) - np.min(self.Geox))**2 + (np.max(self.Geoy) - np.min(self.Geoy))**2)**0.5
        self.norm_edge = self.edge[:, 2]/self.Totallength
        
    def pathij(self, i, j, pathlist):
        """Perform the DFS to find all paths between nodes i and j
        Input: i - path starting from node i
               j - path ending at node j
        """
        import math
        path = []
        
        visit = np.zeros(self.nodenum)
        
        self.DFS(i, j, visit, path, pathlist)
        
        return pathlist
    
    def DFS(self, i, j, visit, path, pathlist):
        import copy
        
        visit[i] = 1
        path.append(i)
        if(i == j):
            pathlist.append(copy.copy(path))
        else:
            for k in range(len(self.adjmatrix[i, :])):
                if(self.adjmatrix[i, k] == 1 and visit[k] == 0):
                    self.DFS(k, j, visit, path, pathlist)
    
        path.pop()
        visit[i] = 0
        
    def topo_shortestpathij(self, i, j):
        """Find the shortest path between node i and j and calculate its topo distance
        """
        pathlist = []
        self.pathij(i, j, pathlist)
        distance = []
        
        for i in range(len(pathlist)):
            distance.append(len(pathlist[i]) - 1)
        
        if(len(distance) == 0):
            return None
        else:
            return min(distance)
    
    def shortestpathij(self, i, j):
        """Find the spatial distance of the shortest path between node i and j
        """
        pathlist = []
        self.pathij(i, j, pathlist)
        distance = []
        
        for i in range(len(pathlist)):
            Temp = 0
            for j in range(len(pathlist[i]) - 1):
                Temp += self.distmatrix[pathlist[i][j], pathlist[i][j+1]]
            distance.append(Temp)
        
        if(len(distance) == 0):
            return None
        else:
            return min(distance)
    
    def topo_efficiency_cal(self):
        """Calculate the topological efficiency of the infrastructure networks
        """
        Temp = 0
        for i in self.supplyseries:
            for j in self.demandseries:
                if(self.topo_shortestpathij(i, j) == None):
                    continue
                Temp += 1/self.topo_shortestpathij(i, j)
                
        self.topo_efficiency = 1/(self.supplynum*self.demandnum)*Temp
        
    def efficiency_cal(self):
        """Calculate the spatial efficiency of the infrastructure networks
        """
        Temp = 0
        for i in self.supplyseries:
            for j in self.demandseries:
                if(self.shortestpathij(i, j) == None):
                    continue
                Temp += 1/self.shortestpathij(i, j)
                
        self.efficiency = 1/(self.supplynum*self.demandnum)*Temp
        
    def cluster_cal(self):
        """calculate the average cluster coefficient of the graph
        """
        self.Cluster = []
        for i in range(self.nodenum):
            neighborhood_node = self.neighbor_node(i)
            Node_num = len(neighborhood_node)
            Count = self.neighbor_edge(neighborhood_node)
            if(Node_num == 0 or Node_num == 1):
                self.Cluster.append(1)
            else:
                self.Cluster.append(Count/(Node_num*(Node_num - 1)))
        
        self.cluster_coeff = np.average(self.Cluster)
            
    def neighbor_node(self, node):
        """return the neighborhood nodes of node i
        """
        neighborhood_node = []
        for i in range(self.nodenum):
            if(self.adjmatrix[node, i] == 1):
                neighborhood_node.append(i)
        
        return neighborhood_node
    
    def neighbor_edge(self, neighborhood_node):
        """Count the number of edges between the neighborhood nodes of the specific node
        """
        Temp = 0
        for node1 in neighborhood_node:
            for node2 in neighborhood_node:
                if(self.adjmatrix[node1, node2] == 1):
                    Temp += 1
        return Temp
    
    def topo_diameter(self):
        """The topological diameter of a network
        """
        import math
        
        Temp = 0
        for i in range(self.nodenum):
            for j in range(self.nodenum):
                pathlist = []
                self.pathij(i, j, pathlist)
                distance = []
                
                for k in range(len(pathlist)):
                    distance.append(len(pathlist[k]) - 1)
                
                if(len(distance) == 0):
                    continue
                else:
                    if(min(distance) >= Temp):
                        Temp = min(distance)
        
        self.topodiameter = Temp
        
    def spatial_diameter(self):
        """The spatial diameter of a network
        """
        import math
        
        Temp = 0
        for i in range(self.nodenum):
            for j in range(self.nodenum):
                pathlist = []
                self.pathij(i, j, pathlist)
                distance = []
                
                for k in range(len(pathlist)):
                    Temp2 = 0
                    for m in range(len(pathlist[k]) - 1):
                        Temp2 += self.distmatrix[pathlist[k][m], pathlist[k][m+1]]
                    distance.append(Temp2)
                
                if(len(distance) == 0):
                    continue
                else:
                    if(min(distance) >= Temp):
                        Temp = min(distance)
        
        self.diameter = Temp
        
    def cal_topology_feature(self):
        """Calculate the topology features of the network
        edge length
        topo_efficiency
        efficiency
        cluster_coefficient
        topology_ diameter
        diameter
        """
        self.NPL()
        self.topo_efficiency_cal()
        self.efficiency_cal()
        self.cluster_cal()
        self.topo_diameter()
        self.spatial_diameter()