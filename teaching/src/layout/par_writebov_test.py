import numpy as np
from mpi4py import MPI

from par_writebov import writeBOV, writePoint3D, initBOVAndPoint3D

def main():
    """
    This is a test routine for writeBov and writePoint3D
    """

    # MPI initialization
    comm = MPI.COMM_WORLD
    nranks = comm.Get_size()
    rank = comm.Get_rank()

    # Figure out where this rank is in space, grid-wise and spatially
    gbl_shape = (128, 128, 128)
    gbl_llf = np.array((-0.5, -0.5, -0.5))
    gbl_trb = np.array((0.5, 0.5, 0.5))
    assert gbl_shape[0] % nranks == 0, "128 must be divisible by the number of ranks"
    lcl_shape = (gbl_shape[0]//nranks, gbl_shape[1], gbl_shape[2])
    gbl_size = gbl_trb - gbl_llf
    lcl_size = gbl_size / np.array((float(nranks), 1.0, 1.0))
    rank_shift = np.array((lcl_size[0], 0.0, 0.0))
    lcl_llf = gbl_llf + rank * rank_shift
    lcl_trb = lcl_llf + lcl_size
    print(f'rank {rank} gbl_size: {gbl_size}  lcl_size: {lcl_size}  local corners: {lcl_llf}, {lcl_trb}')

    # Use this info to initialize the writer
    initBOVAndPoint3D(rank, nranks, gbl_shape, lcl_shape, gbl_llf, gbl_trb)
    print(f"rank {rank} init complete")

    # Each rank contributes to sample dataset with regions colored by rank
    g = np.zeros(lcl_shape)
    g[:,:,:] = rank
    writeBOV(rank, g)
    
    # Each rank contributes a group of points located randomly within
    # its volume, colored by rank
    npts = 10
    pts = lcl_llf + np.random.random((npts, 3)) * lcl_size
    rank_column = np.array(npts * [[rank]])
    pts = np.append(pts, rank_column, axis=1)
    writePoint3D(rank, pts)
    
if __name__ == "__main__":
    main()
