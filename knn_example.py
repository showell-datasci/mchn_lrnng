#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 15:04:08 2021

example of implementation of kNN algorithm

(tailored to ESC data set)

NOTE: there is not single algorithm that applies to all areas. kNN is only one algoirthm. 

Algorithms need to be tailored to specific data sets or have an intermediate
algorithm to assess applicability to a dataset.

@author: deadpool
"""



"""
General process:
TRAIN:
    (1) get data
    (2) train it
    (3) save model
VALDIATE:
    (1) get data (not use in training)
    (2) calculate accuracy
TEST:
    (1) get new data
    (2) run model
    (3) calculate accuracy
UPDATE:
    (1) with new labeled data, increase model size
    (2) run model on validate data set
    (3) calculate accuracy
"""

import json
import numpy as np
import os
import pickle as pkl
import random
import sys
import time

import io_spprt as ios

# kNN example data is stored in a folder
# we will filter the folder as data is entered to get the training model
def fltr_fnct(flnm, fldr, fltr_prcnt):
    data_prcss = ios.ProcessDataIO()
    rslts= {}
    if random.random() > fltr_prcnt:
        data_prcss.add_flnm(os.path.join(fldr,flnm))
        sample_rate, data = data_prcss.rd_snd(True)
        rslts = {'flnm': flnm, 'smpl_rt': sample_rate, 'data': data}
        keep_tf = True
    else:
        keep_tf = False
    return keep_tf, rslts

def train_model(fldr, meta_fl, fltr_prcnt, otpt_flnm, psh_typ):
    data_meta = ios.DataIO()
    data_meta.add_flnm(meta_fl)
    meta_data = data_meta.rd_csv(separator=',')
    meta_map = {vl['filename']: vl['category'] for vl in meta_data}
    data_prcss = ios.ProcessDataIO()
    data_prcss.add_fldr(fldr)
    data_dct_lst = data_prcss.fltr_prcss_fldr(fltr_fnct, [fldr, fltr_prcnt])
    # making use of the mutability of dictionaries
    for vl in data_dct_lst:
        vl['label'] = meta_map[vl['flnm']]
    print(data_dct_lst)
    
    # data_dct_lst now has to be pushed out and stored
    # the code will defeault store as json, but will pickle as well
    if psh_typ == 'json':
        for idx, vl in enumerate(data_dct_lst):
            print(idx)
            vl['data'] = vl['data'].tolist()
        print("Writing file")
        with open(otpt_flnm, 'w') as g:
            json.dump(data_dct_lst, g)
    if psh_typ == 'pickle':  
        # pickling presever python types, but requires python to use
        # json is more generalizable
        with open(otpt_flnm, 'wb') as g:
            # the following pickles data with the highes protocal
            pkl.dump(data_dct_lst, g, pkl.HIGHEST_PROTOCOL)
    
    
    return None

def vldt_mdl(mdl_fl, fl_typ):
    if fl_typ == 'json':
        with open(mdl_fl, 'r') as f:
            mdl_dct_lst = json.load(f)
            for vl in mdl_dct_lst:
                vl['data'] = np.array(vl['data'], dtype = 'int16')
            print(len(mdl_dct_lst))
    elif fl_typ == 'pickle':
        with open(mdl_fl, 'rb') as f:
            mdl_dct_lst = pkl.load(f)

        print(len(mdl_dct_lst))
    # TODO load meta data
    # TODO build knn classifier
    # TODO build analysis tool
    # TODO build accuracy tools
            

if __name__ == "__main__":
    strt_tm = time.time()
    meta_fl = r'/home/deadpool/Projects/MCHN_LRNNG/DATA/ESC-50-master/meta/esc50.csv'
    snd_flnm = r'/home/deadpool/Projects/MCHN_LRNNG/DATA/ESC-50-master/audio/1-137-A-32.wav'
    snd_fldr = r'/home/deadpool/Projects/MCHN_LRNNG/DATA/ESC-50-master/audio/'
    otpt_fldr = r'/home/deadpool/Projects/MCHN_LRNNG/DATA/ESC-50-master/models/'
    mdl_flnm_json = 'knn.json'
    mdl_flnm_pkl = 'knn.pkl'


    if sys.argv[1] == 'train':
        print("TRAINING")
        # train_model(snd_fldr, meta_fl, fltr_prcnt=0.5, otpt_flnm=os.path.join(otpt_fldr, mdl_flnm_json), psh_typ='json')
        train_model(snd_fldr, meta_fl, fltr_prcnt=0.5, otpt_flnm=os.path.join(otpt_fldr, mdl_flnm_pkl), psh_typ='pickle')
    if sys.argv[1] == 'validate':
        print("VALIDATING")
        # read files
        vldt_mdl(os.path.join(otpt_fldr, mdl_flnm_json), fl_typ = 'json')
        vldt_mdl(os.path.join(otpt_fldr, mdl_flnm_pkl), fl_typ = 'pickle')

    
    end_tm = time.time()
    print(f"This scirpt took {end_tm-strt_tm} seconds to run.")
    
    

