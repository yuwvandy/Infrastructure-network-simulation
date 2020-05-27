# -*- coding: utf-8 -*-
"""
Created on Sat May 23 11:29:28 2020

@author: 10624
"""
import Sharefunction as sf
import numpy as np
import Basemapset as bm
from matplotlib import pyplot as plt

class network:
    """Initiate the class of the network
    """
    def __init__(self, name, supplyname, tranname, demandname, nodenum, supplynum, trannum, demandnum, color):
        
        self.name = name
        self.supplyname = supplyname
        self.tranname = tranname
        self.demandname = demandname
        
        self.nodenum = nodenum
        self.demandnum = demandnum
        self.trannum = trannum
        self.supplynum = supplynum
        
        self.demandseries = np.arange(self.supplynum + self.trannum, self.supplynum+self.trannum+self.demandnum, 1)
        self.transeries = np.arange(self.supplynum, self.supplynum+self.trannum, 1)
        self.supplyseries  = np.arange(0, self.supplynum, 1)
        
        
        self.color = color
    
    def Nodelocation(self, Geox, Geoy, Tract_pop, Tractx, Tracty):
        """Annealing simulation to decide the node location
        """
        import annealsimulation
        
        self.demandlat = np.random.randint(len(Geoy) - 1, size = self.demandnum, dtype = int)
        self.demandlon = np.random.randint(len(Geox) - 1, size = self.demandnum, dtype = int)
        
        self.tranlat = np.random.randint(len(Geoy) - 1, size = self.trannum, dtype = int)
        self.tranlon = np.random.randint(len(Geox) - 1, size = self.trannum, dtype = int)
        
        self.supplylat = np.random.randint(len(Geoy) - 1, size = self.supplynum, dtype = int)
        self.supplylon = np.random.randint(len(Geox) - 1, size = self.supplynum, dtype = int)
        
        self.demandloc = np.stack((self.demandlat, self.demandlon)).transpose()
        self.tranloc = np.stack((self.tranlat, self.tranlon)).transpose()
        self.supplyloc = np.stack((self.supplylat, self.supplylon)).transpose()
        
        #Demand node
        Geox1 = sf.FeatureScaling(Geox)
        Geoy1 = sf.FeatureScaling(Geoy)
        Tract_pop1 = sf.FeatureScaling(Tract_pop)
        Tractx1 = sf.FeatureScaling(Tractx)
        Tracty1 = sf.FeatureScaling(Tracty)
        
        self.demandloc, self.demandc = annealsimulation.anneal2(self.demandloc, 'Population', Geox1, Geoy1, Tract_pop1, Tractx1, Tracty1)
        self.demandy1 = Geoy1[self.demandloc[:, 0]]
        self.demandx1 = Geox1[self.demandloc[:, 1]]
        self.demandy = Geoy[self.demandloc[:, 0]]
        self.demandx = Geox[self.demandloc[:, 1]]
        #Transmission node
        self.tranloc, self.tranc = annealsimulation.anneal2(self.tranloc, 'Facility', Geox1, Geoy1, Tract_pop1, self.demandx1, self.demandy1)
        self.trany1 = Geoy1[self.tranloc[:, 0]]
        self.tranx1 = Geox1[self.tranloc[:, 1]]
        self.trany = Geoy[self.tranloc[:, 0]]
        self.tranx = Geox[self.tranloc[:, 1]]

        #Supply node
        self.supplyloc, self.supplyc = annealsimulation.anneal2(self.supplyloc, 'Facility', Geox1, Geoy1, Tract_pop1, self.tranx1, self.trany1)
        self.supplyy1 = Geoy1[self.supplyloc[:, 0]]
        self.supplyx1 = Geox1[self.supplyloc[:, 1]]    
        self.supplyy = Geoy[self.supplyloc[:, 0]]
        self.supplyx = Geox[self.supplyloc[:, 1]]
        
        ##Coordinates of nodes
        self.y = np.concatenate((self.supplyy, self.trany, self.demandy))
        self.x = np.concatenate((self.supplyx, self.tranx, self.demandx))
        
    def drawlocation(self, Type, llon, rlon, llat, rlat):
        """Scatter the facility of the infrastructure system
        """
        bm.BaseMapSet(Type, llon, rlon, llat, rlat)
        
        plt.scatter(self.demandx, self.demandy, 100, self.color, marker = 'o', label = self.demandname)  
    
        plt.scatter(self.tranx, self.trany, 200, self.color, marker = '*', label = self.tranname) 
    
        plt.scatter(self.supplyx, self.supplyy, 400, self.color, marker = '+', label = self.supplyname) 
    
        plt.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1, fontsize = 25)
        
    def drawnetwork(self, Type, llon, rlon, llat, rlat):
        """Draw the network of the infrastructure system on the Basemap
        """
        bm.BaseMapSet(Type, llon, rlon, llat, rlat)
        
        plt.scatter(self.demandx, self.demandy, 100, self.color, marker = 'o', label = self.demandname)  
    
        plt.scatter(self.tranx, self.trany, 200, self.color, marker = '*', label = self.tranname) 
    
        plt.scatter(self.supplyx, self.supplyy, 400, self.color, marker = '+', label = self.supplyname) 
        
        for i in range(len(self.Adjmatrix)):
            for j in range(len(self.Adjmatrix)):
                if(self.Adjmatrix[i, j] == 1):
                    plt.plot([self.x[i], self.x[j]], [self.y[i], self.y[j]], 'black', lw = 1)
    
        plt.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1, fontsize = 25, frameon = 0)
    
    def Distmatrix(self):
        """Calculate the distance matrix for the vertices in the network
        """
        self.Dismatrix = np.zeros((self.nodenum, self.nodenum))
        for i in range(len(self.Dismatrix)):
            for j in range(len(self.Dismatrix)):
                self.Dismatrix[i, j] = sf.dist(self.y[i], self.x[i], self.y[j], self.x[j])
                self.Dismatrix[j, i] = self.Dismatrix[i, j]
        
    
    def connection(self, sampleseq, num):
        """Calculate the adjacent matrix between supply node and transmission node
        Input: the nodal neighborhood degree sequence, d: the number of adjacent nodes
        Output: the adjacent matrix between supply and transmission nodes
        """
        self.Adjmatrix = np.zeros((self.nodenum, self.nodenum), dtype = int)
        
        for i in range(self.supplynum):
            minindex = np.array(sf.minimumk(self.Dismatrix[self.supplyseries[i], self.transeries], sampleseq[self.supplyseries[i]])) + self.supplynum
            self.Adjmatrix[self.supplyseries[i], minindex] = 1
