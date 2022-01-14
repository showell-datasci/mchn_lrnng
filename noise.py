#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 12:14:22 2022

@author: carl
"""

import numpy as np
import os
from scipy.io.wavfile import write
import sys
import time

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

def add_tone():
    #add tone to sound bit
    pass

def insert_tone():
    #insert toen itno sound bit
    pass

def mean_snd_data(sngl_snd, data):
    
    data_io = ios.DataIO()
    
    if sngl_snd:
        data_io.add_flnm(data) #data is single filename
        samplerate, data_obj = data_io.rd_snd(sngl_fl=True, fft_tf=False)
       
        avg_snd_data = np.mean(data_obj)

    else:
        data_io.add_fldr(fldr_nm)
        data_dct_lst = data_io.rd_snd(sngl_fl=False, fft_tf=True)
        
        allmeans = []
        for i in data_dct_lst:
            y_bar = np.mean(i['data'])
            allmeans.append(y_bar)
        
        avg_snd_data = sum(allmeans)/ len(allmeans)
    
    return avg_snd_data

def get_wave(samplerate, freq, amp=8096, duration=0.5):
    '''
    Function takes the "frequecy" and "time_duration" for a wave 
    as the input and returns a "numpy array" of values at all points 
    in time
    '''
    
    t = np.linspace(0, duration, int(samplerate * duration))
    wave = amp * np.sin(2 * np.pi * freq * t)
    
    return wave

    

if __name__ == "__main__":
    t0 = time.time()
    
    
    if sys.argv[1] == "add_note_sngl":
        
        #insert seems to inssert without overriding, but is in every other index
        wav_file_ex = r'/home/carl1/Projects/ESC-50-master/audio/1-19898-C-41.wav'
        data_io = ios.DataIO()
        data_io.add_flnm(wav_file_ex)
        
        samplerate, data_obj = data_io.rd_snd(sngl_fl=True, fft_tf=False)
        print(data_obj)
        
        amp = np.max(data_obj)*0.5
        
        a_wave = get_wave(samplerate, freq=440, amp=amp, duration=5)
        
        new_signal = data_obj + a_wave
        
        new_flnm = r'/home/carl1/Projects/ESC-50-master/audio_a_note/1-19898-C-41_add_note.wav'
        print(new_signal)
        
        data_array = {'flnm': new_flnm, 'smpl_r': samplerate, 'data': new_signal}
        data_io.wrt_snd(data_array)
    
    
    if sys.argv[1] == "append_note":
        
        wav_file_ex = r'/home/carl1/Projects/ESC-50-master/audio/1-22804-A-46.wav'
        data_io = ios.DataIO()
        data_io.add_flnm(wav_file_ex)
        
        samplerate, data_obj = data_io.rd_snd(sngl_fl=True, fft_tf=False)
        print(data_obj)
        
        amp = np.max(data_obj)*0.5
        
        a_wave = get_wave(samplerate, freq=440, amp=amp, duration=1)
        
        new_signal = np.concatenate((data_obj, a_wave))
        new_flnm = r'/home/carl1/Projects/ESC-50-master/audio_a_note/1-22804-A-46_note.wav'
        print(new_signal)
        
        data_array = {'flnm': new_flnm, 'smpl_r': samplerate, 'data': new_signal}
        data_io.wrt_snd(data_array)
        
    
    
    if sys.argv[1] == 'all_noise':
        
        audible = input('Want the noise to be audible [y/n]?    ')

        if 'y' in audible.lower():
            std = 10000
        else:
            std = 100
        
        
        fldr = r'/home/carl1/Projects/ESC-50-master/audio/'
        sngl_snd = False
        mean = mean_snd_data(sngl_snd, fldr)
        
        data_io = ios.DataIO()
        data_io.add_fldr(fldr)
        data_dct_lst = data_io.rd_snd(sngl_fl=False, fft_tf=False)
        
        new_data_dct_lst = []
        
        for ele in data_dct_lst:
            nw_fldr = r'/home/carl1/Projects/ESC-50-master/audio_noise/'
            new_signal = add_gauss_noise(mean, std, ele['data'])
            
            new_flnm = os.path.join(nw_fldr, ele['flnm'][:-4]+'_noise.wav')
            
            data_dct = {'flnm': new_flnm, 'smpl_r': ele['smpl_rt'], 'data': new_signal}
            
            new_data_dct_lst.append(data_dct)
            
        data_io.wrt_snd(new_data_dct_lst, sngl_fl=False)
        t1 = time.time()
        print(f'Noise added to all .wav files. Stored in ESC-50-master/audio_noise folder.Took {round(t1-t0, 2)} seconds to run')
    
    
    if sys.argv[1] == "insert_note_sngl":
        
        #insert seems to inssert without overriding, but is in every other index
        wav_file_ex = r'/home/carl1/Projects/ESC-50-master/audio/1-22804-A-46.wav'
        data_io = ios.DataIO()
        data_io.add_flnm(wav_file_ex)
        
        samplerate, data_obj = data_io.rd_snd(sngl_fl=True, fft_tf=False)
        print(data_obj)
        
        amp = np.max(data_obj)*0.5
        
        a_wave = get_wave(samplerate, freq=440, amp=amp, duration=1)
        
        indices = np.arange(samplerate, samplerate*2)
        
        new_signal = np.insert(data_obj, indices, a_wave)
        
        new_flnm = r'/home/carl1/Projects/ESC-50-master/audio_a_note/1-22804-A-46_insert_note.wav'
        print(new_signal)
        
        data_array = {'flnm': new_flnm, 'smpl_r': samplerate, 'data': new_signal}
        data_io.wrt_snd(data_array)
    
    if sys.argv[1] == 'mean':
            
        fldr = r'/home/carl1/Projects/ESC-50-master/audio/'
        avg = mean_snd_data(fldr)
        print(avg)
        
    if sys.argv[1] == "replace_note_sngl":
        
        #insert seems to inssert without overriding, but is in every other index
        wav_file_ex = r'/home/carl1/Projects/ESC-50-master/audio/1-22804-A-46.wav'
        data_io = ios.DataIO()
        data_io.add_flnm(wav_file_ex)
        
        samplerate, data_obj = data_io.rd_snd(sngl_fl=True, fft_tf=False)
        print(data_obj)
        
        amp = np.max(data_obj)*0.5
        
        a_wave = get_wave(samplerate, freq=440, amp=amp, duration=1)
        
        indices = np.arange(samplerate, samplerate*2)
        
        for indx, i in enumerate(indices):
            data_obj[i] = a_wave[indx]
            
        new_signal = data_obj    
        new_flnm = r'/home/carl1/Projects/ESC-50-master/audio_a_note/1-22804-A-46_replace_w_note.wav'
        print(new_signal)
        
        data_array = {'flnm': new_flnm, 'smpl_r': samplerate, 'data': new_signal}
        data_io.wrt_snd(data_array)   
        
        
    if sys.argv[1] == 'sngl_noise':
        
        audible = input('Want the noise to be audible [y/n]?    ')

        if 'y' in audible.lower():
            std = 10000
        else:
            std = 100
        
        fldr_nm = r'/home/carl1/Projects/ESC-50-master/audio/'
        mean = mean_snd_data(fldr_nm)

        wav_file_ex = r'/home/carl1/Projects/ESC-50-master/audio/1-22804-A-46.wav'
        data_io = ios.DataIO()
        data_io.add_flnm(wav_file_ex)
    
        samplerate, data_obj = data_io.rd_snd(sngl_fl=True, fft_tf=False)
        
        print(data_obj)
        
        new_signal = add_gauss_noise(mean, std, data_obj)
        
        new_flnm = r'/home/carl1/Projects/ESC-50-master/audio_noise1/1-22804-A-46_noise.wav'
        
        print(new_signal)
        
        data_array = {'flnm': new_flnm, 'smpl_r': samplerate, 'data': new_signal}
        
        data_io.wrt_snd(data_array)
        
        t1 = time.time()
        
        print(f'Noise added to one .wav files. Stored in ESC-50-master/audio_noise1 folder. Took {round(t1-t0,2)} seconds to run')
        
    if sys.argv[1] =='sngl_note':
        
        samplerate = 44100
        # To get a 1 second long wave of frequency 440Hz
        a_wave = get_wave(samplerate, 440, 0.5)

        #wave features
        print(len(a_wave)) # 44100
        print(np.max(a_wave)) # 4096
        print(np.min(a_wave)) # -4096
        write('a_note.wav', samplerate, a_wave)
        
    if sys.argv[1] == 'two_notes':
        
        samplerate = 44100
        duration = 1.0
        amp = 3000
        # To get a 1 second long wave of frequency 440Hz
        a_wave = get_wave(samplerate, 440, amp,duration)
        c_wave = get_wave(samplerate, 261.63, amp, duration)
        
        third = a_wave + c_wave        
        
        #wave features
        print(len(a_wave), len(c_wave)) # 44100
        print(np.max(a_wave), np.max(c_wave)) # 4096
        print(np.min(a_wave), np.min(c_wave)) # -4096
        
        fn = r'/home/carl1/Projects/ESC-50-master/audio_a_note/third_ac.wav'
        write(fn, samplerate, third)
        

        
        