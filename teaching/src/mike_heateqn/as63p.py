#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def initialize(xDim, yDim):
    gMat = np.zeros([xDim, yDim])
#    gMat[-1, :] = 1.0  #MJL: edge values=0-0-0-1
    gMat[:,0] = 1.0
    return gMat

#def update(gMat):
#    gNew = np.empty_like(gMat)
#    gNew[1:-1, 1:-1] = 0.25 * (gMat[0:-2, 1:-1] + gMat[2:, 1:-1]
#                               + gMat[1:-1, 0:-2] + gMat[1:-1, 2:])
#    gNew[0, :] = gMat[0, :]
#    gNew[-1, :] = gMat[-1, :]
#    gNew[:, 0] = gMat[:, 0]
#    gNew[:, -1] = gMat[:, -1]
#    return gNew

def update(gMat):  #MJL: do one time step + 5 relaxations; ??indices probably bad below.
    c1=0.025 ; c2=1.+4/*c1          #the time step per update =0.5574 s with c1=0.025
    gNew = np.empty_like(gMat)
    gNew[:]=gMat[:]
    for k in range (0,5)            #??want 5 iterations of sweep
      for i in range (1,xDim-1)     #??want to sweep x excluding 1st & last
        for j in range (1,yDim-1)   #??want to sweep y excluding 1st & last
          gNew[i,j]=(gMat[i,j]+c1*(qNew[i+1,j]+qNew[i-1,j]+qNew[i,j+1]+qNew[i,j-1]))/c2
    return gNew

# Joel, this is the Fortran version.
#! b(0:40,0:40) is input array (at time=t) and the output array (at time=t+dt). dt=0.5574s (see AS62fx).
#    a=b                 !update "old" array using E1, above
#! Relaxation steps for 'solving' (E2)
#    do k=1,5                        !relaxation steps
#! the relaxation sweeps over the array. They do not allow vector notation. const=0.025
#      do i=1,19; do j=1,19          !sweep over arrays using E2, above
#        b(i,j)=(a(i,j)+const*(b(i+1,j)+b(i-1,j)+b(i,j+1)+b(i,j-1)))/(1.+4.*const)
#      enddo; enddo
#    enddo  !(k loop)

def buildPlot():
    fig = plt.figure(figsize=(16,4))
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122)
    X = np.arange(0, 110)
    Y = np.arange(0, 90)
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
    
#gMat = initialize(90, 110)  #MJL
gMat = initialize(40, 40)    #MJL array[0:40,0:40] ???
fig, ax1, ax2, X, Y, surf, imgObj = buildPlot()

frameNum = 0
while True:
    surf, imgObj = animate(frameNum, gMat, ax1, X, Y, surf, imgObj)
    gMat = update(gMat)
    ignored = raw_input('%d > ' % frameNum)
    frameNum += 1

plt.show()

