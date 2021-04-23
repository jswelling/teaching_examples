#! /usr/bin/env python

'''
Created on April 23 2021

@author: welling
'''

import numpy as np
from pathlib import Path

PTS_INDEX_FNAME = 'point3d_index.visit'  # Name for the index file for all Point3D data
COUNTER = 0  # counts calls across time
PTS_COUNTER = 0  # like COUNTER but for point3D files
NRANKS = None  # total ranks
RANK = None  # this rank
GBL_SHAPE = None  # global array shape
LCL_SHAPE = None  # local array shape
GBL_LLC_TUPLE = None  # global lower left corner x, y, z
GBL_TRB_TUPLE = None  # top right back corner x, y, z


def initBOVAndPoint3D(rank, nranks, gbl_shape, lcl_shape, gbl_llfc_xyz, gbl_trbc_xyz):
    """
    This routine initializes the number of ranks and layout, and resets the time step counters
    to zero.  Note that it will delete the .visit file which connects and Point3D outputs!
    
    The layout here assumes that rank 0 will include llfc (the lower left front corner)
    and rank (nranks-1) will include trbc (the top right back corner).
    """
    global COUNTER
    global PTS_COUNTER
    global NRANKS
    global RANK
    global GBL_SHAPE
    global LCL_SHAPE
    global GBL_LLC_TUPLE
    global GBL_TRB_TUPLE

    RANK = rank
    NRANKS = nranks
    GBL_SHAPE = gbl_shape
    LCL_SHAPE = lcl_shape
    GBL_LLC_TUPLE = tuple(gbl_llfc_xyz)
    GBL_TRB_TUPLE = tuple(gbl_trbc_xyz)
    COUNTER = 0
    PTS_COUNTER = 0

    # Clear out the .visit file for Point3D if it exists
    if rank == 0:
        index_path = Path(PTS_INDEX_FNAME)
        if index_path.exists():
            index_path.unlink()
        index_path.write_text(f'!NBLOCKS {nranks}\n')


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
            assert g.shape == LCL_SHAPE, f"array passed in rank {rank} has the wrong shape"
            f.write('DATA_SIZE: %d %d %d\n' % GBL_SHAPE)
            f.write('DATA_BRICKLETS: %d %d %d\n' % LCL_SHAPE)
            if g.dtype == np.float64:
                f.write('DATA_FORMAT: DOUBLE\n')
            elif g.dtype == np.int32:
                f.write('DATA_FORMAT: INT\n')
            else:
                raise RuntimeError(f'unexpected data type {g.dtype}')
            f.write('VARIABLE: U\n')
            f.write('DATA_ENDIAN: LITTLE\n')
            f.write('CENTERING: ZONAL\n')
            llf_x, llf_y, llf_z = GBL_LLC_TUPLE
            trb_x, trb_y, trb_z = GBL_TRB_TUPLE
            f.write(f'BRICK_ORIGIN: {llf_x} {llf_y} {llf_z}\n')
            f.write(f'BRICK_SIZE: {trb_x - llf_x} {trb_y - llf_y} {trb_z - llf_z}\n')
    with open(dataNm, 'w') as f:
        g.T.tofile(f)  # BOV format expects Fortran order


def writePoint3D(rank, points_array):
    """
    points_array is expected to be an (N,3) or (N,4) array of floats.  For each of the N points,
    the X, Y, and Z coordinates should appear in that order, followed by an optional value
    """
    global PTS_COUNTER
    dataNm = 'file_%03d-%d.3D' % (PTS_COUNTER, rank)
    assert len(points_array.shape) == 2, 'points_array has the wrong shape'
    nsamps, ndim = points_array.shape
    assert ndim in [3, 4], 'there should be X, Y, Z or X, Y, Z, value entries for each point'
    with open(dataNm, 'w') as f:
        f.write('x y z value\n')
        for row in range(nsamps):
            val = points_array[row, 3] if ndim == 4 else 0.0
            f.write(f'{points_array[row, 0]} {points_array[row,1]} {points_array[row,2]} {val}\n')

    if rank == 0:    
        with open(PTS_INDEX_FNAME, 'a') as f:
            f.write(f'!TIME {float(PTS_COUNTER)}\n')
            for row in range(NRANKS):
                rowDataNm = 'file_%03d-%d.3D' % (PTS_COUNTER, row)
                f.write(f'{rowDataNm}\n')

    PTS_COUNTER += 1
