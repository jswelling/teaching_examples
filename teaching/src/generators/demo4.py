#! /usr/bin/env python

import math

def stepper(forceFun, startTuple, dt, otherX):
    x, v, t = startTuple
    while True:
        # RK would go here
        v += forceFun(x, otherX) * dt
        x += v * dt
        t += dt
        otherX = yield (x, v, t)

def springForce(x, otherX):
    return -3.0 * (x - otherX)

def main():
    x1 = 1.0
    v1 = 0.0
    x2 = -0.5
    v2 = 0.0
    t = 0.0
    dt = 0.01
    p1 = stepper(springForce, (x1, v1, t), dt, x2)
    p2 = stepper(springForce, (x2, v2, t), dt, x1)

    x1, v1, t = p1.send(None)  
    x2, v2, t = p2.send(None)   
    while True:
        print '%s: x1 = %s, x2 = %s' % (t, x1, x2)
        if (x1 - x2) < 0.0:
            break
        x1, v1, t = p1.send(x2)  
        x2, v2, t = p2.send(x1)   
    
if __name__ == "__main__":
    main()
