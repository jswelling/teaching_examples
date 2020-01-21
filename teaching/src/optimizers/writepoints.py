#! /usr/bin/env python

'''
Created on Jan 10, 2016

@author: welling
'''

counter = 0


def writePoints(label, quadList):
    global counter
    fname = 'points_%03d.point3d' % counter
    counter += 1
    with open(fname, 'w') as f:
        f.write('x y z %s\n' % label)
        for x, y, z, v in quadList:
            f.write('%g %g %g %g\n' % (x, y, z, v))
