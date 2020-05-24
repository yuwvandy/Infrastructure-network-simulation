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
        
        self.demandlat = np.random.randint(len(Geoy), size = self.demandnum, dtype = int)
        self.demandlon = np.random.randint(len(Geox), size = self.demandnum, dtype = int)
        
        self.tranlat = np.random.randint(len(Geoy), size = self.trannum, dtype = int)
        self.tranlon = np.random.randint(len(Geox), size = self.trannum, dtype = int)
        
        self.supplylat = np.random.randint(len(Geoy), size = self.supplynum, dtype = int)
        self.supplylon = np.random.randint(len(Geox), size = self.supplynum, dtype = int)
        
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
        
    def drawlocation(self, Type, llon, rlon, llat, rlat):
        """Draw the map of the infrastructure system
        """
        bm.BaseMapSet(Type, llon, rlon, llat, rlat)
        
        plt.scatter(self.demandx, self.demandy, 100, self.color, marker = 'o', label = self.demandname)  
    
        plt.scatter(self.tranx, self.trany, 200, self.color, marker = '*', label = self.tranname) 
    
        plt.scatter(self.supplyx, self.supplyy, 400, self.color, marker = '+', label = self.supplyname) 
    
        plt.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1, fontsize = 25)
    
    def connection(self):
        
        