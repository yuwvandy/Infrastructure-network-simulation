import data as dt
import Basemapset as bm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Sharefunction as sf

class cenetwork:
    def __init__(self, name, nodenum, seednum, alpha, beta, gamma, Geox, Geoy):
        """Set up the class of infrastructure network defined in paper: A spatial network model for civil infrastructure system development
        Input:
            name - the name of the infrastructure network
            nodenum - the total number of the nodes in the infrastructure network
            seednum - the number of the initial nodes in the infrastructure network
            alpha, beta, gamma - the parameters defined in that paper, the physical meaning can be seen in that paper
        """

        self.name = name
        self.nodenum = nodenum
        self.seednum = seednum
        self.alpha, self.beta, self.gamma = alpha, beta, gamma
        self.Geox, self.Geoy = Geox, Geoy

        self.adjmatrix = np.zeros((self.nodenum, self.nodenum), dtype = int)

    def assignprob(self, density):
        """Calculate the assignment probability based on population density
        Input:
            density - the density of the population distribution

        Output: the cumu_prob along with the index transformatino metric
        """
        prob = sf.FeatureScaling3(density**self.gamma)
        temp1 = len(prob[0])

        probflatten = prob.flatten()
        cumu_prob = []
        cumu_prob_index = []

        for i in range(len(probflatten)):
            cumu_prob_index.append([i%temp1, int(i/temp1)])

            if(i == 0):
                cumu_prob.append(probflatten[i])
            else:
                cumu_prob.append(probflatten[i] + cumu_prob[-1])

        return cumu_prob, cumu_prob_index

    def setlocation(self, density):
        """Assign node locations on 2D-plane based on the population density distribution
        Input:
            xgrid, ygrid - the x, y coordinates of the grid of the 2D-plane
            density - the distribution of the population density
        """
        import numpy as np

        self.cumu_prob, self.cumu_prob_index = self.assignprob(density)
        self.nodelocindex = []
        self.nodex, self.nodey = np.empty(self.nodenum, dtype = float), np.empty(self.nodenum, dtype = float)

        for i in range(self.nodenum):
            flag = 0
            while(flag == 0):
                temp = np.random.rand()
                for j in range(len(self.cumu_prob)):
                    if(temp <= self.cumu_prob[j]):
                        if(self.cumu_prob_index[j] in self.nodelocindex):
                            continue
                        else:
                            self.nodelocindex.append(self.cumu_prob_index[j])
                            self.nodey[i] = self.Geoy[self.cumu_prob_index[j][0]]
                            self.nodex[i] = self.Geox[self.cumu_prob_index[j][1]]
                            flag = 1
                            break
                        

    def distmatrix(self):
        """Set up the distance matrix of the network
        """
        import numpy as np

        self.nodexnormal, self.nodeynormal = sf.FeatureScaling(self.nodex), sf.FeatureScaling(self.nodey)
        
        self.dmatrix = np.empty((self.nodenum, self.nodenum), dtype = float)
        self.dnormalmatrix = np.empty((self.nodenum, self.nodenum), dtype = float)
        
        for i in range(self.nodenum):
            for j in range(i, self.nodenum):
                self.dmatrix[i, j] = sf.dist(self.nodey[i], self.nodex[i], self.nodey[j], self.nodex[j])
                self.dmatrix[j, i] = self.dmatrix[i, j]
                
                self.dnormalmatrix[i, j] = sf.dist(self.nodeynormal[i], self.nodexnormal[i], self.nodeynormal[j], self.nodexnormal[j])
                self.dnormalmatrix[j, i] = self.dnormalmatrix[i, j]
                

    def distseedmatrix(self):
        """Set up the distance matrix of seed nodes in the network
        """
        self.seedindex = []
        while(len(self.seedindex) < self.seednum):
            temp = np.random.randint(0, self.nodenum)
            if(temp in self.seedindex):
                continue
            else:
                self.seedindex.append(temp)
            
        self.dseedmatrix = np.empty((self.seednum, self.seednum), dtype = float)

        for i in range(self.seednum):
            for j in range(self.seednum):
                self.dseedmatrix[i, j] = self.dmatrix[self.seedindex[i], self.seedindex[j]]
                self.dseedmatrix[j, i] = self.dseedmatrix[i, j]


    def mstseednode(self):
        """Set up the minimum spanning tree of the seeded nodes
        """
        mst = sf.mst(self.dseedmatrix)
        for i in range(len(mst)):
            self.adjmatrix[self.seedindex[mst[i][0]], self.seedindex[mst[i][1]]] = 1
            # self.adjmatrix[self.seedindex[mst[i][1]], self.seedindex[mst[i][0]]] = 1


    def cal_adjmatrix(self, k):
        """Set up the adjmatrix
        Input:
            k - the average degree of the network, k<n where the n denotes the number of seeded nodes
        """
        import copy
        import numpy

        self.tempindex = copy.copy(self.seedindex)

        for i in range(self.nodenum):
            if(i in self.seedindex):
                continue
            disttemp, degreetemp = [], []
            for j in range(len(self.tempindex)):
                disttemp.append(self.dnormalmatrix[i, self.tempindex[j]])
                degreetemp.append(np.sum(self.adjmatrix[self.tempindex[j], :]))    

            edgeprob = np.array(degreetemp)**self.beta/np.exp(np.array(disttemp)/self.alpha)
            sortedgeprob_index = np.argsort(-edgeprob)

            subtempindex = []
            
            # temp_degree = np.sum(self.adjmatrix[i, :])
            
            # if(temp_degree >= k/2):
            #     continue
            
            while(len(subtempindex) < k):
                tempprob = np.random.rand()
                for j in range(len(edgeprob)):
                    if(tempprob <= edgeprob[sortedgeprob_index[j]]):
                        subtempindex.append(sortedgeprob_index[j])
                        self.adjmatrix[sortedgeprob_index[j], i] = 1
                        # self.adjmatrix[i, sortedgeprob_index[j]] = 1
                        if(len(subtempindex) >= k):
                            break
            
    
    def topo_efficiency_cal(self):
        """ Calculate the topological efficiency of the infrastructure networks
        """
        
        Temp = 0
        for i in range(self.nodenum):
            print(i)
            for j in range(self.nodenum):
                if(i != j):
                    if(self.topo_shortestpathij(i, j) == None):
                        continue
                    Temp += 1/self.topo_shortestpathij(i, j)

        self.topo_efficiency = 1/(self.nodenum*(self.nodenum - 1))*Temp
        
    def efficiency_cal(self):
        """Calculate the spatial efficiency of the infrastructure networks
        """
        Temp = 0
        for i in range(self.nodenum):
            print(i)
            for j in range(self.nodenum):
                if(i != j):
                    if(self.shortestpathij(i, j) == None):
                        continue
                    Temp += 1/self.shortestpathij(i, j)
                
        self.efficiency = 1/(self.nodenum*(self.nodenum - 1))*Temp
        
    def shortestpathij(self, i, j):
        """Find the spatial distance of the shortest path between node i and j
        """
        pathlist = []
        self.pathij(i, j, pathlist)
        distance = []
        
        for i in range(len(pathlist)):
            Temp = 0
            for j in range(len(pathlist[i]) - 1):
                Temp += self.dmatrix[pathlist[i][j], pathlist[i][j+1]]
            distance.append(Temp)
        
        if(len(distance) == 0):
            return None
        else:
            return min(distance)
    
    def topo_shortestpathij(self, i, j):
        """ Find the shortest path between node i and j and calculate its topo distance
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
    
    def pathij(self, i, j, pathlist):
        """Perform the DFS to find all paths between nodes i and j
        Input: i - path starting from node j
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
        
    def topo_diameter(self):
        """The topological diameter of a network
        """
        import math
        
        Temp = 0
        for i in range(self.nodenum):
            for j in range(self.nodenum):
                # if(i != j):
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
                # if(i != j):
                    pathlist = []
                    self.pathij(i, j, pathlist)
                    distance = []
                    
                    for k in range(len(pathlist)):
                        Temp2 = 0
                        for m in range(len(pathlist[k]) - 1):
                            Temp2 += self.dmatrix[pathlist[k][m], pathlist[k][m+1]]
                        distance.append(Temp2)
                    
                    if(len(distance) == 0):
                        continue
                    else:
                        if(min(distance) >= Temp):
                            Temp = min(distance)
        
        self.diameter = Temp
        
    def cost_cal(self, Type, Tract_pop, Tractx, Tracty):
       """Calculate the normalized demand-population cost
       """
       Geox1 = sf.FeatureScaling(self.Geox)
       Geoy1 = sf.FeatureScaling(self.Geoy)
       Tract_pop1 = sf.FeatureScaling(Tract_pop)
       Tractx1 = sf.FeatureScaling(Tractx)
       Tracty1 = sf.FeatureScaling(Tracty)
      
       self.cost = ans.cost(np.array(self.nodelocindex), Geox1, Geoy1, Tract_pop1, Type, Tractx1, Tracty1, Tract_pop, dt.cnum)[0]
    
    def NPL(self):
        """Calculate the normalized physical length of all edges in the network
        """
        self.edge = np.zeros((np.int(np.sum(self.adjmatrix)), 3))
        Temp = 0
        for i in range(self.nodenum):
            for j in range(self.nodenum):
                if(self.adjmatrix[i, j] == 1):
                    self.edge[Temp, 0], self.edge[Temp, 1], self.edge[Temp, 2] = i, j, self.dmatrix[i, j]
                    Temp += 1
        
        self.Totallength = ((np.max(self.Geox) - np.min(self.Geox))**2 + (np.max(self.Geoy) - np.min(self.Geoy))**2)**0.5
        self.norm_edge = self.edge[:, 2]/self.Totallength
        
    
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
    
    def network_setup(self, Tract_density, Tract_pop, Tractx, Tracty, k):
       """Initialize everything for networks: location, distance matrix, degreesequence, cost, cluster_coeff, efficiency, diameter
       Input: Tract_density - 1D numpy array: population data of each tract in the area
              Tractx - 1D numpy array
              Tracty - 1D numpy array
       
       Output: \
       """
       
       self.setlocation(Tract_density)
       self.distmatrix()
       self.distseedmatrix()
       self.mstseednode()
       self.cal_adjmatrix(k)
       
       self.cal_topology_feature()

       self.cost_cal(dt.Type2, Tract_pop, Tractx, Tracty)
















