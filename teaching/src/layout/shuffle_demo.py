#! /usr/bin/env python

"""
This sample program demonstrates and tests swapping data between ranks in the pattern appropriate for 
X-Y slabs swapping with Z pencils.  Run it like:

    mpirun -n 8 python shuffle_demo.py
"""

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


def shuffle_and_swap(comm, sendbuf, before_layout, after_layout):
    """
    This reordering and transmission pattern is customized for the XY-plane-to-Z-pencil
    layout pattern.
    """
    # Shuffle our data by adding indices and permuting so that all cells destined for the same
    # destination rank are sequential.
    before_nx, before_ny, before_nz = before_layout.shape
    after_nx, after_ny, after_nz = after_layout.shape
    assert before_layout.nranks == after_layout.nranks, "Different numbers of ranks before and after swap?"
    assert after_nz / before_nz == before_layout.nranks, ("The before layout rank does not contribute to"
                                                          " all after-layout ranks")
    assert (before_nx // after_nx) * (before_ny // after_ny) == after_layout.nranks, "shape mismatch?"
    assert sendbuf.shape == before_layout.shape, "send buffer is the wrong shape?"
    sendbuf = sendbuf.reshape((before_nx // after_nx, after_nx, before_ny // after_ny, after_ny, before_nz))
    sendbuf = np.transpose(sendbuf, axes=[0, 2, 1, 3, 4])
    # two reshaping steps for clarity, even though we could accomplish the same with only one
    sendbuf = sendbuf.reshape(before_nx // after_nx, before_ny // after_ny, -1)
    sendbuf = sendbuf.reshape(after_layout.nranks, -1)

    # Actually swap the data.  After the alltoall, rcvbuf will contain regions from all ranks
    # of the input data array.
    rcvbuf = np.empty_like(sendbuf)
    comm.Alltoall(sendbuf, rcvbuf)

    # At this point all the data expected for the 'after' layout is present in rcvbuf, but it
    # is not in the right order.  It arrived with the lowest src rank in the buffer before the
    # next lowest src rank, and that is not what we want.
    rcvbuf = rcvbuf.reshape(after_layout.nranks,
                            after_nx, after_ny,
                            after_nz // after_layout.nranks)
    rcvbuf = np.transpose(rcvbuf, [1, 2, 0, 3])
    rcvbuf = rcvbuf.reshape(after_nx, after_ny, after_nz)
    return rcvbuf


def reverse_shuffle_and_swap(comm, sendbuf, before_layout, after_layout):
    """
    This reordering and transmission pattern is customized for the Z-pencil-to-XY-plane
    layout pattern.
    """
    # Shuffle our data by adding indices and permuting so that all cells destined for the same
    # destination rank are sequential.
    before_nx, before_ny, before_nz = before_layout.shape  # the pencil layout
    after_nx, after_ny, after_nz = after_layout.shape  # the slab layout
    assert before_layout.nranks == after_layout.nranks, "Different numbers of ranks before and after swap?"
    assert before_nz / after_nz == after_layout.nranks, ("The before layout rank does not contribute to"
                                                          " all after-layout ranks")
    assert (after_nx // before_nx) * (after_ny // before_ny) == before_layout.nranks, "shape mismatch?"
    assert sendbuf.shape == before_layout.shape, "send buffer is the wrong shape?"
    sendbuf = sendbuf.reshape((before_nx, before_ny, before_nz // after_nz, after_nz))
    sendbuf = np.transpose(sendbuf, axes=[2, 0, 1, 3])
    sendbuf = sendbuf.reshape(after_layout.nranks, -1)

    # Actually swap the data.  After the alltoall, rcvbuf will contain regions from all ranks
    # of the input data array.
    rcvbuf = np.empty_like(sendbuf)
    comm.Alltoall(sendbuf, rcvbuf)

    # At this point all the data expected for the 'after' layout is present in rcvbuf, but it
    # is not in the right order.  It arrived with the lowest src rank in the buffer before the
    # next lowest src rank, and that is not what we want.
    rcvbuf = rcvbuf.reshape((after_nx // before_nx, after_ny // before_ny, before_nx, before_ny, after_nz))
    rcvbuf = np.transpose(rcvbuf, [0, 2, 1, 3, 4])
    rcvbuf = rcvbuf.reshape(after_nx, after_ny, after_nz)
    return rcvbuf


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
    sent_writer = BOVWriter('sent', 'sent', rank, nranks, before_layout.gbl_shape, before_layout.shape,
                            GBL_LLF, GBL_TRB)
    received_writer = BOVWriter('received', 'received', rank, nranks, after_layout.gbl_shape, after_layout.shape,
                                GBL_LLF, GBL_TRB)
    expected_writer = BOVWriter('expected', 'expected', rank, nranks, after_layout.gbl_shape, after_layout.shape,
                                GBL_LLF, GBL_TRB)
    returned_writer = BOVWriter('returned', 'returned', rank, nranks, before_layout.gbl_shape, before_layout.shape,
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

    # First test: all senders send their own rank.  Do the results go to the right place?
    sendbuf = np.zeros(before_layout.shape, dtype=np.int32)
    sendbuf[:,:,:] = rank
    sent_writer.writeBOV(sendbuf)
    # Perform the swap, and verify that everything ended up on the correct rank
    rcvbuf = shuffle_and_swap(comm, sendbuf, before_layout, after_layout)
    received_writer.writeBOV(rcvbuf)
    expected = np.empty(after_layout.shape, dtype=np.int32)
    for i in range(after_layout.shape[0]):
        for j in range(after_layout.shape[1]):
            for k in range(after_layout.shape[2]):
                gbl_idx = after_layout.lcl_to_gbl(rank, (i,j,k))
                before_rank, before_idx = before_layout.gbl_to_lcl(gbl_idx)
                expected[i,j,k] = before_rank
    print(f'{rank}: done building comparison rank array')
    expected_writer.writeBOV(expected)
    if np.all(rcvbuf == expected):
        print(f'{rank}: source-side rank comparison succeeded')
    else:
        print(f'{rank}: source-side rank comparison failed')
    returnbuf = reverse_shuffle_and_swap(comm, rcvbuf, after_layout, before_layout)
    if np.all(returnbuf == sendbuf):
        print(f'{rank}: source-side rank return comparison succeeded')
    else:
        print(f'{rank}: source-side rank return comparison failed')
    returned_writer.writeBOV(returnbuf)

    # Second test: for X, Y, and Z in turn, have each sender send the global index of
    # each cell.
    for axis, axisname in enumerate("XYZ"):
        sendbuf = np.empty(before_layout.shape, dtype=np.int32)
        for i in range(before_layout.shape[0]):
            for j in range(before_layout.shape[1]):
                for k in range(before_layout.shape[2]):
                    gbl_idx = before_layout.lcl_to_gbl(rank, (i, j, k))
                    sendbuf[i, j, k] = gbl_idx[axis]
        expected = np.empty(after_layout.shape, dtype=np.int32)
        for i in range(after_layout.shape[0]):
            for j in range(after_layout.shape[1]):
                for k in range(after_layout.shape[2]):
                    gbl_idx = after_layout.lcl_to_gbl(rank, (i, j, k))
                    expected[i, j, k] = gbl_idx[axis]
        rcvbuf = shuffle_and_swap(comm, sendbuf, before_layout, after_layout)
        sent_writer.writeBOV(sendbuf)
        received_writer.writeBOV(rcvbuf)
        expected_writer.writeBOV(expected)
        if np.all(rcvbuf == expected):
            print(f'{rank}: index {axisname} comparison succeeded')
        else:
            print(f'{rank}: index {axisname} comparison failed')
        returnbuf = reverse_shuffle_and_swap(comm, rcvbuf, after_layout, before_layout)
        if np.all(returnbuf == sendbuf):
            print(f'{rank}: index {axisname} return comparison succeeded')
        else:
            print(f'{rank}: index {axisname} return comparison failed')
        returned_writer.writeBOV(returnbuf)
        
    # Use a feature in the Layout class that uniquely numbers each cell, and make sure all of the cells
    # end up where expected.  There's no point plotting these because the global addresses don't make
    # much visual sense.
    sendbuf = np.zeros(before_layout.shape, dtype=np.int32)
    sendbuf = before_layout.fill_with_gbl_addr(rank, sendbuf)
    print(f'{rank}: done building global address array')
    rcvbuf = shuffle_and_swap(comm, sendbuf, before_layout, after_layout)
    for_comparison = np.empty(after_layout.shape, dtype=np.int32)
    for_comparison = after_layout.fill_with_gbl_addr(rank, for_comparison)
    if np.all(rcvbuf == for_comparison):
        print(f'{rank}: Global address comparison succeeded')
    else:
        print(f'{rank}: Global address comparison failed :-(')
    returnbuf = reverse_shuffle_and_swap(comm, rcvbuf, after_layout, before_layout)
    if np.all(returnbuf == sendbuf):
        print(f'{rank}: Global address return comparison succeeded')
    else:
        print(f'{rank}: Global address return comparison failed')
    
    
if __name__ == "__main__":
    main()
