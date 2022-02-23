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
import os
import random
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
    
    return dict(Counter(ctgry_lst))


def gt_anlyss_data(lbl_vls, meta_flnm, mdl_fldr, non_lbl_prcnt):
    data_io = ios.DataIO()
    data_io.add_flnm(meta_flnm)
    meta_lst = data_io.rd_csv(separator=',')
    print(len(meta_lst))
    lbl_flnm_dct = {}
    for data_vl in meta_lst:
        if data_vl['category'] in lbl_vls:
            lbl_flnm_dct.setdefault(data_vl['category'], [])
            lbl_flnm_dct[data_vl['category']].append(data_vl['filename'])
    
    tlt_lbls = sum([len(lbl_flnm_dct[lbl]) for lbl in lbl_flnm_dct])
    use_prctn = non_lbl_prcnt*tlt_lbls/(len(meta_lst) - tlt_lbls)
    
    other_lbl_dct = {}
    for data_vl in meta_lst:
        if data_vl['category'] not in lbl_vls:
            if random.random() <= use_prctn:
                other_lbl_dct.setdefault(data_vl['category'], [])
                other_lbl_dct[data_vl['category']].append(data_vl['filename'])
        
    with open(os.path.join(mdl_fldr, f"analysis_{'_'.join(lbl_vls)}.csv"), 'w') as g:
        g.write('label,file\n')
        for lbl in lbl_flnm_dct:
            for flnm in lbl_flnm_dct[lbl]:
                g.write(f"{lbl},{flnm}\n")
        for lbl in other_lbl_dct:
            for flnm in other_lbl_dct[lbl]:
                g.write(f"{lbl},{flnm}\n")  
  
    return lbl_flnm_dct, other_lbl_dct


def make_prediction(inpt_arry, wghts, bias):
    ms_cls = ms.MltPrdcts()
    
    layer_1 = ms_cls.dot(inpt_arry, wghts) + bias
    layer_2 = fs.sigmoid(layer_1)
    return layer_2

def rd_anlyss_data(fl_lst, fft_tf=False):
    data_dct_lst = []
    # for each of the files we will need to get the sound data
    io_cls = ios.DataIO()
    
    for flnm in fl_lst:
        io_cls.add_flnm(flnm)
        sample_rate, snd_data = io_cls.rd_snd(sngl_fl=True, fft_tf=True)
        data_dct_lst.append(snd_data)
    
    return data_dct_lst


if __name__ == "__main__":
    strt_tm = time.time()
    print("Looking at sound data.")
    flnm = r'/home/deadpool2/Projects/MCHN_LRNNG/DATA/ESC-50-master/meta/esc50.csv'
    mdl_fldr = r'/home/deadpool2/Projects/MCHN_LRNNG/DATA/ESC-50-master/models'
    anlyss_snd(flnm)
    print("We want to pick one category to make a prediction. It is this category or not.")
    cat_select = 'chainsaw'
    print(f"We will use {cat_select}")
    print("Getting the sound data.")
    snd_fldr = r'/home/deadpool2/Projects/MCHN_LRNNG/DATA/ESC-50-master/audio/'
    lbl_flnm_dct, other_lbl_dct = gt_anlyss_data(['chainsaw'], meta_flnm=flnm, mdl_fldr=mdl_fldr, non_lbl_prcnt=1)
    # read in the data
    print(lbl_flnm_dct)
    print(other_lbl_dct)
    fl_lst = [os.path.join(snd_fldr, flnm) for flnm in  lbl_flnm_dct['chainsaw']]
    print(len(fl_lst))
    data_dct_lst = rd_anlyss_data(fl_lst, fft_tf=True)
    print(data_dct_lst[0])
    
    

    
    

    
    end_tm = time.time()
    print(f"This scirpt took {end_tm-strt_tm} seconds to run.")
