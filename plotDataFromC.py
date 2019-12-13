# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 12:10:07 2019

@author: hjaeger
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from cffi import FFI
import time

buildPath = './../build-rfft32-Desktop_Qt_5_13_0_MinGW_64_bit-Release'

if __name__ == '__main__':
    
    NFFT = 4096
    int32Scaler = (2**31-1)
    
    with open(os.path.join(buildPath, 'rfftResult.raw'), 'rb') as f:
        rfftResRaw = f.read()  
    rfftRes = np.frombuffer(rfftResRaw, np.float64)
    
    with open(os.path.join(buildPath, 'irfftResult.raw'), 'rb') as f:
        irfftResRaw = f.read()
    irfftRes = np.frombuffer(irfftResRaw, np.float64)
    
    plt.close('all')
    plt.figure()
    
    plt.subplot(2,1,1)
    plt.plot(rfftRes)
    plt.plot(np.abs(np.fft.rfft(irfftRes))/NFFT)
    plt.grid()
    plt.xlabel('Frequency bin N')
    plt.ylabel('Amplitude A [NV]')
    plt.subplot(2,1,2)
    plt.plot(irfftRes)
    plt.grid()
    plt.xlabel('Time bin N')
    plt.ylabel('Amplitude A [NV]')
    plt.tight_layout()
    
    ###
    ffi = FFI()
    rfft32lib = ffi.dlopen(os.path.join(buildPath, 'librfft32.dll'))
    
    ffi.cdef("""
     typedef struct {
    int32_t re,im;
    } complex32;
     
    void init_rfft32();
    void rfft32(int32_t *input, complex32 *spectrum);
    void irfft32(complex32 *spectrum, int32_t *output);
    """)
    
    inp = (np.sin(2.0*np.pi*np.arange(NFFT)*1000.0/44100.0)*int32Scaler).astype(np.int32);
    spec = np.zeros(NFFT+2).astype(np.int32)
    absSpec = np.zeros(NFFT//2+1)
    outp = np.zeros(NFFT).astype(np.int32)
    
    pInp = ffi.cast("int32_t *", inp.ctypes.data)
    pSpec = ffi.cast("complex32 *", spec.ctypes.data)
    pOutp = ffi.cast("int32_t *", outp.ctypes.data)
    
    rfft32lib.init_rfft32()
    rfft32lib.rfft32(pInp, pSpec)
    rfft32lib.irfft32(pSpec, pOutp)
    
    for i in range(NFFT//2+1):
        absSpec[i] = np.sqrt(float(spec[2*i])**2 + float(spec[2*i+1])**2) / int32Scaler
    
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(absSpec)
    plt.grid()
    plt.xlabel('Frequency bin N')
    plt.ylabel('Amplitude A [NV]')
    plt.subplot(2,1,2)
    plt.plot(outp/int32Scaler)
    plt.grid()
    plt.xlabel('Time bin N')
    plt.ylabel('Amplitude A [NV]')
    plt.tight_layout()
    
    startTime = time.clock()
    for i in range(10000):
        np.fft.rfft(inp)
    npRfftTime = time.clock() - startTime
    print('numpy rfft needed: '+str(npRfftTime) + "s for 10k iterations")
    
    startTime = time.clock()
    for i in range(10000):
        rfft32lib.rfft32(pInp, pSpec)
    cffiRfftTime = time.clock() - startTime
    print('cffi rfft needed: '+str(cffiRfftTime) + "s for 10k iterations")