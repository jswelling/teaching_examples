#! /usr/bin/env python

import numpy as np

LEN = 14

def trickfun(aVec, bVec, cVec):
    for i in xrange(aVec.shape[0]):
        aVec[i] += (bVec[i] + cVec[i])
    return aVec

def vecfun(aVec, bVec, cVec):
    aVec += bVec
    aVec += cVec
    return aVec

def main():
    aVec = np.zeros(LEN)
    bVec = np.full(LEN, 2.0)
    cVec = np.full(LEN, 3.0)
    aVec = trickfun(aVec, bVec, cVec)
    print "\n---used as intended---"
    for i, val in enumerate(aVec):
        print '%s: %8.0f' % (i, val)
        
    aVec = np.zeros(LEN)
    aVec[0] = 1.0
    aVec[1] = 2.0
    subVec = trickfun(aVec[2:], aVec[:-2], aVec[1:-1])
    print "\n---the Fibonacci trick---"
    for i, val in enumerate(aVec):
        print '%s: %8.0f' % (i, val)
    
    aVec = np.zeros(LEN)
    aVec[0] = 1.0
    aVec[1] = 2.0
    subVec = vecfun(aVec[2:], aVec[:-2], aVec[1:-1])
    print "\n---vectorized version ---"
    for i, val in enumerate(aVec):
        print '%s: %8.0f' % (i, val)
    

if __name__ == "__main__":
    main()
