#! /usr/bin/env python
import sys
import os
import math
import random
import getopt

# Most of the defaults are set here
debug= 0
sampCount= 1000
mu= 0.0
sigma= 10.0
nTrials= 5

# vExpected is the integral from x=-infinity to infinity of func
vExpected= math.pi
def func(x):
    return (1.0-math.cos(x))/(x*x)

def gausscurve(x,mu,sigma):
    expterm= -((x-mu)*(x-mu))/(2.0*sigma*sigma)
    return (1.0/(sigma*math.sqrt(2.0*math.pi)))*math.exp(expterm)

def boxcarcurve(x,mu,sigma):
    if x>=mu-sigma and x<=mu+sigma:
        return 1.0/(2.0*sigma)
    else:
        return 0;

def normalSamp(mu,sigma):
    x= random.gauss(mu,sigma)
    v= func(x)/gausscurve(x,mu,sigma)
    if debug:
        print "x= %g -> func= %g, gauss= %g -> samp= %g"%\
            (x, func(x), gausscurve(x,mu,sigma), v)
    return v

def boxcarSamp(mu,sigma):
    x= random.uniform(mu-sigma,mu+sigma)
    v= func(x)/boxcarcurve(x,mu,sigma)
    if debug:
        print "x= %g -> func= %g, pdf= %g -> samp= %g"%\
            (x, func(x), boxcarcurve(x,mu,sigma), v)
    return v

def runTrial(sampleFunc):
    sum= 0.0
    for i in xrange(0,sampCount):
        sum += sampleFunc(mu,sigma)
    v= sum/sampCount
    print v
    return v

def describeSelf():
    print """
usage: %s [-d] [--pdf boxcar|gaussian] [--samples nSamples] [--trials nTrials]

-d produces debugging output, listing every sample
You'll need to edit the file to change the shapes of the PDFs.
"""

##########
# Main
##########

try:
    (opts,pargs) = getopt.getopt(sys.argv[1:],"d",
                                 ["pdf=","samples=","trials=","sigma="])
except:
    print "%s: Invalid command line parameter" % sys.argv[0]
    describeSelf();
    sys.exit()

sampleFunc= normalSamp
sampleTypeName= "gaussian"
for a,b in opts:
    if a=="-d":
        debug= 1
    if a=="--samples":
        sampCount= int(b)
    if a=="--trials":
        nTrials= int(b)
    if a=="--pdf":
        if b=="boxcar":
            sampleFunc= boxcarSamp
            sampleTypeName= "boxcar"
        elif b=="gaussian":
            sampleFunc== normalSamp
            sampleTypeName= "gaussian"
        else:
            sys.exit("Invalid pdf string")
    if a=="--sigma":
        sigma= float(b)


print "%s pdf with mu= %g, sigma= %g, %d trials of %d samples"%\
    (sampleTypeName,mu,sigma,nTrials,sampCount)
resultList= []
for i in xrange(nTrials):
    v= runTrial(sampleFunc)
    resultList.append(v)

meanSum= 0.0
for v in resultList:
    meanSum += v
mean= meanSum/nTrials

varSum= 0.0
for v in resultList:
    varSum += (v-mean)*(v-mean)

variance= varSum/(nTrials-1)
print "%d MonteCarlo trials gives %g stdv %g vs. expected value %g"%\
    (nTrials,mean,math.sqrt(variance),vExpected)

