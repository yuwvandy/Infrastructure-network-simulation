# -*- coding: utf-8 -*-
"""
Created on Sat May 23 11:29:28 2020

@author: 10624
"""
import Sharefunction as sf
import numpy as np
import Basemapset as bm
from matplotlib import pyplot as plt
import annealsimulation as ans
import data as dt

class network:
    """Initiate the class of the network
    """
    def __init__(self, netdata, Geox, Geoy):
        """Initialize the parameters of the networks and set up the background
        """
        #Name
        self.name, self.supplyname, self.tranname, self.demandname = netdata["name"], netdata["supplyname"], netdata["transmissionname"], netdata["demandname"]
        #Facility number
        self.nodenum, self.demandnum, self.trannum, self.supplynum = netdata["nodenum"], netdata["demandnum"], netdata["trannum"], netdata["supplynum"]
        
        #NodeSeries Number
        self.demandseries = np.arange(self.supplynum + self.trannum, self.supplynum+self.trannum+self.demandnum, 1)
        self.transeries = np.arange(self.supplynum, self.supplynum+self.trannum, 1)
        self.supplyseries  = np.arange(0, self.supplynum, 1)
        self.supplytranseries = np.concatenate((self.supplyseries, self.transeries))
        self.trandemandseries = np.concatenate((self.transeries, self.demandseries))
        
        self.edgediameter = netdata["edgediameter"]
        
        
        self.color = netdata["color"]
        self.Geox = Geox
        self.Geoy = Geoy
    
        
    def Nodelocation(self, Tract_pop, Tractx, Tracty, longitude, latitude):
        """Annealing simulation to decide the node location
        """
        import annealsimulation
        
        self.latl, self.lonl = [], []
        
        while(len(self.latl) != self.nodenum):
            lat = np.random.randint(len(self.Geoy) - 1)
            lon = np.random.randint(len(self.Geox) - 1)
            if(lat not in self.latl or lon not in self.lonl):
                self.latl.append(lat)
                self.lonl.append(lon)    
        
        self.latl, self.lonl = np.array(self.latl), np.array(self.lonl)
            
        self.demandlat, self.demandlon = self.latl[self.demandseries], self.lonl[self.demandseries]
        self.tranlat, self.tranlon = self.latl[self.transeries], self.lonl[self.transeries]
        self.supplylat, self.supplylon = self.latl[self.supplyseries], self.lonl[self.supplyseries]
        
        self.demandloc = np.stack((self.demandlat, self.demandlon)).transpose()
        self.tranloc = np.stack((self.tranlat, self.tranlon)).transpose()
        self.supplyloc = np.stack((self.supplylat, self.supplylon)).transpose()
        
        #Demand node
        Geox1 = sf.FeatureScaling(self.Geox)
        Geoy1 = sf.FeatureScaling(self.Geoy)
        Tract_pop1 = sf.FeatureScaling(Tract_pop)
        Tractx1 = sf.FeatureScaling(Tractx)
        Tracty1 = sf.FeatureScaling(Tracty)
        
        self.demandloc, self.demandc, self.popuassign = ans.anneal2(self.demandloc, 'Population', Geox1, Geoy1, Tract_pop1, Tractx1, Tracty1, Tract_pop)
        self.demandy1 = Geoy1[self.demandloc[:, 0]]
        self.demandx1 = Geox1[self.demandloc[:, 1]]
        self.demandy = self.Geoy[self.demandloc[:, 0]]
        self.demandx = self.Geox[self.demandloc[:, 1]]
        #Transmission node
        self.tranloc, self.tranc, temp = ans.anneal2(self.tranloc, 'Facility', Geox1, Geoy1, Tract_pop1, self.demandx1, self.demandy1, Tract_pop)
        self.trany1 = Geoy1[self.tranloc[:, 0]]
        self.tranx1 = Geox1[self.tranloc[:, 1]]
        self.trany = self.Geoy[self.tranloc[:, 0]]
        self.tranx = self.Geox[self.tranloc[:, 1]]

        #Supply node
        self.supplyloc, self.supplyc, temp = ans.anneal2(self.supplyloc, 'Facility', Geox1, Geoy1, Tract_pop1, self.tranx1, self.trany1, Tract_pop)
        self.supplyy1 = Geoy1[self.supplyloc[:, 0]]
        self.supplyx1 = Geox1[self.supplyloc[:, 1]]    
        self.supplyy = self.Geoy[self.supplyloc[:, 0]]
        self.supplyx = self.Geox[self.supplyloc[:, 1]]
        
        ##Coordinates of nodes
        self.y = np.concatenate((self.supplyy, self.trany, self.demandy))
        self.x = np.concatenate((self.supplyx, self.tranx, self.demandx))
        
        ##Latitudes and longitudes of nodes
        self.demandlatitude, self.demandlongitude = latitude[self.demandloc[:, 0]], longitude[self.demandloc[:, 1]]
        self.tranlatitude, self.tranlongitude = latitude[self.tranloc[:, 0]], longitude[self.tranloc[:, 1]]
        self.supplylatitude, self.supplylongitude = latitude[self.supplyloc[:, 0]], longitude[self.supplyloc[:, 1]]
        
        self.latitude = np.concatenate((self.supplylatitude, self.tranlatitude, self.demandlatitude))
        self.longitude = np.concatenate((self.supplylongitude, self.tranlongitude, self.demandlongitude))
    
    def GoogleAPIele(self):
        """Get the elevation data based on the latitude and longitude from Google API
        """
        import urllib.request
        import json
        
        self.elevation = []
        Base_url = "https://maps.googleapis.com/maps/api/elevation/json?locations="
        APIkey = "&key=AIzaSyDOo1DAojYoYf3WCcadLrsl9PZbnougbtE"
        
        for i in range(self.nodenum):
            Para_url = "%s,%s" % (self.latitude[i], self.longitude[i])
            url = Base_url + Para_url + APIkey
            
            with urllib.request.urlopen(url) as f:
                response = json.loads(f.read().decode())
            
            self.elevation.append(response['results'][0]['elevation'])
            
        
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
            minindex = np.array(sf.minimumk(self.Dismatrix[self.supplyseries[i], self.trandemandseries], sampleseq[self.supplyseries[i]]))
            self.Adjmatrix[self.supplyseries[i], self.trandemandseries[minindex]] = 1
