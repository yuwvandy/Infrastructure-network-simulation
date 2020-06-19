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
        self.create_edgelist()
    
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
    
    def create_edgelist(self):
        """Define the edge list of the interdependent networks
        Input: the adjacent matrix of the network
        Output: the edge list of the network: list of python dictionary, the dimenstion of the list is the number of edges, the dictionary has the following keys
                [start node, end node, network1, network2, length, edgediameter, X of the middle point, Y of the middle point] 
        """
        self.edgelist = []
        
        for i in range(self.nodenum1):
            for j in range(self.nodenum2):
                if(self.adjmatrix[i, j] == 1):
                    middlex = 0.5*(self.network1.x[self.network1.demandseries[i]] + self.network2.x[self.network2.supplyseries[j]])
                    middley = 0.5*(self.network1.y[self.network1.demandseries[i]] + self.network2.y[self.network2.supplyseries[j]])
                    self.edgelist.append({"start node": i, "end node": j, 
                                          "start node in network1": self.network1.demandseries[i], "end node in network2": self.network2.supplyseries[j], 
                                          "network1": self.network1.name, "network2": self.network2.name, 
                                          "link length": self.distmatrix[i, j], "edgediameter": self.network1.edgediameter, 
                                          "middlex": middlex, "middley": middley})
                    


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
        self.link2node()
    
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
    
    def link2node(self):
        """Define the link2nodeid, given the link number, output the node id on the two ends of the link
        """
        self.link2nodeid = np.zeros((self.linknum2, 2), dtype = int)
        
        for i in range(self.linknum2):
            self.link2nodeid[i, 0] = self.network2.edgelist[i]["start node"]
            self.link2nodeid[i, 1] = self.network2.edgelist[i]["end node"]
            
        
            
#-----------------------------------------------------phynode2interlink dependency
class phynode2interlink():
    def __init__(self, internet1net2, network3, interpara):
        """Define the object of the physical dependency between nodes and interdependent links
        Input: internet1net2 - the dependency of network2 on network1
               network3 - the network on which the interdependency of network1 and network2 depends
        Output: the object of physical dependency of interdependency of network1 and network2 on network3
        """
        self.name = interpara["Name"]
        self.internet1net2 = internet1net2
        self.network1, self.network2, self.network3 = internet1net2.network1, internet1net2.network2, network3
        self.nodenum1, self.nodenum2, self.nodenum3 = self.network1.demandnum, self.network2.supplynum, self.network3.demandnum
        self.linknum = len(self.internet1net2.edgelist)
        
        self.nearestnum = interpara["dependnum"]
        
        self.Distmatrix()
        self.Adjmatrix()
        self.link2node()
    
    def Distmatrix(self):
        """Define the distance matrix of this dependency
        Ex: self.distmatrix[i, j] - the distance between node i in network3 and middle point of link j in internet from network1 to network2
        Output: 2D numpy array, the distance matrix of the dependency
        """
        self.distmatrix = np.zeros((self.nodenum3, self.linknum), dtype = float)
        
        for i in range(self.nodenum3):
            for j in range(self.linknum):
                self.distmatrix[i, j] = sf.dist(self.network3.y[self.network3.demandseries[i]], self.network3.x[self.network3.demandseries[i]], \
                                                self.internet1net2.edgelist[j]["middley"], self.internet1net2.edgelist[j]["middlex"])
                
    def Adjmatrix(self):
        """Define the adjacent matrix of this dependency
        Input: \
        Output: 2D numpy array, the adjacent matrix of the dependency
        """
        self.adjmatrix = np.zeros((self.nodenum3, self.linknum), dtype = int)
        
        for i in range(self.linknum):
            minindex = np.array(sf.minimumk(self.distmatrix[:, i], self.nearestnum))
            self.adjmatrix[minindex, i] = 1
            
    def link2node(self):
        """Define the link2nodeid, given the link number, output the node id on the two ends of the link
        """
        self.link2nodeid = np.zeros((self.linknum, 2), dtype = int)
        
        for i in range(self.linknum):
            self.link2nodeid[i, 0] = self.internet1net2.edgelist[i]["start node"]
            self.link2nodeid[i, 1] = self.internet1net2.edgelist[i]["end node"]
    

        