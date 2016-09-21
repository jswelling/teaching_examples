#! /usr/bin/env python

import math

def stepper(forceFun, startTuple, dt):
    x, v, t = startTuple
    while True:
        print 'generator: dt = %s' % dt
        # RK would go here
        v += forceFun(x) * dt
        x += v * dt
        t += dt
        dt = yield (x, v, t)

def springForce(x):
    return -3.0 * x

def main():
    x = 1.0
    v = 0.0
    t = 0.0
    dt = 0.01
    myGenerator = stepper(springForce, (x, v, t), dt)

    x, v, t = myGenerator.send(None)    
    while True:
        print '%s: x = %s, v = %s' % (t, x, v)
        if x < 0.0:
            break
        x, v, t = myGenerator.send(math.fabs(0.01/v))
    
if __name__ == "__main__":
    main()
