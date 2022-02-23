#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 19:54:52 2021
script to contain io class

@author: deadpool
"""
import numpy as np
import os
import numpy as np
from scipy.fft import fft, fftfreq
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
    
    def rd_snd(self, sngl_fl=True, fft_tf=False):
        if sngl_fl:
            samplerate, data_arry_fll = wavfile.read(self.flnm)
            
            if fft_tf:
                freq_arry = fftfreq(len(data_arry_fll), d=1/samplerate)
                data_arry = np.stack((freq_arry, fft(data_arry_fll)), 0)
                # print(len(freq_arry), len(data_arry_fll))
                return samplerate, data_arry
            else:
                return samplerate, data_arry_fll
        else:
            data_dct_lst = []
            for flnm in os.listdir(self.fldr):
                if os.path.isfile(os.path.join(self.fldr, flnm)):
                    samplerate, data_arry_fll = wavfile.read(os.path.join(self.fldr, flnm))
                    if fft_tf:
                        freq_arry = fftfreq(len(data_arry_fll), d=1/samplerate)
                        data_arry = np.stack((freq_arry, fft(data_arry_fll)), 0)
                        data_dct_lst.append({'flnm': flnm, 'smpl_rt': samplerate, 'data': data_arry})
                    else:
                        data_dct_lst.append({'flnm': flnm, 'smpl_rt': samplerate, 'data': data_arry_fll})
                    
            return data_dct_lst
        
        
    def wrt_snd(self, data_array, sngl_fl=True, fft_tf=False):
        #do I need to un-do a fft if it was applied?
        if sngl_fl:
            wavfile.write(data_array['flnm'], data_array['smpl_r'], data_array['data'].astype(np.int16))
        else:
            for ele in data_array:
                wavfile.write(ele['flnm'], ele['smpl_r'], ele['data'].astype(np.int16))
            
            
            

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
    
    def prcss_snd(self, snd_data, step_sz=1000, sngl_fl=False):
        if sngl_fl:
           l = np.arange(0,len(snd_data[0]), step_sz) 
           snd_piece = []
           for i in l[1:]:
               snd_piece.append(np.average(snd_data[i-1:i]))
           return np.array(snd_piece)
        else:
            smooth_snd_dct_lst = []
            l = np.arange(0,len(snd_data[0]['data']), 1000)
            for snd in snd_data:
                snd_piece = []
                for i in l[1:]:
                    snd_piece.append(np.average(snd['data'][i-1:i]))
                    
                new_flnm = os.path.join(self.fldr, snd['flnm'][:-4]+'_smooth.wav')
                new_signal = np.array(snd_piece)
                dct_lst = {'flnm': new_flnm, 'smpl_r': int(snd['smpl_rt']/step_sz), 'data': new_signal}
                smooth_snd_dct_lst.append(dct_lst)
            return smooth_snd_dct_lst
        
        