#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 12:14:22 2022

@author: carl
"""

import numpy as np
import os
import sys

import io_spprt as ios

def add_gauss_noise(mean, std, data):
    '''
    Parameters
    ----------
    mean : int or float
        mean of distribution
    std : int or float
        standard deviation of distribution
    data : array
        np array of data
        
    Returns
    -------
    new_signal : array
        data array with noise added

    '''
    noise = np.random.normal(mean, std, data.shape)
    
    new_signal = data + noise
    
    return new_signal
    

if __name__ == "__main__":
    
    if sys.argv[1] == 'sngl_noise':

        wav_file_ex = r'/home/carl1/Projects/ESC-50-master/audio/1-22804-A-46.wav'
        data_io = ios.DataIO()
        data_io.add_flnm(wav_file_ex)
    
        samplerate, data_obj = data_io.rd_snd(sngl_fl=True, fft_tf=False)
        
        print(data_obj)
        
        new_signal = add_gauss_noise(0, 10000, data_obj)
        
        new_flnm = r'/home/carl1/Projects/ESC-50-master/audio_noise/1-22804-A-46_noise.wav'
        
        print(new_signal)
        
        data_array = {'flnm': new_flnm, 'smpl_r': samplerate, 'data': new_signal}
        
        data_io.wrt_snd(data_array)
        
    if sys.argv[1] == 'all_noise':
        
        fldr = r'/home/carl1/Projects/ESC-50-master/audio/'
        data_io = ios.DataIO()
        data_io.add_fldr(fldr)
        data_dct_lst = data_io.rd_snd(sngl_fl=False, fft_tf=False)
        
        new_data_dct_lst = []
        
        for ele in data_dct_lst:
            nw_fldr = r'/home/carl1/Projects/ESC-50-master/audio_noise/'
            new_signal = add_gauss_noise(0, 10000, ele['data'])
            
            new_flnm = os.path.join(nw_fldr, ele['flnm'][:-4]+'_noise.wav')
            
            data_dct = {'flnm': new_flnm, 'smpl_r': ele['smpl_rt'], 'data': new_signal}
            
            new_data_dct_lst.append(data_dct)
            
        data_io.wrt_snd(new_data_dct_lst, sngl_fl=False)
