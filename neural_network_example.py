#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to build a neural network. 

Based on realypython article:
    https://realpython.com/python-ai-neural-network/

Created on Sun Jan  9 06:20:06 2022

@author: deadpool
"""

import numpy as np
import time
from collections import Counter

import fnctn_spprt as fs
import io_spprt as ios
import mtrc_spprt as ms

def anlyss_snd(meta_flnm):
    data_io = ios.DataIO()
    data_io.add_flnm(meta_flnm)
    meta_lst = data_io.rd_csv(separator=',')
    print(len(meta_lst))
    ctgry_lst = [data_vl['category'] for data_vl in meta_lst]
    print(dict(Counter(ctgry_lst)))
    
    return None




def make_prediction(inpt_arry, wghts, bias):
    ms_cls = ms.MltPrdcts()
    
    layer_1 = ms_cls.dot(inpt_arry, wghts) + bias
    layer_2 = fs.sigmoid(layer_1)
    return layer_2

if __name__ == "__main__":
    strt_tm = time.time()
    print("Looking at sound data.")
    flnm = r'/home/deadpool/Projects/MCHN_LRNNG/DATA/ESC-50-master/meta/esc50.csv'
    anlyss_snd(flnm)
    print("We want to pick one category to make a prediction. It is this category or not.")
    cat_select = 'chainsaw'
    print("We will use {cat_select}")
    print("Getting the sound data.")
    snd_fldr = r'/home/deadpool/Projects/MCHN_LRNNG/DATA/ESC-50-master/audio/'
    
    
    

    
    end_tm = time.time()
    print(f"This scirpt took {end_tm-strt_tm} seconds to run.")
