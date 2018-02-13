#! /usr/bin/env python

'''
Created on Jan 10, 2016

@author: welling
'''

################
# In mat[a,b], a is the row and b is the column.
################

import numpy as np
from writebov import writeBOV
from mpi4py import MPI

totSzTpl = (9, 11)   # (totRows, totCols)

def initialize(xDim, yBlk, yOff):
    """
    yOff gives the offset of this sub-array within the
    global array
    """
    gOld = np.zeros([yBlk, xDim])
    gOld[:, -1] = 1.0
    yTot, xTot = totSzTpl
    if yBlk + yOff == yTot:
        gOld[-1, :] = 1.0
    return gOld


def update(gOld):
    """This is the same update routine as before"""
    gNew = np.empty_like(gOld)
    gNew[1:-1, 1:-1] = 0.25 * (gOld[0:-2, 1:-1] + gOld[2:, 1:-1]
                               + gOld[1:-1, 0:-2] + gOld[1:-1, 2:])
    gNew[0, :] = gOld[0, :]
    gNew[-1, :] = gOld[-1, :]
    gNew[:, 0] = gOld[:, 0]
    gNew[:, -1] = gOld[:, -1]
    return gNew

def sendGhosts(gFull, ghostLow, ghostHigh, rank, comm):
    if ghostLow:
        # Use Isend to send the rank one below ours the
        # row it needs.  Keep the request object.
        theirGhostRowIdx = 1
        lowReq = None  # FIX ME
    else:
        # There is no rank one below ours
        lowReq = None
    if ghostHigh:
        # Use Isend to send the rank one above ours the
        # row it needs.  Keep the request object.
        theirGhostRowIdx = -2
        highReq = None  # FIX ME
    else:
        highReq = None
    # Return both request objects
    return lowReq, highReq

def recvGhosts(gFull, ghostLow, ghostHigh, rank, comm):
    if ghostLow:
        # Use Irecv to accept the ghost row sent from the
        # rank below ours. It's OK to immediately wait on
        # the request object.
        myGhostRowIdx = 0
        pass  # FIX ME
    if ghostHigh:
        # Use Irecv to accept the ghost row sent from the
        # rank above ours.  It's OK to immediately wait on
        # the request object.
        myGhostRowIdx = -1
        pass  # FIX ME

def waitGhosts(ghostLow, ghostHigh, lowReq, highReq):
    if ghostLow:
        # Wait for the low send to complete
        pass  # FIX ME
    if ghostHigh:
        # Wait for the high send to complete
        pass  # FIX ME

def printEverythingInOrder(gFull, rank, size, comm, ghostLow, ghostHigh):
    """This is a Python version of the printing loop we saw in C"""
    for i in range(size):
        comm.Barrier()
        if i == rank:
            print 'rank %s: %s %s' % (rank, ghostLow, ghostHigh)
            print gFull

def collectFullLiveArray(gFull, rank, size, comm, yBlk, ghostLow, ghostHigh):
    yTot, xTot = totSzTpl
    offset = 1 if ghostLow else 0
    myTag = 3
    if rank == 0:
        reqList = []
        # Allocate the full array size and copy in our bit.
        gAll = np.zeros(totSzTpl)
        gAll[0:yBlk,:] = gFull[offset:offset+yBlk,:]
        for otherRank in range(1, size):
            # Calculate where the incoming block goes and how many
            # rows it contains
            otherYBlk = (yTot - otherRank*yBlk if otherRank == size-1
                         else yBlk)
            otherOffset = otherRank*yBlk
            # Use Irecv to accept the incoming block, storing it in
            # the correct place in gAll.  Save the request in reqList.
            req = None  # FIX ME
            reqList.append(req)
        # Wait on all the requests in reqList.
        for req in reqList:
            pass  # FIX ME
    else:
        # Send this rank's block to rank 0.
        pass  # FIX ME
        gAll = None
        
    return gAll

def main():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    yTot, xTot = totSzTpl
    yBlk = yTot/size
    yOff = rank * yBlk
    if rank == size - 1:
        yBlk = yTot - yOff

    gLive = initialize(xTot, yBlk, yOff)
    ghostLow = (yOff != 0)
    ghostHigh = (yOff + yBlk != yTot)

    if ghostLow:
        if ghostHigh:
            gFull = np.zeros([yBlk+2, xTot])
            gFull[1:-1,:] = gLive
        else:
            gFull = np.zeros([yBlk+1, xTot])
            gFull[1:, :] = gLive
    else:
        if ghostHigh:
            gFull = np.zeros([yBlk+1, xTot])
            gFull[:-1, :] = gLive
        else:
            gFull = np.zeros([yBlk, xTot])
            gFull[:,:] = gLive
            
    printEverythingInOrder(gFull, rank, size, comm,
                           ghostLow, ghostHigh)
    comm.Barrier()
    gAll = collectFullLiveArray(gFull, rank, size, comm, yBlk,
                                ghostLow, ghostHigh)
    if rank == 0:
        writeBOV(gAll)
    comm.Barrier()

    # writeBOV(collectFullLiveArray(gFull, rank, size, comm,
    #                               yBlk, ghostLow, ghostHigh))

    for n in xrange(20000):  # @UnusedVariable
        lowReq, highReq = sendGhosts(gFull, ghostLow, ghostHigh, rank, comm)
        recvGhosts(gFull, ghostLow, ghostHigh, rank, comm)
        waitGhosts(ghostLow, ghostHigh, lowReq, highReq)
        gFull = update(gFull)

    printEverythingInOrder(gFull, rank, size, comm,
                           ghostLow, ghostHigh)

if __name__ == '__main__':
    main()
