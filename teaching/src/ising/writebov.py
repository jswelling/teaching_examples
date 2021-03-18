#! /usr/bin/env python

'''
Created on Jan 10, 2016

@author: welling
'''

import numpy as np

counter = 0


def writeBOV(g):
    """g is presumed to be a numpy 2D array of doubles"""
    global counter
    bovNm = 'file_%03d.bov' % counter
    dataNm = 'file_%03d.doubles' % counter
    counter += 1
    with open(bovNm, 'w') as f:
        f.write('TIME: %g\n' % float(counter))
        f.write('DATA_FILE: %s\n' % dataNm)
        f.write('DATA_SIZE: %d %d 1\n' % g.shape)
        f.write('DATA_FORMAT: DOUBLE\n')
        f.write('VARIABLE: U\n')
        f.write('DATA_ENDIAN: LITTLE\n')
        f.write('CENTERING: ZONAL\n')
        f.write('BRICK_ORIGIN: 0. 0. 0.\n')
        f.write('BRICK_SIZE: 1.0 1.0 1.0\n')
    with open(dataNm, 'w') as f:
        g.T.tofile(f)  # BOV format expects Fortran order
