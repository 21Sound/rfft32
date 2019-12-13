# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 10:44:28 2019

@author: hjaeger
"""

import numpy as np

if __name__ == '__main__':
    n = 4096
    bits = 32
    intfactor = 2**(bits-1)
    maxnum = 2**(bits-1)-1
    minnum = -2**(bits-1)+1
    
    nfft = n//2
    
    tableStr = "{" + str(nfft) + ", "
    
    for i in range(nfft//2):
        tmp = max(minnum, min(maxnum, round(+np.cos(2*np.pi*i/nfft)*intfactor)))
        tableStr += str(int(tmp)) + ", "
        tmp = max(minnum, min(maxnum, round(-np.sin(2*np.pi*i/nfft)*intfactor)))
        tableStr += str(int(tmp)) + ", "
    
    for i in range(nfft//2):
        tmp = max(minnum, min(maxnum, round(np.cos(np.pi*i/nfft)*intfactor)))
        tableStr += str(int(tmp)) + ", "
        
    print(tableStr[:-2] + "}")