#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def initialize(xDim, yDim):
    gMat = np.zeros([xDim, yDim])
    gMat[-1, :] = 1.0
    gMat[:, -1] = 1.0
    return gMat

def update(gMat):
    gNew = np.empty_like(gMat)
    gNew[1:-1, 1:-1] = 0.25 * (gMat[0:-2, 1:-1] + gMat[2:, 1:-1]
                               + gMat[1:-1, 0:-2] + gMat[1:-1, 2:])
    gNew[0, :] = gMat[0, :]
    gNew[-1, :] = gMat[-1, :]
    gNew[:, 0] = gMat[:, 0]
    gNew[:, -1] = gMat[:, -1]
    return gNew

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
    
gMat = initialize(90, 110)
fig, ax1, ax2, X, Y, surf, imgObj = buildPlot()

frameNum = 0
while True:
    surf, imgObj = animate(frameNum, gMat, ax1, X, Y, surf, imgObj)
    gMat = update(gMat)
    ignored = raw_input('%d > ' % frameNum)
    frameNum += 1

plt.show()
