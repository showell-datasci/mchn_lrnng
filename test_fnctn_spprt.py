#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit testing for functions

Created on Sun Jan  9 06:40:27 2022

@author: deadpool
"""

import numpy as np
import time

import fnctn_spprt as fs

def tst_sigmoid():
    print("TESTING SIGMOID.")
    x_lst = [-10, -5, -2, -1, 0, 1, 2, 5, 10]
    vl_lst = [fs.sigmoid(x) for x in x_lst]
    print(f"The values {x_lst} are sigmoided to {vl_lst}")
    x_arry = np.array(x_lst)
    print("NP ARRAY MODE!")
    print(f"The array is {x_arry} and the values are {fs.sigmoid(x_arry)}")
    print("BOOM!")
    return None
    

if __name__ == "__main__":
    strt_tm = time.time()
    tst_sigmoid()
    
    
    end_tm = time.time()
    print(f"This scirpt took {end_tm-strt_tm} seconds to run.")

