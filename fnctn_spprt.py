#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script containing functions.

This script is desgined for conenvience. 

Created on Sun Jan  9 06:38:24 2022

@author: deadpool
"""

import numpy as np

def sigmoid(x):
    # funtion tha makes a smooth transition from 0 to 1
    vl = 1 / (1 + np.exp(-x))
    return vl
