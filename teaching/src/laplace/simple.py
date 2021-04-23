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


def update(gOld, gNew):
    gNew[0, :] = gOld[0, :]
    gNew[-1, :] = gOld[-1, :]
    gNew[:, 0] = gOld[:, 0]
    gNew[:, -1] = gOld[:, -1]
    for i in range(1, gOld.shape[0] - 1):
        for j in range(1, gOld.shape[1] - 1):
            gNew[i, j] = 0.25 * (gOld[i - 1, j] + gOld[i + 1, j]
                                 + gOld[i, j - 1] + gOld[i, j + 1])
    np.copyto(gOld, gNew)


def main():
    gOld = initialize(90, 110)
    gNew = np.zeros_like(gOld)
#     writeBOV(gOld)

    for n in range(20000):  # @UnusedVariable
        update(gOld, gNew)
    print(gOld)
#         writeBOV(gOld)

if __name__ == '__main__':
    main()
