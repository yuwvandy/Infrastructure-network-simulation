# -*- coding: utf-8 -*-
"""
Created on Sat May 23 12:05:38 2020

@author: 10624
"""
"""
This file contains function shared by all other program files. All functions here are the general functions
"""
import numpy as np

def FeatureScaling(A):
    return ((A-np.min(A))/(np.max(A)-np.min(A)))
