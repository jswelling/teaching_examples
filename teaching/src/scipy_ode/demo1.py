#! /usr/bin/env python

"""
This is a variant of generators/demo4 using the SciPy ODE solver facility
"""

import math
import numpy as np
from scipy.integrate import ode

def springForce(x, k, otherX):
    return -k * (x - otherX)

def evolutionEquations(t, y, k):
    x1, v1, x2, v2 = y
    dx1dt = v1
    dv1dt = springForce(x1, k, x2)
    dx2dt = v2
    dv2dt = springForce(x2, k, x1)
    return [dx1dt, dv1dt, dx2dt, dv2dt]

def main():
    x1 = 1.0
    v1 = 0.0
    x2 = -0.5
    v2 = 0.0
    xInitial = [x1, v1, x2, v2]
    t = 0.0
    dt = 0.01
    k = 3.0
    solver = ode(evolutionEquations)
    solver.set_initial_value(xInitial).set_f_params(k).set_integrator('dopri5')

    tRunaway = 5.0
    while solver.successful() and solver.t < tRunaway:
        solver.integrate(solver.t + dt)
        x1, v1, x2, v2 = solver.y
        print '%s: x1 = %s, x2 = %s' % (solver.t, x1, x2)
        if (x1 - x2) < 0.0:
            break
    
if __name__ == "__main__":
    main()
