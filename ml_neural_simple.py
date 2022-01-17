#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 21:27:34 2022

neural network class

@author: deadpool
"""

import numpy as np

import mtrc_spprt as ms

class NeuralNetworkSimple:
    def __init__(self, lrnng_rt):
        # set random weights
        self.wghts = None
        self.bias = np.random.random()
        self.lrnng_rt = lrnng_rt
        ms_cls = ms.MltPrdcts()
        
        
        def cmpt_grdnts(self, inpt_arry, trgt_vl):
            layer_1 = ms_cls.dot(inpt_arry, self.wghts) + self.bias
            prdct_vl = self.prdctn(inpt_arry)
            derror_dprdctn = 2*(prdct_vl - trgt_vl)
            dprdctn_dlayer1 = self.sigmoid_drvtv(layer_1) 
            dlayer1_dbias = 1
            # 0, 1 is based on tehe taret value being 0 or 1
            dlayer1_dwghts = (0*self.wghts) + (1*inpt_arry)
            
            derror_dbias = derror_dprdctn*dprdctn_dlayer1*dlayer1_dbias
            derror_dwghts = derror_dprdctn*dprdctn_dlayer1*dlayer1_dwghts
            
            return derror_dbias, derror_dwghts
            
        
        def prdctn(self, inpt_arry):
            layer_1 = ms_cls.dot(inpt_arry, self.wghts) + self.bias
            layer_2 = self.sigmoid(layer_1)
            prdct_vl = layer_2
            return prdct_vl
        
        
        def sigmoid(self, x):
            # funtion tha makes a smooth transition from 0 to 1
            vl = 1 / (1 + np.exp(-x))
            return vl

        def sigmoid_drvtv(self, x):
            # funtion tha makes a smooth transition from 0 to 1
            vl = np.exp(-x)/(np.power(1 + np.exp(-x), 2))
            return vl
        
        def train(self, inpt_arrys, trgts, itrtns):
            cmltv_errs = []
            for cur_itrtn in itrtns:
                rndm_data_indx = np.random.randint(len(inpt_arrys))
                inpt_arry = inpt_arrys[rndm_data_indx]
                trgt = trgts[rndm_data_indx]
                
                derror_dbias, derror_dwghts = self.cmpt_grdnts(inpt_arry, trgt)
                self.update_prmtrs(derror_dbias, derror_dwghts)
                
                if cur_itrtn % 100 == 0:
                    cmltv_err = 0
                    for data_instnc_idx in range(len(inpt_arrys)):
                        data_pnt = inpt_arrys[data_instnc_idx]
                        trgt = trgts[data_instnc_idx]
                        
                        prdctn = self.prdctn(data_pnt)
                        err = np.square(prdctn - trgt)
                        cmltv_err = cmltv_err + err
                    cmltv_errs.append(cmltv_err)
            return cmltv_errs
            
        
        
        def update_prmtrs(self, derror_dbias, derror_dwghts):
            self.bias = self.bias - (derror_dbias*self.lrnng_rt)
            self.wghts = self.wghts - (derror_dwghts* self.lrnng_rt)
        