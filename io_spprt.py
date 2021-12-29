#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 19:54:52 2021
script to contain io class

@author: deadpool
"""

class DataIO():
    """
    Class for reading data stored in various formats.
    Includes reading into machine friendly formats.
    """
    def __init__(self):
        self.flnm = ""
        self.fldr = ""
        
    def add_flnm(self, flnm):
        self.flnm = flnm
        
    def rd_csv(self, separator=','):
        # read csv files into a list of dictionaries
        # assumes a header
        data_dct_lst = []
        with open(self.flnm, 'r') as f:
            hdr_dct = {idx: hdr_vl for idx, hdr_vl in enumerate(f.readline().strip().split(separator))}
            for ln in f:
                data_dct_lst.append({ hdr_dct[idx]: data_vl for idx, data_vl in enumerate(ln.strip().split(separator)) })
        return data_dct_lst
        
        

