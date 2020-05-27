# -*- coding: utf-8 -*-
"""
Created on Sun May 24 11:09:43 2020

@author: 10624
"""

"""
This file is to collect data of the existed infrastructure network, calculate the degree distribution
and nodal neighborhood degree distribution and fit them with poisson distribution
"""

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.special import factorial
from scipy.optimize import curve_fit

def poisson(k, lamb):
    return (lamb**k/factorial(k)) * np.exp(-lamb)

def NDegree(nodenum, path):
    """Read the excel file from path
    And collect the adjmatrix data
    Input: the number of the nodes
    Output: the degree sequence and the neighborhood degree sequence
    """
    
    A = pd.read_excel(path)    
    Adjmatrix = np.zeros((nodenum, nodenum), dtype = int)
    
    for i in range(len(A['node1'])):
        Adjmatrix[A['node1'][i] - 1, A['node2'][i] - 1] = 1
        Adjmatrix[A['node2'][i] - 1, A['node1'][i] - 1] = 1
    
    Degree = np.sum(Adjmatrix, axis = 0)
    Ndegree = np.zeros(nodenum, dtype = int)
    
    for i in range(len(Ndegree)):
        Temp = 0
        for j in range(len(Ndegree)):
            Temp += Degree[j]*Adjmatrix[i, j]
        Ndegree[i] = Temp
    
    return Degree, Ndegree

def number2sequence(Ndegree):
    """Sort the Ndegree and calculate its frequency of each unique element
    Input: Ndegree - the neighborhood degree sequence
    Output: list1 - the sorted and unique degree sequence
            list2 - the frequency of each unique element in the order of what they are in list1
    """
    list1 = []
    list2 = []
    Ndegree = np.sort(Ndegree)
    for i in range(len(Ndegree)):
        if(Ndegree[i] in list1):
            continue
        list1.append(int(Ndegree[i]))
    
    for i in range(len(list1)):
        Temp = 0
        for j in range(len(Ndegree)):
            if(Ndegree[j] == list1[i]):
                Temp += 1
        list2.append(Temp)
    
    return list1, list2

def cumu(list1, list2):
    """Given the unique nodal neighborhood degree sequence and its corresponding frequency list
    calculate the cumulative frequency list
    Input: list1, list2 - the same as function 'number2sequence'
    Output: the cumulative frequency list
    """
    list3 = []
    for i in range(len(list2)):
        Temp = 0
        for j in range(i):
            Temp += list2[j]
        list3.append(Temp)
    
    return list3

def degreefit(Ndegree, a):
    """Given the unique list and frequency list, output the fitted result
    """
    list1, list2 = number2sequence(Ndegree)
    
    list2 = np.array(list2)/np.sum(list2)
    list3 = np.array(cumu(list1, list2))
    list4 = []
    
    for i in range(len(list1)):
        list4.append(poisson(list1[i], a)) #Fit by matlab
    
    list5 = np.array(db.cumu(list1, list4))
    
    plt.figure(figsize = (10,6))
    plt.scatter(list1, list2, label = 'Empirical', s = 75)
    plt.scatter(list1, list4, label = 'Poisson', marker = '>', s = 75)
    plt.grid(True)
    plt.xlabel('The neighborhood nodal degree', fontsize = 15)
    plt.ylabel('The probability', fontsize = 15)
    plt.legend(framealpha=1, frameon=False, loc = 'upper left', fontsize = 15)
    
    plt.figure(figsize = (10,6))
    plt.scatter(list1, list3, label = 'Empirical', s = 75)
    plt.scatter(list1, list5, label = 'Poisson', marker = '>', s = 75)
    plt.grid(True)
    plt.xlabel('The neighborhood nodal degree', fontsize = 15)
    plt.ylabel('The cumulative probability', fontsize = 15)
    plt.legend(framealpha=1, frameon=False, loc = 'upper left', fontsize = 15)
    
    return list1, list2, list3, list4, list5














