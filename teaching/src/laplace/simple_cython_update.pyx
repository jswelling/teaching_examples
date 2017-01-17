#! /usr/bin/env python

import numpy as np

cimport numpy as np
cimport cython

DTYPE = np.float
ctypedef np.float_t DTYPE_t

@cython.boundscheck(False)
def update(np.ndarray[DTYPE_t, ndim=2] gOld, np.ndarray[DTYPE_t, ndim=2] gNew):
    gNew[0, :] = gOld[0, :]
    gNew[-1, :] = gOld[-1, :]
    gNew[:, 0] = gOld[:, 0]
    gNew[:, -1] = gOld[:, -1]
    cdef int i, j
    for i in xrange(1, gOld.shape[0] - 1):
        for j in xrange(1, gOld.shape[1] - 1):
            gNew[i, j] = 0.25 * (gOld[i - 1, j] + gOld[i + 1, j]
                                 + gOld[i, j - 1] + gOld[i, j + 1])
    np.copyto(gOld, gNew)
