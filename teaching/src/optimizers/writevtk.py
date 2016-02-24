#! /usr/bin/env python

'''
Created on Jan 10, 2016

@author: welling
'''

import types

counter = 0


def writeCurve3D(label, tripleList, attrListList=None):
    global counter
    fname = 'curve3d_%03d.vtk' % counter
    counter += 1
    with open(fname, 'w') as f:
        f.write("# vtk DataFile Version 2.0\n")
        f.write("Output of three_d.py\n")
        f.write("ASCII\n")
        f.write("DATASET UNSTRUCTURED_GRID\n")
        f.write("POINTS %d float\n" % len(tripleList))
        for x, y, z in tripleList:
            f.write("%f %f %f\n" % (x, y, z))
        f.write("\n")
        f.write("CELLS 1 %d\n" % (len(tripleList) + 1))
        f.write("%d\n" % len(tripleList))
        for i in xrange(len(tripleList)):
            f.write("%d\n" % i)
        f.write("\n")
        f.write("CELL_TYPES 1\n")
        f.write("4\n")
        f.write("\n")
        if attrListList is None:
            attrListList = [('sample', range(len(tripleList)))]
        if len(attrListList) > 0:
            f.write("POINT_DATA %d\n" % len(tripleList))
        for name, attrList in attrListList:
            delta = len(attrList) - len(tripleList)
            if delta > 0:
                attrList = attrList[0:len(tripleList)]  # throw out extra values
            elif delta < 0:
                attrList = attrList + (-1*delta)*[None]  # pad with none
            if isinstance(attrList[0], types.TupleType):
                f.write("VECTORS %s float\n" % name)
                for t in attrList:
                    if t is None:
                        f.write("0.0 0.0 0.0\n")
                    else:
                        f.write("%f %f %f\n" % t)
                f.write("\n")
            else:
                f.write("SCALARS %s float 1\n" % name)
                f.write("LOOKUP_TABLE default\n")
                for v in attrList:
                    if v is None:
                        f.write("0.0\n")
                    else:
                        f.write("%f\n" % v)
                f.write("\n")

