# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 09:43:47 2020

@author: 10624
"""
import numpy as np
import Sharefunction as sf

#----------------------------------------------phynode2node dependency
class phynode2node:
    def __init__(self, network1, network2, interpara):
        """Define the object of the physical dependency between nodes and nodes
        Input: network1, network2 - two python objects, network1 serves for network2
               interpara - dictionary, the parameters for defining interdependency between network1 and network2
        Output: the object of physical interdependency
        """
        self.name = interpara["Name"]
        self.nodenum1, self.nodenum2 = network1.demandnum, network2.supplynum
        self.network1, self.network2 = network1, network2
        
        self.nearestnum = interpara["dependnum"]
        
        self.Distmatrix()
        self.Adjmatrix()
    
    def Distmatrix(self):
        """Define the distance matrix of this dependency
        Ex: self.distmatrix[i, j] - the distance between node i in network1 and node j in network2
        Output: 2D numpy array, the distance matrix of the dependency
        """
        self.distmatrix = np.zeros((self.nodenum1, self.nodenum2), dtype = float)
        
        for i in range(self.nodenum1):
            for j in range(self.nodenum2):
                self.distmatrix[i, j] = sf.dist(self.network1.y[self.network1.demandseries[i]], self.network1.x[self.network1.demandseries[i]], \
                                                self.network2.y[self.network2.supplyseries[j]], self.network2.x[self.network2.supplyseries[j]])
        
    def Adjmatrix(self):
        """Define the adjacent matrix of this dependency
        Input: \
        Output: 2D numpy array, the adjacent matrix of the dependency
        """
        self.adjmatrix = np.zeros((self.nodenum1, self.nodenum2), dtype = int)
        
        for i in range(self.nodenum2):
            minindex = np.array(sf.minimumk(self.distmatrix[:, i], self.nearestnum))
            self.adjmatrix[minindex, i] = 1


#-----------------------------------------------------phynode2link dependency
class phynode2link():
    def __init__(self, network1, network2, interpara):
        """Define the object of the physical dependency between nodes and links
        Input: network1, network2 - two python objects, network1 serves for network2
        Output: the object of physical interdependency
        """
        self.name = interpara["Name"]
        self.nodenum1, self.linknum2 = network1.demandnum, len(network2.edgelist)
        self.network1, self.network2 = network1, network2
        
        self.nearestnum = interpara["dependnum"]
        
        self.Distmatrix()
        self.Adjmatrix()
    
    def Distmatrix(self):
        """Define the distance matrix of this dependency
        Ex: self.distmatrix[i, j] - the distance between node i in network1 and middle point of link j in network2
        Output: 2D numpy array, the distance matrix of the dependency
        """
        self.distmatrix = np.zeros((self.nodenum1, self.linknum2), dtype = float)
        
        for i in range(self.nodenum1):
            for j in range(self.linknum2):
                self.distmatrix[i, j] = sf.dist(self.network1.y[self.network1.demandseries[i]], self.network1.x[self.network1.demandseries[i]], \
                                                self.network2.edgelist[j]["middley"], self.network2.edgelist[j]["middlex"])
                
    def Adjmatrix(self):
        """Define the adjacent matrix of this dependency
        Input: \
        Output: 2D numpy array, the adjacent matrix of the dependency
        """
        self.adjmatrix = np.zeros((self.nodenum1, self.linknum2), dtype = int)
        
        for i in range(self.linknum2):
            minindex = np.array(sf.minimumk(self.distmatrix[:, i], self.nearestnum))
            self.adjmatrix[minindex, i] = 1
    

        