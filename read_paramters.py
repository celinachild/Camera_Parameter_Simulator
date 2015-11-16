# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 15:17:51 2015

@author: DongwonShin
"""
import numpy as np

def read_paramters_from_file(filename):
    
    f = open(filename,'r').read().split()
    
    A = np.zeros(9,dtype=np.float64)
    R = np.zeros(9,dtype=np.float64)
    t = np.zeros(3,dtype=np.float64)
    
    for i in range(0, len(f)):
        
        if (i < 9):
            A[i] = float(f[i])
            
        if (9 <= i < 18):
            R[i-9] = float(f[i])
        
        if (18 <= i):
            t[i-18] = float(f[i])
            
    A = np.reshape(A, (3,3))
    R = np.reshape(R, (3,3))
    
    return A,R,t
    
if __name__ ==  "__main__":
    A,R,t = read_paramters_from_file('param/20150602/cam1.txt')
    print A
    print R
    print t