#            self.Adjmatrix[minindex, self.supplyseries[i]] = 1
        
#        for i in range(self.trannum):
#            if(np.sum(self.Adjmatrix[self.supplyseries, self.transeries[i]]) == 0):
#                minindex = np.array(sf.minimumk(self.Dismatrix[self.supplyseries, self.transeries[i]], 1))
#                self.Adjmatrix[minindex, self.transeries[i]] = 1
        
#        for i in range(self.supplynum):
#            minindex = np.array(sf.minimumk(self.Dismatrix[self.supplyseries[i], self.supplyseries], num))
#            self.Adjmatrix[self.supplyseries[i], minindex] = 1
#            self.Adjmatrix[minindex, self.supplyseries[i]] = 1
        
#        for i in range(self.trannum):
#            if(np.sum(self.Adjmatrix[self.supplyseries, self.transeries[i]]) != 0):
#                continue
#            minindex = np.array(sf.minimumk(self.Dismatrix[self.supplyseries, self.transeries[i]], num))
#            self.Adjmatrix[minindex, self.transeries[i]] = 1
##            self.Adjmatrix[self.transeries[i], minindex] = 1
#        
        for i in range(self.trannum):
            minindex = np.array(sf.minimumk(self.Dismatrix[self.transeries[i], self.demandseries], sampleseq[self.transeries[i]])) + self.supplynum + self.trannum
            self.Adjmatrix[self.transeries[i], minindex] = 1
#            self.Adjmatrix[minindex, self.transeries[i]] = 1
            
#        for i in range(self.demandnum):
#            if(np.sum(self.Adjmatrix[self.transeries, self.demandseries[i]]) == 0):
#                minindex = np.array(sf.minimumk(self.Dismatrix[self.transeries, self.demandseries[i]], 1)) + self.supplynum
#                self.Adjmatrix[minindex, self.demandseries[i]] = 1
        
#        for i in range(self.trannum):
#            minindex = np.array(sf.minimumk(self.Dismatrix[self.transeries[i], self.transeries], num)) + self.supplynum
#            self.Adjmatrix[self.transeries[i], minindex] = 1
        
        
        
#        for i in range(self.demandnum):
#            if(np.sum(self.Adjmatrix[self.transeries, self.demandseries[i]]) != 0):
#                continue
#            minindex = np.array(sf.minimumk(self.Dismatrix[self.transeries, self.demandseries[i]], num)) + self.supplynum
#            self.Adjmatrix[minindex, self.demandseries[i]] = 1
#            self.Adjmatrix[self.demandseries[i], minindex] = 1
        
        for i in range(self.demandnum):
            minindex = np.array(sf.minimumk(self.Dismatrix[self.demandseries[i], self.demandseries], sampleseq[self.demandseries[i]])) + self.supplynum + self.trannum
            self.Adjmatrix[self.demandseries[i], minindex] = 1
            self.Adjmatrix[minindex, self.demandseries[i]] = 1
        
        
#    def STconnection(self, neighdegree, d):
#        """Calculate the adjacent matrix between supply node and transmission node
#        Input: the nodal neighborhood degree sequence, d: the number of adjacent nodes
#        Output: the adjacent matrix between supply and transmission nodes
#        """
#        self.Adjmatrix = np.zeros((self.nodenum, self.nodenum))
#        self.degree = np.zeros(self.nodenum)
#        
#        for i in range(self.supplynum):
#            splitlist = sf.decompose(neighdegree[self.supplyseries[i]], d)
#            minindex = np.array(sf.minimumk(self.Dismatrix[self.supplyseries[i], self.transeries], len(splitlist))) + self.supplynum
#            for j in range(len(minindex)):
#                if(splitlist[j] >= self.degree[minindex[j]]):
#                    self.degree[minindex[j]] = splitlist[j]
#            self.Adjmatrix[self.supplyseries[i], minindex] = 1
##            self.degree[self.supplyseries[i]] = d
#    
#    def TDconnection(self, neighdegree, d):
#        """Calculate the adjacent matrix between transmission node and demand node
#        Input: the nodal neighborhood degree sequence, d: the number of adjacent nodes
#        Output: the adjacent matrix between transmission and demand nodes
#        """
#        for i in range(self.trannum):
#            splitlist = sf.decompose(neighdegree[self.transeries[i]], d)
#            minindex = np.array(sf.minimumk(self.Dismatrix[self.transeries[i], self.demandseries], len(splitlist))) + self.supplynum + self.trannum
#            for j in range(len(minindex)):
#                if(splitlist[j] >= self.degree[minindex[j]]):
#                    self.degree[minindex[j]] = splitlist[j]
#            self.Adjmatrix[self.transeries[i], minindex] = 1
##            self.degree[self.transeries[i]] = d
#        
        
        
        