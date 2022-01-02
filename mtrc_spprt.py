#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 13:36:13 2021

Script to hold metrics.

@author: deadpool
"""

import numpy as np
# note use of numpy longdouble

class MtrcSpprt():
    def __init__(self):
        self.mtrc_nm = ''
        
    def l1(self, arry0, arry1):
        d = np.sum(np.abs(arry0-arry1, dtype=np.longdouble))
        return d
        
    
    def l2(self, arry0, arry1):
        d = np.sqrt(np.sum(np.power(arry0-arry1, 2, dtype=np.longdouble)))
        return d
    
    def l_inf(self, arry0, arry1):
        d = np.max(np.abs(arry0-arry1))
        return d
    
    def l_r(self, arry0, arry1):
        d = np.power(np.sum(np.power(np.abs(arry0-arry1, dtype=np.longdouble), self.r)), (1/self.r))
        return d
    
    def set_r(self, r):
        self.r = r
        