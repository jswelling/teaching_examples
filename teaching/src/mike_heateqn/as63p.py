#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
This is a Python implementation of the AS63 code.

Good things to google:
  -try 'matplotlib 3d' and specifically http://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#surface-plots
   for information on the 3d surface plot.
  -try 'matplotlib imshow' and specifically http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.imshow
   for information on the function that draws a matrix as an image.
  -There are several ways to do animation in matplotlib.  Google 'matplotlib animation' for examples.  This
   code is a synthesis of several examples; I'm afraid I can't find a reference that looks quite like it.
  -Google 'numpy fortran to python' for information on using ftopy.  The best specific page is 
   https://docs.scipy.org/doc/numpy-1.10.0/user/c-info.python-as-glue.html
"""


XDIM = 20
YDIM = 30

def initialize(xDim, yDim):
    gMat = np.zeros([xDim, yDim])
#    gMat[-1, :] = 1.0  #MJL: edge values=0-0-0-1
    gMat[:,0] = 1.0
    return gMat


def update(gMat):  #MJL: do one time step + 5 relaxations
    """Do one update, including 5 sweeps"""
    xDim, yDim = gMat.shape
    c1 = 0.025
    c2=1. + (4*c1)         #the time step per update =0.5574 s with c1=0.025
    gNew = np.empty_like(gMat)
    gNew[:]=gMat[:]
    
    for _ in range (0, 5):               # 5 iterations of sweep
        for i in range (1,xDim-1):       # sweep x excluding 1st & last
            for j in range (1,yDim-1):   # sweep y excluding 1st & last
                gNew[i,j]= (gMat[i,j]+c1*(gNew[i+1,j]+gNew[i-1,j]+gNew[i,j+1]+gNew[i,j-1]))/c2
                
    # Why not use this much more concise version?  How could you fix it?
#     for _ in range(0, 5):
#         gNew[1:-1, 1:-1] = gMat[1:-1, 1:-1] + c1*(gNew[2:, 1:-1] + gNew[0:-2, 1:-1]
#                                                   + gNew[1:-1, 2:] + gNew[1:-1, 0:-2])/c2
    
    return gNew


def buildPlot(gMat):
    fig = plt.figure(figsize=(16,4))
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122)
    X = np.arange(0, YDIM)
    Y = np.arange(0, XDIM)
    X, Y = np.meshgrid(X, Y)
    surf = ax1.plot_surface(X, Y, gMat, rstride=1, cstride=1,
                            cmap=plt.cm.coolwarm,
                            linewidth=0, antialiased=False)
    ax1.set_zlim(-0.5, 1.5)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax1.zaxis.set_major_locator(plt.LinearLocator(10))
    ax1.zaxis.set_major_formatter(plt.FormatStrFormatter('%.02f'))

    imgObj = ax2.imshow(gMat, vmin=0.0, vmax=1.0)
    return fig, ax1, ax2, X, Y, surf, imgObj
        
def animate(frameNum, gMat, ax1, X, Y, surf, imgObj):
    # print frameNum
    surf.remove()
    surf= ax1.plot_surface(X, Y, gMat, rstride=1, cstride=1,
                           cmap=plt.cm.coolwarm,
                           linewidth=0, antialiased=False)
    imgObj.set_data(gMat)
    plt.pause(0.001)  # Give up the thread so the UI can catch up
    return [surf, imgObj]

def main():
    gMat = initialize(XDIM, YDIM)
    fig, ax1, ax2, X, Y, surf, imgObj = buildPlot(gMat)
    
    frameNum = 0
    while True:
        surf, imgObj = animate(frameNum, gMat, ax1, X, Y, surf, imgObj)
        gMat = update(gMat)
        ignored = raw_input('%d > ' % frameNum)
        frameNum += 1
    
    plt.show()

if __name__ == "__main__":
    main()

