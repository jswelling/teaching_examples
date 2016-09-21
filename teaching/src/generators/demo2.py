#! /usr/bin/env python

import math

def stepper(forceFun, startTuple, dt):
    x, v, t = startTuple
    while True:
        # RK would go here
        v += forceFun(x) * dt
        x += v * dt
        t += dt
        yield (x, v, t)

def springForce(x):
    return -3.0 * x

def main():
    x = 1.0
    v = 0.0
    t = 0.0
    dt = 0.01
    myGenerator = stepper(springForce, (x, v, t), dt)
    
    while True:
        x, v, t = myGenerator.next()
        print '%s: x = %s, v = %s' % (t, x, v)
        if x < 0.0:
            break
    
if __name__ == "__main__":
    main()
