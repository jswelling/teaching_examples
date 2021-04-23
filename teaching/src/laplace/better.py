#! /usr/bin/env python

'''
Created on Jan 10, 2016

@author: welling
'''

import numpy as np
from scipy.ndimage.interpolation import shift


def shiftI(xs, n):
    return shift(xs, [n, 0], order=0)


def shiftJ(xs, n):
    return shift(xs, [0, n], order=0)


def initialize(xDim, yDim):
    gOld = np.zeros([xDim, yDim], order=2)
    gOld[-1, :] = 1.0
    gOld[:, -1] = 1.0
    return gOld


def update(gOld):
    gNew = 0.25 * (shiftI(gOld, 1) + shiftI(gOld, -1)
                   + shiftJ(gOld, 1) + shiftJ(gOld, -1))
    gNew[0, :] = gOld[0, :]
    gNew[-1, :] = gOld[-1, :]
    gNew[:, 0] = gOld[:, 0]
    gNew[:, -1] = gOld[:, -1]
    return gNew


def main():
    gOld = initialize(90, 110)

    for n in range(20000):  # @UnusedVariable
        gOld = update(gOld)
#         if (n + 1) % 100 == 0:
#             writeBOV(gOld)
    print(gOld)

if __name__ == '__main__':
    main()
