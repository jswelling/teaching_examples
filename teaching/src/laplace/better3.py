#! /usr/bin/env python

'''
Created on Jan 10, 2016

@author: welling
'''

import numpy as np


def initialize(xDim, yDim):
    gOld = np.zeros([xDim, yDim])
    gOld[-1, :] = 1.0
    gOld[:, -1] = 1.0
    return gOld


def update(gOld):
    gNew = np.empty_like(gOld)
    gNew[1:-1, 1:-1] = 0.25 * (gOld[0:-2, 1:-1] + gOld[2:, 1:-1]
                               + gOld[1:-1, 0:-2] + gOld[1:-1, 2:])
    gNew[0, :] = gOld[0, :]
    gNew[-1, :] = gOld[-1, :]
    gNew[:, 0] = gOld[:, 0]
    gNew[:, -1] = gOld[:, -1]
    return gNew


def main():
    gOld = initialize(90, 110)
#     writeBOV(gOld)

    for n in xrange(20000):  # @UnusedVariable
        gOld = update(gOld)
#         if (n + 1) % 100 == 0:
#             writeBOV(gOld)
    print gOld

if __name__ == '__main__':
    main()
