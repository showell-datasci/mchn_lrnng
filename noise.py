#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 12:14:22 2022

@author: carl
"""
import numpy as np

import io_spprt as ios

if __name__ == "__main__":

    wav_file_ex = r'/home/carl1/Projects/ESC-50-master/audio/1-22804-A-46.wav'
    data_io = ios.DataIO()
    data_io.add_flnm(wav_file_ex)
    
    samplerate, data_obj = data_io.rd_snd(sngl_fl=True, fft_tf=False)
    
    print(data_obj)
    
    noise = np.random.normal(0, 10000, data_obj.shape)
    
    new_signal = data_obj + noise
    
    new_flnm = r'/home/carl1/Projects/ESC-50-master/audio_noise/1-22804-A-46_morenoise.wav'
    
    print(new_signal)
    
    data_io.add_flnm(new_flnm)
    
    data_io.wrt_snd(new_signal.astype(np.int16))
