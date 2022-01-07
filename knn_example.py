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

import concurrent.futures
import json
import numpy as np
import os
import pickle as pkl
import random
import sys
import time

import io_spprt as ios
import mtrc_spprt as mspprt
import ml_kNN as kNN


# kNN example data is stored in a folder
# we will filter the folder as data is entered to get the training model
def fltr_fnct(flnm, fldr, fltr_prcnt, fft_tf=False):
    data_prcss = ios.ProcessDataIO()
    rslts= {}
    if random.random() > fltr_prcnt:
        data_prcss.add_flnm(os.path.join(fldr,flnm))
        sample_rate, data = data_prcss.rd_snd(True, fft_tf=fft_tf)
        rslts = {'flnm': flnm, 'smpl_rt': sample_rate, 'data': data}
        keep_tf = True
    else:
        keep_tf = False
    return keep_tf, rslts

def exct_mdl_tst_pnt(mdl_fl, fl_typ, k, tst_fl, fft_tf=False):
    print("Getting models")
    knn = kNN.ml_kNN(k)
    ms = mspprt.MtrcSpprt()
    
    print("Getting model")
    knn.gt_mdl(mdl_fl, fl_typ, select_rule='mode', d_fnctn=ms.l2)

    print(len(knn.mdl_dct_lst))
    print(knn.mdl_dct_lst[0])
    print(knn.slct_rl)
    print(knn.d)
    
    print("Getting test file")
    data_io = ios.DataIO()
    data_io.add_flnm(tst_fl)
    print(data_io.flnm)
    samplerate, data_obj = data_io.rd_snd(sngl_fl=True, fft_tf=fft_tf)
    tst_pnt = {'flnm': tst_fl, 'smpl_rt': samplerate, 'data': data_obj}
    tst_id, tst_lbl_dct, tst_lbls = knn.exct_mdl(tst_pnt)
    print(f'The file is: {tst_id}')
    print(f'The label values are: {tst_lbl_dct}')
    print(f'The labels are: {tst_lbls}')


def train_model(fldr, meta_fl, fltr_prcnt, otpt_flnm, psh_typ, fft_tf=False):
    data_meta = ios.DataIO()
    data_meta.add_flnm(meta_fl)
    meta_data = data_meta.rd_csv(separator=',')
    meta_map = {vl['filename']: vl['category'] for vl in meta_data}
    data_prcss = ios.ProcessDataIO()
    data_prcss.add_fldr(fldr)
    data_dct_lst = data_prcss.fltr_prcss_fldr(fltr_fnct, [fldr, fltr_prcnt, fft_tf])
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

def vldt_mdl(mdl_fl, data_fldr, fl_typ, fft_tf=False):
    print("Getting models")
    knn = kNN.ml_kNN(3)
    ms = mspprt.MtrcSpprt()
    
    knn.gt_mdl(mdl_fl, fl_typ, select_rule='mode', d_fnctn=ms.l2)

    print(len(knn.mdl_dct_lst))
    print(knn.mdl_dct_lst[0])
    print(knn.slct_rl)
    print(knn.d)
    
    print("Getting validation data.")
    # find test list
    tst_lst = [vl['flnm'] for vl in knn.mdl_dct_lst]
    print(len(tst_lst))
    # for sample data set, read in everything and then filter out the tst_lst
    data_io = ios.DataIO()
    data_io.add_fldr(data_fldr)
    vldt_dct_lst = [vl for vl in data_io.rd_snd(sngl_fl=False, fft_tf=fft_tf) if vl['flnm'] not in tst_lst]
    print(len(vldt_dct_lst))
    print(vldt_dct_lst[0])
    
    # TODO add variable
    vldt_dct_lst = vldt_dct_lst[:20]
    print("Making predictions")
    parallel_tf = True
    if parallel_tf:
        workers = os.cpu_count()
        tst_pnt_lst = [(idx, tst_pnt) for idx, tst_pnt in enumerate(vldt_dct_lst)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            rslts = executor.map(knn.exct_mdl, tst_pnt_lst, chunksize=len(tst_pnt_lst)/10*workers)
    else:
        rslts = []
        for tst_pnt in vldt_dct_lst:
            tst_id, tst_lbl_dct, tst_lbls = knn.exct_mdl(tst_pnt)
            rslts.append([tst_id, tst_lbl_dct, tst_lbls])
    
    print("Checking accuracy")
    data_meta = ios.DataIO()
    data_meta.add_flnm(meta_fl)
    meta_data = data_meta.rd_csv(separator=',')
    meta_map = {vl['filename']: vl['category'] for vl in meta_data}
    
    rght_lst,wrng_lst = [], []
    unrslvd_lst = []
    
    for vl in rslts:
        if len(vl[2]) == 1:
            if vl[2][0] == meta_map[vl[0]]:
                rght_lst.append(vl[0])
            else:
                wrng_lst.append(vl[0])
        else:
            unrslvd_lst.append(vl[0])
    
    print(f"There are {len(rght_lst)} correct results, {100*len(rght_lst)/len(vldt_dct_lst)}%")
    print(f"There are {len(wrng_lst)} misclassfied results, {100*len(wrng_lst)/len(vldt_dct_lst)}%")            
    print(f"There are {len(unrslvd_lst)} unreseolved results, {100*len(unrslvd_lst)/len(vldt_dct_lst)}%")   

if __name__ == "__main__":
    strt_tm = time.time()
    meta_fl = r'/home/carl1/Projects/ESC-50-master/meta/esc50.csv'
    snd_flnm = r'/home/carl1/Projects/ESC-50-master/audio/1-137-A-32.wav'
    snd_fldr = r'/home/carl1/Projects/ESC-50-master/audio/'
    otpt_fldr = r'/home/carl1/Projects/ESC-50-master/models/'
    
    fft_use = sys.argv[2]
    if fft_use == 'fft':
        fft_tf = True
    else:
        fft_tf = False
    
    if fft_tf:
        mdl_flnm_json = 'knn_fft.json'
        mdl_flnm_pkl = 'knn_fft.pkl'
    else:
        mdl_flnm_json = 'knn.json'
        mdl_flnm_pkl = 'knn.pkl'


    if sys.argv[1] == 'train':
        print("TRAINING")
        # train_model(snd_fldr, meta_fl, fltr_prcnt=0.5, otpt_flnm=os.path.join(otpt_fldr, mdl_flnm_json), psh_typ='json')
        train_model(snd_fldr, meta_fl, fltr_prcnt=0.5, otpt_flnm=os.path.join(otpt_fldr, mdl_flnm_pkl), psh_typ='pickle', fft_tf=fft_tf)
    if sys.argv[1] == 'validate':
        print("VALIDATING")
        # read files
        # vldt_mdl(os.path.join(otpt_fldr, mdl_flnm_json), fl_typ = 'json')
        vldt_mdl(os.path.join(otpt_fldr, mdl_flnm_pkl), snd_fldr, fl_typ = 'pickle', fft_tf=fft_tf)
    if sys.argv[1] == 'execute':
        print("EXECUTING")
        tst_fl = input("Enter test file contained in the data folder.")
        exct_mdl_tst_pnt(os.path.join(otpt_fldr, mdl_flnm_pkl), fl_typ = 'pickle', k=5, tst_fl=os.path.join(snd_fldr, tst_fl), fft_tf=fft_tf)
    
    end_tm = time.time()
    print(f"This scirpt took {end_tm-strt_tm} seconds to run.")
    
    

