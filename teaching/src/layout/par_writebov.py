#! /usr/bin/env python

'''
Created on April 23 2021

@author: welling
'''

import numpy as np
from layout import Layout

COUNTER = 0  # counts calls across time
LAYOUT = None  # information about the layout
LLC_TUPLE = None  # global lower left corner x, y, z
TRB_TUPLE = None  # top right back corner x, y, z


def initBOV(nranks, gbl_shape, bricklet_shape, gbl_llfc_xyz, gbl_trbc_xyz):
    """
    The layout here assumes that rank 0 will include llfc (the lower left front corner)
    and rank (nranks-1) will include trbc (the top right back corner)
    """
    global COUNTER
    global LAYOUT
    global LLC_TUPLE
    global TRB_TUPLE
    LAYOUT = Layout(nranks, bricklet_shape, gbl_shape)
    LLC_TUPLE = tuple(gbl_llfc_xyz)
    TRB_TUPLE = tuple(gbl_trbc_xyz)
    COUNTER = 0


def writeBOV(rank, g):
    """g is presumed to be a numpy 2D or 3D array of doubles or 32-bit ints"""
    global COUNTER
    bovNm = 'file_%03d.bov' % COUNTER
    dataNm = 'file_%03d-%d.data' % (COUNTER, rank)
    dataNmProto = 'file_%03d-%%d.data' % COUNTER
    COUNTER += 1
    if rank == 0:
        with open(bovNm, 'w') as f:
            f.write('TIME: %g\n' % float(COUNTER))
            f.write('DATA_FILE: %s\n' % dataNmProto)
            assert g.shape == LAYOUT.shape, f"array passed in rank {rank} has the wrong shape"
            f.write('DATA_SIZE: %d %d %d\n' % LAYOUT.gbl_shape)
            f.write('DATA_BRICKLETS: %d %d %d\n' % g.shape)
            if g.dtype == np.float64:
                f.write('DATA_FORMAT: DOUBLE\n')
            elif g.dtype == np.int32:
                f.write('DATA_FORMAT: INT\n')
            else:
                raise RuntimeError(f'unexpected data type {g.dtype}')
            f.write('VARIABLE: U\n')
            f.write('DATA_ENDIAN: LITTLE\n')
            f.write('CENTERING: ZONAL\n')
            llf_x, llf_y, llf_z = LLC_TUPLE
            trb_x, trb_y, trb_z = TRB_TUPLE
            f.write(f'BRICK_ORIGIN: {llf_x} {llf_y} {llf_z}\n')
            f.write(f'BRICK_SIZE: {trb_x - llf_x} {trb_y - llf_y} {trb_z - llf_z}\n')
    with open(dataNm, 'w') as f:
        g.T.tofile(f)  # BOV format expects Fortran order

from mpi4py import MPI
def main():
    """
    This is a test routine for writeBov
    """
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    gbl_shape = (128, 128, 128)
    gbl_llf = (-0.5, -0.5, -0.5)
    gbl_trb = (0.5, 0.5, 0.5)
    print(f"Hello from {rank} of {size}")
    assert gbl_shape[0] % size == 0, "128 must be divisible by the number of ranks"
    lcl_shape = (gbl_shape[0]//size, gbl_shape[1], gbl_shape[2])
    initBOV(size, gbl_shape, lcl_shape, gbl_llf, gbl_trb)
    print(f"{rank} init complete")
    g = np.zeros(lcl_shape)
    g[:,:,:] = rank
    writeBOV(rank, g)
    
if __name__ == "__main__":
    main()
