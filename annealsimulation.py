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
import numpy as np
import Sharefunction as sf

def cost(sol, Geox, Geoy, PD, Type, Tractx, Tracty, PD_beforenormalize, cnum):
    """Calculate the overall cost of a new solution: two type: demand-population, supply-transmission(transmission-demand)
    Input: sol - new solution: location in the form of the index
           Geox -
           Geoy -
           PD -
           Type -
           Tractx -
           Tracty -
    Output: cost of the new solution and the population assignment for the demand nodes of the new solution
    """
    Popu_assign, Popu_assign2 = np.zeros(len(sol)), np.zeros(len(sol))
    Sum_Cost = 0
    
    for i in range(len(Tractx)):
        Dist = np.empty(len(sol), dtype = float)
        for k in range(len(sol)):
            Dist[k] = math.sqrt((Tracty[i] - Geoy[sol[k][0]])**2 + (Tractx[i] - Geox[sol[k][1]])**2)
        
        index = sf.minimumk(Dist, min(cnum, len(sol)))
        ratio = sf.FeatureScaling3(np.sum(np.exp(Dist[index]))/np.exp(Dist[index]))
        
        for k in range(len(index)):
            Popu_assign[index[k]] += PD_beforenormalize[i]*ratio[k]
            Popu_assign2[index[k]] += PD[i]*ratio[k]
            
            if(Type == 'Population'):
                Sum_Cost += Popu_assign2[index[k]]*Dist[index[k]]
            else:
                Sum_Cost += Dist[index[k]]
                
    return Sum_Cost, Popu_assign
    
def neighbor1(sol, Geox, Geoy, T, direc, step, c, Time):
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
        if((Sol[Index][0] >= 0 and Sol[Index][0] <= (len(Geoy)-1)) and (Sol[Index][1] >= 0 and Sol[Index][1] <= (len(Geox)-1))):
            step.append(Step)
            direc.append(Temp)
            return Sol
        else:
            Sol = copy.deepcopy(sol)
            
def neighbor2(sol, Geox, Geoy, T):
    """Explore the neighborhood of the current solution
    """
    initial_sol = copy.deepcopy(sol)
    Index = np.random.randint(0, len(sol))
    Sol = copy.deepcopy(sol)
    temp = 0
    while(1):
        temp += 1
        flag = 0
        
        if(T > 0.5):
            Step = np.random.randint(0, 6)
        if(T <= 0.5 and T > 0.3):
            Step = np.random.randint(0, 3)
        if(T <= 0.3):
            Step = np.random.randint(0, 2)
            
        Temp = np.random.randint(0,4)
        if(Temp == 0):
            Sol[Index][0] += Step
        elif(Temp == 1):
            Sol[Index][0] -= Step
        elif(Temp == 2):
            Sol[Index][1] += Step
        elif(Temp == 3):
            Sol[Index][1] -= Step
            
        for i in range(len(Sol)): ##ensure not repeat facility (no co-location)
            if(Sol[Index][0] == Sol[i][0] and Sol[Index][1] == Sol[i][1] and i != Index):
                flag = 1
            
        if(Sol[Index][0] >= 1 and Sol[Index][0] <= (len(Geoy)-2) and Sol[Index][1] >= 1 and Sol[Index][1] <= (len(Geox)-2) and flag == 0):
            return Sol
        else:
            if(temp >= 1000):
                return initial_sol
            Sol = copy.deepcopy(sol)
#            print(temp, "temp")
            
def acceptance_probability(old_cost, new_cost, T):
    return math.exp((old_cost - new_cost)/T)

def anneal1(sol, Type, Geox, Geoy, PD, Tractx, Tracty):
#    normalized_factor = (Geoy[-1]**2+Geox[-1]**2)**0.5*np.max(PD)
    c = []
    direc = []
    step = []
    old_cost = cost(sol, Geox, Geoy, PD, Type, Tractx, Tracty)
    c.append(old_cost)
    Time = 1
    T = 1.0
    T_min = 0.1
    alpha = 0.9
    Cost_Iter = []
    while T > T_min:
        i = 0
        while i <= 200:
            new_sol = neighbor1(sol, Geox, Geoy, T, direc, step, c, Time)
            new_cost = cost(new_sol, Geox, Geoy, PD, Type, Tractx, Tracty)
            ap = acceptance_probability(old_cost, new_cost, T)
            if(ap >= np.random.rand()):
                sol = new_sol
                old_cost = new_cost
                Cost_Iter.append(old_cost)
#            print('Iteration {}, Temperature {}, Cost {}'.format(Time, T, old_cost))
            i += 1
            Time += 1
            c.append(new_cost)
            
        T = T*alpha
    return sol, c

def anneal2(sol, Type, Geox, Geoy, PD, Tractx, Tracty, PD_beforenormalize, cnum):
#    normalized_factor = (Geoy[-1]**2+Geox[-1]**2)**0.5*np.max(PD)
    c = []
    old_cost, Popu_assign = cost(sol, Geox, Geoy, PD, Type, Tractx, Tracty, PD_beforenormalize, cnum)
    c.append(old_cost)
    Time = 1
    T = 1.0
    T_min = 0.1
    alpha = 0.9
    Cost_Iter = []
    while T > T_min:
        i = 0
        if(T > 0.7 and T <= 1):
            Iter = 10 #100
        if(T <= 0.7 and T >= 0.3):
            Iter = 10 #200
        if(T < 0.3 and T >= 0.2):
            Iter = 10 #500
        if(T < 0.2 and T >= 0.1):
            Iter = 10 #800
        while i <= Iter:
            new_sol = neighbor2(sol, Geox, Geoy, T)
            new_cost, Popu_assign = cost(new_sol, Geox, Geoy, PD, Type, Tractx, Tracty, PD_beforenormalize, cnum)
            ap = acceptance_probability(old_cost, new_cost, T)
            if(ap >= np.random.rand()):
                sol = new_sol
                old_cost = new_cost
                Cost_Iter.append(old_cost)
#            print('Iteration {}, Temperature {}, Cost {}'.format(Time, T, old_cost))
            i += 1
            Time += 1
            c.append(new_cost)

            
        T = T*alpha
    return sol, c, Popu_assign
    