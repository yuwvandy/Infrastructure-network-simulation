# -*- coding: utf-8 -*-
"""
Created on Sat May 23 11:10:44 2020

@author: 10624
"""

"""
This file is to:
Apply annealing simulation to locate the optimal solution of infrastructure facility
"""

import math
import copy

def cost(sol, lat, lon, PDsub, Type, LAT, LON):
    """Calculate the overall cost all a new solution: two type: demand-population, supply-transmission(transmission-demand)
    sol: new solution: location in the form of the index
    lat, lon: the latitude and longitude of the small pixel in the basemap (the lat and lon of the sublevel facilities)
    LAT, LON: the latitude and longitude of the small pixel in the basemap
    """
    Sum_Cost = 0
    if(Type == 'Population'):
        for i in range(len(lat)-1):
            for j in range(len(lon)-1):
                temp_X = 0.5*(lat[i]+lat[i+1])
                temp_Y = 0.5*(lon[j]+lon[j+1])
                Min_Dist = math.inf
                for k in range(len(sol)):
                    Dist = math.sqrt((temp_X - LAT[sol[k][0]])**2 + (temp_Y - LON[sol[k][1]])**2)
                    if(Dist < Min_Dist):
                        Min_Dist = Dist
                        index = k
                Sum_Cost += Min_Dist*PDsub[i][j]
        return Sum_Cost
    else:
        for i in range(len(lat)):
            Min_Dist = math.inf
            for k in range(len(sol)):
                Dist = math.sqrt((lat[i] - LAT[sol[k][0]])**2 + (lon[i] - LON[sol[k][1]])**2)
                if(Dist < Min_Dist):
                    Min_Dist = Dist
                    index = k
            Sum_Cost += Min_Dist
        return Sum_Cost
    
def neighbor1(sol, LAT, LON, T, direc, step, c, Time):
    """Explore the neighborhood of the current solution
    sol: current solution
    direc: Track down the direction during iteration
    step: Track down the step during iteration
    c: Track down the cost during iteration
    """
    Index = np.random.randint(0, len(sol))
    Sol = copy.deepcopy(sol)
    while(1):
        if(Time == 1):
            Step = np.random.randint(0, 6)
            Temp = np.random.randint(0, 4)
        else:
            if(c[-1] < c[-2]):
                Temp = direc[-1]
                if(T >= 0.66):
                    Step = np.random.randint(0, 6)
                if(T >= 0.2 and T <= 0.66):
                    Step = np.random.randint(0, 3)
                if(T <= 0.2):
                    Step = np.random.randint(0, 2)
            else:
                Temp = np.random.randint(0, 4)
                Step = np.random.randint(0, 5)

        if(Temp == 0):
            Sol[Index][0] += Step
        elif(Temp == 1):
            Sol[Index][0] -= Step
        elif(Temp == 2):
            Sol[Index][1] += Step
        elif(Temp == 3):
            Sol[Index][1] -= Step
        if((Sol[Index][0] >= 0 and Sol[Index][0] <= (len(LAT)-1)) and (Sol[Index][1] >= 0 and Sol[Index][1] <= (len(LON)-1))):
            step.append(Step)
            direc.append(Temp)
            return Sol
        else:
            Sol = copy.deepcopy(sol)
            
def neighbor2(sol, LAT, LON):
    """Explore the neighborhood of the current solution
    """
    Index = np.random.randint(0, len(sol))
    Sol = copy.deepcopy(sol)
    while(1):
        Step = np.random.randint(1,5)
        Temp = np.random.randint(0,4)
        if(Temp == 0):
            Sol[Index][0] += Step
        elif(Temp == 1):
            Sol[Index][0] -= Step
        elif(Temp == 2):
            Sol[Index][1] += Step
        elif(Temp == 3):
            Sol[Index][1] -= Step
        if((Sol[Index][0] >= 0 and Sol[Index][0] <= (len(LAT)-1)) and (Sol[Index][1] >= 0 and Sol[Index][1] <= (len(LON)-1))):
            return Sol
        else:
            Sol = copy.deepcopy(sol)
            
def acceptance_probability(old_cost, new_cost, T):
    return math.exp((old_cost - new_cost)/T)

def anneal1(sol, Type, lat, lon, PDsub, LAT, LON):
    c = []
    direc = []
    step = []
    old_cost = cost(sol, lat, lon, PDsub, Type, LAT, LON)
    c.append(old_cost)
    Time = 1
    T = 1.0
    T_min = 0.1
    alpha = 0.9
    Cost_Iter = []
    while T > T_min:
        i = 0
        while i <= 100:
            new_sol = neighbor1(sol, LAT, LON, T, direc, step, c, Time)
            new_cost = cost(new_sol, lat, lon, PDsub, Type, LAT, LON)
            ap = acceptance_probability(old_cost, new_cost, T)
            if(ap >= np.random.rand()):
                sol = new_sol
                old_cost = new_cost
                Cost_Iter.append(old_cost)
            print('Iteration {}, Temperature {}, Cost {}'.format(Time, T, old_cost))
            i += 1
            Time += 1
            c.append(new_cost)
            
        T = T*alpha
    return sol, old_cost, c

def anneal2(sol, Type, lat, lon, PDsub, LAT, LON):
    c = []
    old_cost = cost(sol, lat, lon, PDsub, Type, LAT, LON)
    c.append(old_cost)
    Time = 1
    T = 1.0
    T_min = 0.1
    alpha = 0.9
    Cost_Iter = []
    while T > T_min:
        i = 0
        while i <= 100:
            new_sol = neighbor2(sol, LAT, LON)
            new_cost = cost(new_sol, lat, lon, PDsub, Type, LAT, LON)
            ap = acceptance_probability(old_cost, new_cost, T)
            if(ap >= np.random.rand()):
                sol = new_sol
                old_cost = new_cost
                Cost_Iter.append(old_cost)
            print('Iteration {}, Temperature {}, Cost {}'.format(Time, T, old_cost))
            i += 1
            Time += 1
            c.append(new_cost)

            
        T = T*alpha
    return sol, old_cost, c
    