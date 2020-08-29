class centerville:
    def __init__(self, adjpath, nodenum):
        import pandas as pd

        self.nodenum = nodenum
        self.adjlist = pd.read_csv('./data/centerville_water_edge', sep = ',', header = None).values

    def adjmatrix(self):
        self.adjmatrix = np.empty((self.nodenum, self.nodenum), dtype = int)
        for i in range(len(self.adjlist)):
            self.adjmatrix[self.adjlist[i, 0], self.adjlist[i, 1]] = 1

    def topo_efficiency_cal(self):
        """Calculate the topological efficiency of the infrastructure networks
        """
        Temp = 0
        for i in range(self.nodenum):
            for j in range(self.nodenum):
                if(self.topo_shortestpathij(i, j) == None):
                    continue
                Temp += 1/self.topo_shortestpathij(i, j)
                
        self.topo_efficiency = 1/(self.nodenum**2)*Temp
        
    def efficiency_cal(self):
        """Calculate the spatial efficiency of the infrastructure networks
        """
        Temp = 0
        for i in range(self.nodenum):
            for j in range(self.nodenum):
                if(self.shortestpathij(i, j) == None):
                    continue
                Temp += 1/self.shortestpathij(i, j)
                
        self.efficiency = 1/(self.nodenum*self.nodenum)*Temp

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
                Temp += self.dmatrix[pathlist[i][j], pathlist[i][j+1]]
            distance.append(Temp)
        
        if(len(distance) == 0):
            return None
        else:
            return min(distance)

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
        
        self.cost = ans.cost(self.loc[self.supplynum:, :], Geox1, Geoy1, Tract_pop1, Type, Tractx1, Tracty1)





