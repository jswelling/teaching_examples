#! /usr/bin/env python
import sys
import os
import math
import random
import matplotlib.pyplot as plt

mutatorSigma= 0.5
initialX= 30.0
#burnInCount= 10000
burnInCount= 0
trialCount= 50000
acceptCount= 0

histoBins= 256
histo= {}

def addToHisto(x):
    scaledX= 0.005*(x+100.0)
    bin= int(round((histoBins-1)*scaledX))
    if bin<0:
        bin= 0
    if bin>=histoBins:
        bin= histoBins-1
    histo[bin] += 1

def histoBinLoc(i):
    return (float(i)/float(histoBins-1))*200.0 - 100.0

def func(x):
  return (1.0-math.cos(x))/(x*x)

def integrand(x):
    return (1.0+math.cos(x))

def mutate(oldX,oldF):
    global R
    global acceptCount
    newX= oldX+R.gauss(0.0,mutatorSigma)
    newF= func(newX)
    if newF>=oldF:
        acceptCount += 1
        return (newX,newF)
    else:
        ratio= math.fabs(newF/oldF)
        if R.random()<ratio:
            acceptCount += 1
            return (newX,newF)
        else:
            return (x,oldF)

frame_num=0
def makeFrame(num,scale):
    global histo
    global frame_num
    counts = [histo[i] for i in range(histoBins)]
    locs = [histoBinLoc(i) for i in range(histoBins)]
    
    plt.figure()
    plt.bar(locs, counts)
    plt.savefig('frame_%04d.png'%frame_num)
    plt.close()
    frame_num += 1
    print("wrote frame %d"%num)

##########
# Main
##########

R= random.Random()

for i in range(0,histoBins):
    histo[i]= 0

# burn-in
x= initialX
f= func(x)
fMax= f
for i in range(0,burnInCount):
    (x,f)= mutate(x,f)
    if f>fMax: fMax= f

# trials
acceptCount= 0
sum= 0.0
for i in range(0,trialCount):
    addToHisto(x)
    sum += integrand(x)
    if i%100 == 0: makeFrame(i/100,1.0/float(i+1))
    (x,f)= mutate(x,f)

print("%d trials, %d accepted: %f"%(trialCount,acceptCount,sum/trialCount))

