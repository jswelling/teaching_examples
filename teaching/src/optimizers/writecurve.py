#! /usr/bin/env python

'''
Created on Jan 10, 2016

@author: welling
'''

counter = 0


def writeCurve(label, pairList):
    global counter
    fname = 'curve_%03d.curve' % counter
    counter += 1
    with open(fname, 'w') as f:
        f.write('#%s\n' % label)
        for x, y in pairList:
            f.write('%f %f\n' % (x, y))