#            self.Adjmatrix[minindex, self.supplyseries[i]] = 1
        
        for i in range(self.trannum):
            if(np.sum(self.Adjmatrix[self.supplyseries, self.transeries[i]]) == 0):
                minindex = np.array(sf.minimumk(self.Dismatrix[self.supplyseries, self.transeries[i]], 1))
                self.Adjmatrix[minindex, self.transeries[i]] = 1
#                self.Adjmatrix[self.transeries[i], minindex] = 1
                
        
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
            minindex = np.array(sf.minimumk(self.Dismatrix[self.transeries[i], self.demandseries], min(sampleseq[self.transeries[i]], self.demandnum))) + self.supplynum + self.trannum
            self.Adjmatrix[self.transeries[i], minindex] = 1
#            self.Adjmatrix[minindex, self.transeries[i]] = 1
            
#        for i in range(self.demandnum):
#            if(np.sum(self.Adjmatrix[self.transeries, self.demandseries[i]]) == 0):
#                minindex = np.array(sf.minimumk(self.Dismatrix[self.transeries, self.demandseries[i]], 1)) + self.supplynum
#                self.Adjmatrix[minindex, self.demandseries[i]] = 1
        
#        for i in range(self.trannum):
#            minindex = np.array(sf.minimumk(self.Dismatrix[self.transeries[i], self.transeries], num)) + self.supplynum
#            self.Adjmatrix[self.transeries[i], minindex] = 1
        
        for i in range(self.demandnum):
            if(np.sum(self.Adjmatrix[self.transeries, self.demandseries[i]]) == 0):
                minindex = np.array(sf.minimumk(self.Dismatrix[self.transeries, self.demandseries[i]], num)) + self.supplynum
                self.Adjmatrix[minindex, self.demandseries[i]] = 1
#            self.Adjmatrix[self.demandseries[i], minindex] = 1
        
        for i in range(self.demandnum):
            minindex = np.array(sf.minimumk(self.Dismatrix[self.demandseries[i], self.demandseries], min(sampleseq[self.demandseries[i]] + 1, self.demandnum))) + self.supplynum + self.trannum
            minindex = minindex[1:-1]
            for j in range(len(minindex)):
                if(self.Adjmatrix[self.demandseries[i], minindex[j]] == 1 or self.Adjmatrix[minindex[j], self.demandseries[i]] == 1):
                    continue
                self.Adjmatrix[self.demandseries[i], minindex[j]] = 1
