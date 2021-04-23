#! /usr/bin/env python

'''
Created on Jan 10, 2016

@author: welling
'''

import numpy as np

counter = 0


def writeBOV(g):
    """g is presumed to be a numpy 2D or 3D array of doubles or 32-bit ints"""
    global counter
    bovNm = 'file_%03d.bov' % counter
    dataNm = 'file_%03d.data' % counter
    counter += 1
    with open(bovNm, 'w') as f:
        f.write('TIME: %g\n' % float(counter))
        f.write('DATA_FILE: %s\n' % dataNm)
        if len(g.shape) == 2:
            f.write('DATA_SIZE: %d %d 1\n' % g.shape)
        elif len(g.shape) == 3:
            f.write('DATA_SIZE: %d %d %d\n' % g.shape)
        else:
            raise RuntimeError(f'unexpected shape {g.shape}')
        if g.dtype == np.float64:
            f.write('DATA_FORMAT: DOUBLE\n')
        elif g.dtype == np.int32:
            f.write('DATA_FORMAT: INT\n')
        else:
            raise RuntimeError(f'unexpected data type {g.dtype}')
        f.write('VARIABLE: U\n')
        f.write('DATA_ENDIAN: LITTLE\n')
        f.write('CENTERING: ZONAL\n')
        f.write('BRICK_ORIGIN: 0. 0. 0.\n')
        f.write('BRICK_SIZE: 1.0 1.0 1.0\n')
    with open(dataNm, 'w') as f:
        g.T.tofile(f)  # BOV format expects Fortran order

