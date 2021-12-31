#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 19:54:52 2021
script to contain io class

@author: deadpool
"""
import os
from scipy.io import wavfile

class DataIO():
    """
    Class for reading data stored in various formats.
    Includes reading into machine friendly formats.
    """
    def __init__(self):
        self.flnm = ""
        self.fldr = ""
        
    def add_fldr(self, fldr):
        """Sets the folder name; must be set to read in multiple files"""
        self.fldr = fldr

    def add_flnm(self, flnm):
        """Sets the filename; must be set to read single file"""
        self.flnm = flnm
        
    def rd_csv(self, separator=','):
        """Method to read csv files into memory as a list of dictionaries;
        all inputs are text"""
        # read csv files into a list of dictionaries
        # assumes a header
        data_dct_lst = []
        with open(self.flnm, 'r') as f:
            hdr_dct = {idx: hdr_vl for idx, hdr_vl in enumerate(f.readline().strip().split(separator))}
            for ln in f:
                data_dct_lst.append({ hdr_dct[idx]: data_vl for idx, data_vl in enumerate(ln.strip().split(separator)) })
        return data_dct_lst
    
    def rd_snd(self, sngl_fl=True):
        if sngl_fl:
            samplerate, data_arry = wavfile.read(self.flnm)
            return samplerate, data_arry
        else:
            data_dct_lst = []
            for flnm in os.listdir(self.fldr):
                if os.path.isfile(os.path.join(self.fldr, flnm)):
                    samplerate, data_arry = wavfile.read(os.path.join(self.fldr, flnm))
                    data_dct_lst.append({'flnm': flnm, 'smpl_rt': samplerate, 'data': data_arry})
            return data_dct_lst
            

class ProcessDataIO(DataIO):
    def __init__(self):
        self.flnm = ""
        self.fldr = ""
        super().__init__()
        
    def fltr_prcss_fldr(self, fltr_prcss_fnct, fnctn_inpt=[]):
        data_dct_lst = []
        for flnm in os.listdir(self.fldr):
            if os.path.isfile(os.path.join(self.fldr, flnm)):
                tmp_fnctn_inpt = [flnm]+ fnctn_inpt
                keep_tf, rstls = fltr_prcss_fnct(*tmp_fnctn_inpt)
                if keep_tf:
                    data_dct_lst.append(rstls)
        return data_dct_lst
    