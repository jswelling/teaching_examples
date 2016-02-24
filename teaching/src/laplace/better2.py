#! /usr/bin/env python

'''
Created on Jan 10, 2016

@author: welling
'''

import numpy as np


# Thank you Stack Overflow!
# http://stackoverflow.com/questions/30399534/shift-elements-in-a-numpy-array
def shiftI(xs, n):
    e = np.empty_like(xs)
    if n >= 0:
        e[:n, :] = 0.0
        e[n:, :] = xs[:-n, :]
    else:
        e[n:, :] = 0.0
        e[:n, :] = xs[-n:, :]
    return e


def shiftJ(xs, n):
    e = np.empty_like(xs)
    if n >= 0:
        e[:, :n] = 0.0
        e[:, n:] = xs[:, :-n]
    else:
        e[:, n:] = 0.0
        e[:, :n] = xs[:, -n:]
    return e


def initialize(xDim, yDim):
    gOld = np.zeros([xDim, yDim])
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

    for n in xrange(20000):  # @UnusedVariable
        gOld = update(gOld)
#         if (n + 1) % 100 == 0:
#             writeBOV(gOld)
    print gOld

if __name__ == '__main__':
    main()