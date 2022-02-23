#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 20:03:26 2021

unit testing for io_spprt

@author: deadpool
"""
import os
import random
import time

import io_spprt as ios

def tst_data_io_csv(flnm):
    data_io = ios.DataIO()
    data_io.add_flnm(flnm)
    print(data_io.flnm)
    data_dct_lst = data_io.rd_csv()
    for data_vls in data_dct_lst:
        print(data_vls)
        
def tst_data_io_snd(data_loc, sngl_fl, fft_tf=False):
    data_io = ios.DataIO()
    if sngl_fl:
        data_io.add_flnm(data_loc)
        print(data_io.flnm)
        samplerate, data_obj = data_io.rd_snd(sngl_fl=sngl_fl, fft_tf=fft_tf)
        print(samplerate)
        print(data_obj)
    else:
        snd_strt_tm = time.time()
        data_io.add_fldr(data_loc)
        print(data_io.fldr)
        data_dct_lst = data_io.rd_snd(sngl_fl=sngl_fl,fft_tf=fft_tf)
        for vl in data_dct_lst[:5]:
            print(vl)
        snd_end_tm = time.time()
        print(f'It took {snd_end_tm - snd_strt_tm} to get sound files.')


def tst_fltr_prcss(data_loc, fft_tf):
    data_prcss = ios.ProcessDataIO()
    data_prcss.add_fldr(data_loc)
    snd_strt_tm = time.time()
    def fltr_fnct(flnm, fldr, fltr_prcnt):
        data_prcss_int = ios.ProcessDataIO()
        rslts= {}
        if random.random() > fltr_prcnt:
            data_prcss_int.add_flnm(os.path.join(fldr, flnm))
            sample_rate, data = data_prcss_int.rd_snd(True, fft_tf=fft_tf)
            rslts = {'flnm': flnm, 'smpl_rt': sample_rate, 'data': data}
            keep_tf = True
        else:
            keep_tf = False
        return keep_tf, rslts
    
    data_dct_lst = data_prcss.fltr_prcss_fldr(fltr_fnct, [data_prcss.fldr, 0.75])   
    for vl in data_dct_lst[:5]:
        print(vl)
        
    data_io = ios.DataIO()
    data_io.add_fldr(data_loc)
    data_dct_lst = data_io.rd_snd(sngl_fl=False, fft_tf=False)
    
    data_obj = [ele['data'] for ele in data_dct_lst]
        
    snd_smooth = data_prcss.prcss_snd(data_obj)
    new_fldr = '/home/carl/projects/ESC-50-master/audio_smooth/'
    smooth_data_dct_lst = []
    for i in snd_smooth:
        smooth_data_dct_lst.append({'flnm': new_fldr, 'smpl_r': int(44100/1000) , 'data': i})
    
    data_io.wrt_snd(smooth_data_dct_lst, sngl_fl=True, fft_tf=False)
    print(len(data_obj), len(snd_smooth))
    print(len(data_obj[0]), len(snd_smooth[0]))
    snd_end_tm = time.time()
    print(f'It took {snd_end_tm - snd_strt_tm} to get sound files.')
    print(f'There are now {len(data_dct_lst)} sampled files.')
        
        
    

if __name__ == "__main__":
    strt_tm = time.time()
    flnm = r'/home/deadpool/Projects/MCHN_LRNNG/DATA/ESC-50-master/meta/esc50.csv'
    snd_flnm = r'/home/deadpool/Projects/MCHN_LRNNG/DATA/ESC-50-master/audio/1-137-A-32.wav'
    # snd_fldr = r'/home/deadpool/Projects/MCHN_LRNNG/DATA/ESC-50-master/audio/'
    print("Testing meta data")
    tst_data_io_csv(flnm)

    print("Testing sound data file")
    tst_data_io_snd(snd_flnm, sngl_fl=True)
    
    print("Testing sound data folder")
    tst_data_io_snd(snd_fldr, sngl_fl=False, fft_tf=False)
    tst_data_io_snd(snd_fldr, sngl_fl=False, fft_tf=True)
    
    print("Testing filtering and processing of sound data folder")
    tst_fltr_prcss(snd_fldr, fft_tf=True)
    tst_fltr_prcss(snd_fldr, fft_tf=False)

    data_io.wrt_snd(new_signal.astype(np.int16))
       
    end_tm = time.time()
    print(f"This scirpt took {end_tm-strt_tm} seconds to run.")
    