#            self.Adjmatrix[minindex, self.demandseries[i]] = 1
        
        
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
                
    def create_edgelist(self):
        """Define the edge list of the network
        Input: the adjacent matrix of the network
        Output: the edge list of the network: list of python dictionary, the dimenstion of the list is the number of edges, the dictionary has the following keys
                [start node, end node, length, edgediameter, X of the middle point, Y of the middle point] 
        """
        self.edgelist = []
        
        for i in range(len(self.Adjmatrix)):
            for j in range(len(self.Adjmatrix)):
                if(self.Adjmatrix[i, j] == 1):
                    middlex = 0.5*(self.x[i] + self.x[j])
                    middley = 0.5*(self.y[i] + self.y[j])
                    self.edgelist.append({"start node": i, "end node": j, "link length": self.Dismatrix[i, j], "edgediameter": self.edgediameter, "middlex": middlex, "middley": middley})
                    
    def NPL(self):
        """Calculate the normalized physical length of all edges in the network
        """
        self.edge = np.zeros((np.sum(self.Adjmatrix), 3))
        Temp = 0
        for i in range(self.nodenum):
            for j in range(self.nodenum):
                if(self.Adjmatrix[i, j] == 1):
                    self.edge[Temp, 0], self.edge[Temp, 1], self.edge[Temp, 2] = i, j, self.Dismatrix[i, j]
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
            for k in range(len(self.Adjmatrix[i, :])):
                if(self.Adjmatrix[i, k] == 1 and visit[k] == 0):
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
                Temp += self.Dismatrix[pathlist[i][j], pathlist[i][j+1]]
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
                self.Cluster.append(0.5)
            else:
                self.Cluster.append(Count/(Node_num*(Node_num - 1)))
        
        self.cluster_coeff = np.average(self.Cluster)
            
    def neighbor_node(self, node):
        """return the neighborhood nodes of node i
        """
        neighborhood_node = []
        for i in range(self.nodenum):
            if(self.Adjmatrix[node, i] == 1):
                neighborhood_node.append(i)
        
        return neighborhood_node
    
    def neighbor_edge(self, neighborhood_node):
        """Count the number of edges between the neighborhood nodes of the specific node
        """
        Temp = 0
        for node1 in neighborhood_node:
            for node2 in neighborhood_node:
                if(self.Adjmatrix[node1, node2] == 1):
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
                        Temp2 += self.Dismatrix[pathlist[k][m], pathlist[k][m+1]]
                    distance.append(Temp2)
                
                if(len(distance) == 0):
                    continue
                else:
                    if(min(distance) >= Temp):
                        Temp = min(distance)
        
        self.diameter = Temp
        
    def degreeNdegree(self):
        """Calculate the degree sequence and nodal neighborhood degree
        Visualize them as distributions
        """
        self.degree = np.sum(self.Adjmatrix, axis = 1)
        self.Ndegree = np.zeros(len(self.degree), dtype = int)
        for i in range(len(self.degree)):
            Temp = 0
            for j in range(len(self.degree)):
                Temp += self.degree[j]*self.Adjmatrix[i, j]
            self.Ndegree[i] = Temp
            
    def cost_cal(self, Type, Tract_pop, Tractx, Tracty):
        """Calculate the normalized demand-population cost
        """
        Geox1 = sf.FeatureScaling(self.Geox)
        Geoy1 = sf.FeatureScaling(self.Geoy)
        Tract_pop1 = sf.FeatureScaling(Tract_pop)
        Tractx1 = sf.FeatureScaling(Tractx)
        Tracty1 = sf.FeatureScaling(Tracty)
        
        self.cost, temp = ans.cost(self.demandloc, Geox1, Geoy1, Tract_pop1, Type, Tractx1, Tracty1, Tract_pop)
        
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
        
    def network_setup(self, Tract_density, Tractx, Tracty, i, lon, lat):
        """Initialize everything for networks: location, distance matrix, degreesequence, cost, cluster_coeff, efficiency, diameter
        Input: Tract_density - 1D numpy array: population data of each tract in the area
               Tractx - 1D numpy array
               Tracty - 1D numpy array
               i - the number of the network in the system: i = 1, 2, 3 representing water, power and gas
        
        Output: \
        """
        self.Nodelocation(Tract_density, Tractx, Tracty, lon, lat)
        ##from GOOGLE API get the elevation
        self.GoogleAPIele()
        self.Distmatrix()
        
        #Decision of network adjacent matrix of three networks
        while(1):
            self.sampleseq = np.random.poisson(dt.fitdegree[i], size = self.nodenum)
            if(self.sampleseq.all() != 0):
                #if(np.max(self.sampleseq) >= 5):
                    #continue
                break
        
        self.connection(self.sampleseq, dt.num)
        self.create_edgelist()
        self.degree, self.Ndegree = sf.degreeNdegree(self.Adjmatrix)
        
        #Plot each single infrastructure network
#       self.drawnetwork(dt.Type1, dt.llon, dt.rlon, dt.llat, dt.rlat)
        #plt.savefig("{} network.png".format(self.name), dpi = 2000)
        
        ##Calculate the network topology features
        self.cal_topology_feature()
        self.cost_cal(dt.Type2, Tract_density, Tractx, Tracty)
#       self.cost_cal(dt.Type2, Tract_pop, Tractx, Tracty)
        
    def datacollection(self):
        """Collect the necessary information of the network features and package them into a dictionary for optimization in julia
        Input: self.features......
        
        Output: dictionary of the network features
        """
        
        self.datadict = {'name': self.name, 'supplyname': self.supplyname, 'tranname': self.tranname, 'demandname': self.demandname, 
                        'nodenum': self.nodenum, 'demandnum': self.demandnum, 'trannum': self.trannum, 'supplynum': self.supplynum,
                        "demandseries": self.demandseries, 'transeries': self.transeries, 'supplyseries': self.supplyseries,
                        "edgediameter": self.edgediameter, 'population_assignment': self.popuassign, 'elevation': self.elevation, 'color': self.color}
        