#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 13:36:13 2021

Script to hold metrics.

@author: deadpool
"""

import numpy as np

class MtrcSpprt():
    def __init__(self):
        self.mtrc_nm = ''
        
    def l1(arry0, arry1):
        d = np.sum(np.abs(arry0-arry1))
        return d
        
    
    def l2(arry0, arry1):
        d = np.sqrt(np.sum(np.power(arry0-arry1, 2)))
        return d
    
    def l_inf(arry0, arry1):
        d = np.max(np.abs(arry0-arry1))
        return d
    
    def l_r(arry0, arry1, r):
        d = np.power(np.sum(np.power(np.abs(arry0-arry1), r)), (1/r))
        return d