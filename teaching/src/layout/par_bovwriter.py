#! /usr/bin/env python

'''
Created on April 23 2021

@author: welling
'''

import numpy as np
from pathlib import Path

class BOVWriter:
    def __init__(self, base_name, variable_name, rank, nranks, gbl_shape, lcl_shape, gbl_llf_xyz, gbl_trb_xyz):
        self.base_name = base_name
        self.var_name = variable_name
        self.rank = rank
        self.nranks = nranks
        self.gbl_shape = gbl_shape
        self.lcl_shape = lcl_shape
        self.gbl_llf_xyz = np.array(gbl_llf_xyz)
        self.gbl_trb_xyz = np.array(gbl_trb_xyz)
        self.counter = 0
        self.pts_counter = 0

        # Clear out the .visit file for Point3D if it exists
        if rank == 0:
            index_path = Path(self.get_pts_index_fname())
            if index_path.exists():
                index_path.unlink()
            index_path.write_text(f'!NBLOCKS {nranks}\n')

    def get_pts_index_fname(self):
        return f'{self.base_name}_3D_index.visit'

    def skip(self):
        """
        Advance BOV and 3D frame numbers without writing output
        """
        self.counter += 1
        self.pts_counter += 1

    def writeBOV(self, g):
        assert g.shape == self.lcl_shape, f"array passed in rank {self.rank} has the wrong shape"
        bovNm = '%s_%03d.bov' % (self.base_name, self.counter)
        dataNm = '%s_%03d-%d.data' % (self.base_name, self.counter, self.rank)
        dataNmProto = '%s_%03d-%%d.data' % (self.base_name, self.counter)
        self.counter += 1
        if self.rank == 0:
            with open(bovNm, 'w') as f:
                f.write('TIME: %g\n' % float(self.counter))
                f.write('DATA_FILE: %s\n' % dataNmProto)
                f.write('DATA_SIZE: %d %d %d\n' % self.gbl_shape)
                f.write('DATA_BRICKLETS: %d %d %d\n' % self.lcl_shape)
                if g.dtype == np.float64:
                    f.write('DATA_FORMAT: DOUBLE\n')
                elif g.dtype == np.int32:
                    f.write('DATA_FORMAT: INT\n')
                else:
                    raise RuntimeError(f'unexpected data type {g.dtype}')
                f.write('VARIABLE: %s\n' % self.var_name)
                f.write('DATA_ENDIAN: LITTLE\n')
                f.write('CENTERING: ZONAL\n')
                llf_x, llf_y, llf_z = self.gbl_llf_xyz
                trb_x, trb_y, trb_z = self.gbl_trb_xyz
                f.write(f'BRICK_ORIGIN: {llf_x} {llf_y} {llf_z}\n')
                f.write(f'BRICK_SIZE: {trb_x - llf_x} {trb_y - llf_y} {trb_z - llf_z}\n')
        with open(dataNm, 'w') as f:
            g.T.tofile(f)  # BOV format expects Fortran order
        

    def writePoint3D(self, points_array):
        """
        points_array is expected to be an (N,3) or (N,4) array of floats.  For each of the N points,
        the X, Y, and Z coordinates should appear in that order, followed by an optional value
        """
        dataNm = '%s_%03d-%d.3D' % (self.base_name, self.pts_counter, self.rank)
        assert len(points_array.shape) == 2, 'points_array has the wrong shape'
        nsamps, ndim = points_array.shape
        assert ndim in [3, 4], 'there should be X, Y, Z or X, Y, Z value entries for each point'
        with open(dataNm, 'w') as f:
            f.write('x y z value\n')
            for row in range(nsamps):
                val = points_array[row, 3] if ndim == 4 else 0.0
                f.write(f'{points_array[row, 0]} {points_array[row,1]} {points_array[row,2]} {val}\n')

        if self.rank == 0:    
            with open(self.get_pts_index_fname(), 'a') as f:
                f.write(f'!TIME {float(self.pts_counter)}\n')
                for row in range(self.nranks):
                    rowDataNm = '%s_%03d-%d.3D' % (self.base_name, self.pts_counter, row)
                    f.write(f'{rowDataNm}\n')

        self.pts_counter += 1
