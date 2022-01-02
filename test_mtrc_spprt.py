#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 06:38:45 2022

Script for unit testing of the metric support folder.

@author: deadpool
"""
import numpy as np
import time

import mtrc_spprt as mspprt

def test_hlbrt_mtrcs(r):
    tst_arry0 = np.array([1, 1, 0, 0])
    tst_arry1 = np.array([0, 0, 1, 1])
    tst_arry2 = np.array([4, 0, 0, 4])
    
    
    ms = mspprt.MtrcSpprt()
    
    h_r = ms.l_r
    h_1 = ms.l1
    h_2 = ms.l2
    h_inf = ms.l_inf
    
    print(f'The vectors are {tst_arry0}, {tst_arry1}, and {tst_arry2}')
    print(f'The l_inf distance of {tst_arry0}, {tst_arry1} is {h_inf(tst_arry0, tst_arry1)}')
    print(f'The l_inf distance of {tst_arry0}, {tst_arry2} is {h_inf(tst_arry0, tst_arry2)}')
    ms.set_r(1)
    print(f'The l1 distance of {tst_arry0}, {tst_arry1} is {h_1(tst_arry0, tst_arry1)}')
    print(f'The l1 distance of {tst_arry0}, {tst_arry1} is {h_r(tst_arry0, tst_arry1)}')    
    ms.set_r(2)
    print(f'The l2 distance of {tst_arry0}, {tst_arry1} is {h_2(tst_arry0, tst_arry1)}')
    print(f'The l2 distance of {tst_arry0}, {tst_arry1} is {h_r(tst_arry0, tst_arry1)}')
    ms.set_r(r)
    print(f'The l_{r} distance of {tst_arry0}, {tst_arry1} is {h_r(tst_arry0, tst_arry1)}')

      
    return None

if __name__ == "__main__":
    strt_tm = time.time()
    
    test_hlbrt_mtrcs(3)

    
    end_tm = time.time()
    print(f"This scirpt took {end_tm-strt_tm} seconds to run.")