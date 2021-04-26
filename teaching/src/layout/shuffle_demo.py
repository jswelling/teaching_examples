import sys
import numpy as np
from mpi4py import MPI

from layout import Layout
from par_bovwriter import BOVWriter

GBL_SHAPE= (128, 128, 128)
GBL_LLF = np.array((-0.5, -0.5, -0.5))
GBL_TRB = np.array((0.5, 0.5, 0.5))

def get_corners(rank, layout, llf, trb):
    rank_indices = layout.get_rank_indices(rank)
    deltas = (trb - llf) / np.array(layout.ranks_per_edge)
    my_llf = llf + (rank_indices * deltas)
    my_trb = my_llf + deltas
    return my_llf, my_trb

def main():
    """
    This is a demonstration of global shuffling
    """

    # Sample layouts
    before_layout = xy_slab_layout = Layout(8, (128, 128, 16), GBL_SHAPE)
    after_layout = z_pencil_layout = Layout(8, (64, 32, 128), GBL_SHAPE)

    # MPI initialization
    comm = MPI.COMM_WORLD
    nranks = comm.Get_size()
    assert nranks == before_layout.nranks, "before_layout has the wrong number of ranks"
    assert nranks == after_layout.nranks, "after_layout has the wrong number of ranks"
    rank = comm.Get_rank()

    # We are going to write two sets of BOV files
    before_writer = BOVWriter('before', 'before', rank, nranks, before_layout.gbl_shape, before_layout.shape,
                              GBL_LLF, GBL_TRB)
    after_writer = BOVWriter('after', 'after', rank, nranks, after_layout.gbl_shape, after_layout.shape,
                              GBL_LLF, GBL_TRB)
                              
    # Figure out where this rank is in space, grid-wise and spatially
    before_rank_indices = before_layout.get_rank_indices(rank)
    print(f'{rank}: before_rank_indices: {before_rank_indices}')
    after_rank_indices = after_layout.get_rank_indices(rank)
    print(f'{rank}: after_rank_indices: {after_rank_indices}')
    before_lcl_llf, before_lcl_trb = get_corners(rank, before_layout, GBL_LLF, GBL_TRB)
    print(f'{rank}: corners before shuffle: {before_lcl_llf} {before_lcl_trb}')
    after_lcl_llf, after_lcl_trb = get_corners(rank, after_layout, GBL_LLF, GBL_TRB)
    print(f'{rank}: corners after shuffle: {after_lcl_llf} {after_lcl_trb}')

    # Save bov files containing our rank before and after.
    data = np.zeros(before_layout.shape, dtype=np.int32)
    data[:,:,:] = rank
    before_writer.writeBOV(data)
    data = np.zeros(after_layout.shape, dtype=np.int32)
    data[:,:,:] = rank
    after_writer.writeBOV(data)

    # Make an array where each cell contains the rank that will be associated with that location after
    # the shuffle.
    data = np.zeros(before_layout.shape, dtype=np.int32)
    for i in range(before_layout.shape[0]):
        for j in range(before_layout.shape[1]):
            for k in range(before_layout.shape[2]):
                gbl_idx = before_layout.lcl_to_gbl(rank, (i,j,k))
                after_rank, after_idx = after_layout.gbl_to_lcl(gbl_idx)
                data[i,j,k] = after_rank
    print(f'{rank}: done building!')
    before_writer.writeBOV(data)  # This should look like the output of after_writer above

    # Shuffle our data by adding indices and permuting so that all cells destined for the same
    # destination rank are sequential.
    data = data.reshape((2, 64, 4, 32, 16))
    data = np.transpose(data, axes=[0, 2, 1, 3, 4])
    print(data.shape)
    data = data.reshape(2, 4, 32*64*16)
    dest_rank = 0
    for i in range(2):
        for j in range(4):
            #print(f'({i}, {j}): {data[i,j,:]}')
            #print(f'({i}, {j}): {data[i,31,j,31,:]}')
            if not np.all(data[i, j, :] == dest_rank):
                print(f'{rank}: Nope on {dest_rank}')
            dest_rank += 1
    
    # The following reshape had better work, or there is not a match between the number of
    # communicating ranks and the number of data blocks- which means we picked inappropriate
    # layouts
    data = data.reshape(nranks, -1)

    # Actually swap the data.  After the alltoall, rcvbuf will contain regions from all ranks
    # of the input data array.
    rcvbuf = np.empty_like(data)
    comm.Alltoall(data, rcvbuf)
    if not np.all(rcvbuf[:,:] == rank):
        print(f'{rank}: Nope on recv')

    # And restore the shape of rcvbuf
    rcvbuf = rcvbuf.reshape(32, 63, 128)

            
    sys.exit('done')
    gbl_size = gbl_trb - gbl_llf
    lcl_size = gbl_size / np.array((float(nranks), 1.0, 1.0))
    rank_shift = np.array((lcl_size[0], 0.0, 0.0))
    lcl_llf = gbl_llf + rank * rank_shift
    lcl_trb = lcl_llf + lcl_size
    print(f'rank {rank} gbl_size: {gbl_size}  lcl_size: {lcl_size}  local corners: {lcl_llf}, {lcl_trb}')

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
