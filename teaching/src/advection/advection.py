#! /usr/bin/env python

'''
Created on Jan 10, 2016

@author: welling
'''

import numpy as np
import writecurve

import math
import random

XDIM = 100

tMax = 400.0
dx = 2.0/XDIM  # So this is .02; total interval is -1.0 to 1.0
c = 0.01
dt = 1.0  # 2.0 corresponds to xi of 1


def iToX(i):
    return (i - 0.5*(XDIM-1))*dx


def iToXShift(i, t):
    xShift = iToX(i) - c*t
    cycles = math.floor(0.5*(xShift+1.0))
    xShift = xShift-cycles*2.0
    return xShift


def initval(x, shape='gaussian'):
    ctrX = 0.0
    sigma = 0.25
    maxU = 1.0

    if shape == 'gaussian':
        distSqr = (x-ctrX)*(x-ctrX)
        U = maxU*math.exp(-distSqr/(sigma*sigma))

    elif shape == 'tophat':
        if math.fabs(x) <= sigma:
            U = 1.0
        else:
            U = 0.0

    elif shape == 'random':
        U = sigma*(random.random() - 0.5)

    else:
        raise RuntimeError('Unknown shape %s' % shape)

    return U


def initializeU(shape='gaussian'):
    U = np.empty(XDIM)
    for i in xrange(XDIM):
        U[i] = initval(iToX(i), shape=shape)
    return U


def tridiagonal(v1, v2, v3):
    am1 = np.empty(XDIM-1)
    am1.fill(v1)
    a0 = np.empty(XDIM)
    a0.fill(v2)
    ap1 = np.empty(XDIM-1)
    ap1.fill(v3)
    return np.diag(am1, -1)+np.diag(a0, 0) + np.diag(ap1, 1)


matNew = None
matNewInv = None
matCurrent = None


def doTimeStep(U, UOld, mthd='lax'):
    global matNew, matCurrent, matNewInv
    xi = c*(dt/dx)
    Uip1 = np.roll(U, -1)  # shift left by 1
    Uim1 = np.roll(U, +1)  # shift right by 1

    if mthd == 'simple':
        # Simple, unstable
        UNew = U - ((Uip1 - Uim1) * 0.5 * xi)

    elif mthd == 'lax':
        # Lax
        UNew = ((Uip1 + Uim1) * 0.5) - ((Uip1 - Uim1) * 0.5 * xi)

    elif mthd == 'upwind':
        # upwind
        UNew = U - ((U - Uim1) * xi)

    elif mthd == 'crank':
        # Crank-Nicholson
        if matNew is None:
            matNew = tridiagonal(-0.25 * xi, 1.0, 0.25 * xi)
            matNew[0, XDIM - 1] = -0.25 * xi
            matNew[XDIM - 1, 0] = 0.25 * xi
        if matNewInv is None:
            matNewInv = np.linalg.inv(matNew)
        if matCurrent is None:
            matCurrent = tridiagonal(0.25 * xi, 1.0, -0.25 * xi)
            matCurrent[0, XDIM - 1] = 0.25 * xi
            matCurrent[XDIM - 1, 0] = -0.25*xi
        matU = np.transpose(np.matrix(U))
        matUNew = np.dot(np.dot(matNewInv, matCurrent), matU)
        UNew = np.squeeze(np.asarray(matUNew))
    else:
        raise RuntimeError('Unknown method %s' % mthd)

    return UNew


def timeToOutput(t, count):
    return (count % 1 == 0)


def main():

    print "Running with xi= %g" % (c * dt / dx)
    shape = 'gaussian'
    mthd = 'simple'

    U = initializeU(shape)
    UOld = np.copy(U)

    t = 0.0
    count = 0
    while t < tMax:
        if timeToOutput(t, count):
            writecurve.writeCurve('U', [(iToXShift(i, t), v) for i, v in enumerate(U)])
        UNew = doTimeStep(U, UOld, mthd=mthd)

        # Rather than copy matrix contents, just let the old one get garbage-collected
        UOld = U
        U = UNew
        UNew = None  # just as a reminder
        count += 1
        t += dt

if __name__ == '__main__':
    main()
