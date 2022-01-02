#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 06:58:07 2022

@author: deadpool
"""

import json
import numpy as np
import pickle as pkl

from collections import Counter

# import mtrc_spprt as mspprt

class ml_kNN():
    """
    kNN algorithm -- class for methods related to 
        (1) getting the kNN model
        (2) executing the kNN model
    """
    def __init__(self, k):
        self.k = k
    
    def cng_k(self, k):
        self.k = k
    
    def exct_mdl(self, tst_pnt):
        # assumes test point is a dictionary with keys containing the flnm and
        # data.
        nn = {}
        lbl = ''
        dst_lst = []
        
        # helps watch parallelization complete
        if type(tst_pnt) == tuple:
            print(tst_pnt[0])
            tst_pnt = tst_pnt[1]
        
        for mdl_vls in self.mdl_dct_lst:
            dst = self.d(tst_pnt['data'], mdl_vls['data'])
            if dst in dst_lst:
                nn[dst].append(mdl_vls['label'])
            else:
                if len(dst_lst) < self.k:
                    dst_lst.append(dst)
                    dst_lst.sort()
                    nn.setdefault(dst, [])
                    nn[dst].append(mdl_vls['label'])
                else:
                    if dst < dst_lst[-1]:
                        nn.pop(dst_lst[-1])
                        dst_lst = [dst] + dst_lst[:-1]
                        dst_lst.sort()
                        nn.setdefault(dst, [])
                        nn[dst].append(mdl_vls['label'])                       
                    
        if self.slct_rl == 'mode':
            lbl_lst = []
            for dst in nn:
                lbl_lst += nn[dst]
            lbl_dct = dict(Counter(lbl_lst))
            vl_lbl_dct = {}
            for lbl in lbl_dct:
                vl_lbl_dct.setdefault(lbl_dct[lbl], [])
                vl_lbl_dct[lbl_dct[lbl]].append(lbl)
            max_vl = max([vl for vl in vl_lbl_dct])
        
        return tst_pnt['flnm'], lbl_dct, vl_lbl_dct[max_vl]
        
    def gt_mdl(self, trn_flnm, trn_fl_typ, select_rule, d_fnctn):
        self.slct_rl = select_rule
        self.d = d_fnctn
        if trn_fl_typ == 'json':
            with open(trn_flnm, 'r') as f:
                self.mdl_dct_lst = json.load(f)
                for vl in self.mdl_dct_lst:
                    vl['data'] = np.array(vl['data'], dtype = 'int16')
        elif trn_fl_typ == 'pickle':
            with open(trn_flnm, 'rb') as f:
                self.mdl_dct_lst = pkl.load(f)
        