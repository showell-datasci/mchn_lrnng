#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 20:03:26 2021

unit testing for io_spprt

@author: deadpool
"""

import time

import io_spprt as ios

def tst_data_io(flnm):
    data_io = ios.DataIO()
    data_io.add_flnm(flnm)
    print(data_io.flnm)
    data_dct_lst = data_io.rd_csv()
    for data_vls in data_dct_lst:
        print(data_vls)

if __name__ == "__main__":
    strt_tm = time.time()
    flnm = r'/home/deadpool/Projects/MCHN_LRNNG/DATA/ESC-50-master/meta/esc50.csv'
    tst_data_io(flnm)
    
    end_tm = time.time()
    print(f"This scirpt took {end_tm-strt_tm} seconds to run.")
    

