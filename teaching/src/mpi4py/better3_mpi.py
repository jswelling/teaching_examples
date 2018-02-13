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
    gOld = np.zeros([yBlk, xDim])
    gOld[:, -1] = 1.0
    yTot, xTot = totSzTpl
    if yBlk + yOff == yTot:
        gOld[-1, :] = 1.0
    return gOld


def update(gOld):
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
        lowReq = comm.Isend(gFull[1,:], rank-1, 7)
    else:
        lowReq = None
    if ghostHigh:
        highReq = comm.Isend(gFull[-2,:], rank+1, 8)
    else:
        highReq = None
    return lowReq, highReq

def recvGhosts(gFull, ghostLow, ghostHigh, rank, comm):
    if ghostLow:
        lowRcvReq = comm.Irecv(gFull[0,:],rank-1, 8)
        lowRcvReq.Wait()
    if ghostHigh:
        highRcvReq = comm.Irecv(gFull[-1,:], rank+1, 7)
        highRcvReq.Wait()

def waitGhosts(ghostLow, ghostHigh, lowReq, highReq):
    if ghostLow:
        lowReq.Wait()
    if ghostHigh:
        highReq.Wait()

def printEverythingInOrder(gFull, rank, size, comm, ghostLow, ghostHigh):
    for i in range(size):
        comm.Barrier()
        if i == rank:
            print 'rank %s: %s %s' % (rank, ghostLow, ghostHigh)
            print gFull

def collectFullLiveArray(gFull, rank, size, comm, yBlk, ghostLow, ghostHigh):
    yTot, xTot = totSzTpl
    offset = 1 if ghostLow else 0
    if rank == 0:
        reqList = []
        gAll = np.zeros(totSzTpl)
        gAll[0:yBlk,:] = gFull[offset:offset+yBlk,:]
        for otherRank in range(1, size):
            otherYBlk = (yTot - otherRank*yBlk if otherRank == size-1
                         else yBlk)
            otherOffset = otherRank*yBlk
            req = comm.Irecv(gAll[otherOffset:otherOffset+otherYBlk,:],
                             otherRank, 3)
            reqList.append(req)
        for req in reqList:
            req.Wait()
    else:
        req = comm.Isend(gFull[offset:offset+yBlk,:], 0, 3)
        req.Wait()
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

    for i in range(size):
        comm.Barrier()
        if i == rank:
            print rank, yBlk, yOff, yTot, ghostLow, ghostHigh
            print gFull

if __name__ == '__main__':
    main()
