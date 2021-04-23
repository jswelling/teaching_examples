#! /usr/bin/env python

'''
Created on Jan 10, 2016

@author: welling
'''

import numpy as np
import pyximport
pyximport.install(setup_args={'include_dirs':[np.get_include()]})
import simple_cython_update


def initialize(xDim, yDim):
    gOld = np.zeros([xDim, yDim])
    gOld[-1, :] = 1.0
    gOld[:, -1] = 1.0
    return gOld


def main():
    gOld = initialize(90, 110)
    gNew = np.zeros_like(gOld)
#     writeBOV(gOld)

    for n in range(20000):  # @UnusedVariable
        simple_cython_update.update(gOld, gNew)
    print(gOld)
#         writeBOV(gOld)

if __name__ == '__main__':
    main()
