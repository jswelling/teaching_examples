#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from writebov import writeBOV

# max values for NX and NY
MAXX = 128
MAXY = 128

# Horiz and vert number of lattice points, and total number of spins
NX = 128
NY = 128
NSPIN = NX*NY

# Number of thermalization sweeps
#NTHERM = 3
NTHERM = 400

# Freq of sweeps to avoid correlations
NFREQ = 100
#NFREQ = 1

# Number of entries in averages (each entry separated by NFREQ sweeps)
#NSIZE = 1000
NSIZE = 100


def checkerboard(shape):
    """
    Thank you stackoverflow!
    """
    return np.indices(shape).sum(axis=0) % 2


def make_random_spin_array():
    rand_vals = np.random.rand(NX, NY)
    ones = np.ones((NX, NY), dtype=int)
    rslt = np.choose(rand_vals >= 0.5,
                     [-ones, ones])
    return rslt

class MetropolisRatio:
    def __init__(self):
        self.array = np.zeros((3,9))
    def set(self, nbr_sum, this_spin, value):
        self.array[this_spin+1, nbr_sum+4] = value
    def get(self, nbr_sum, this_spin):
        return self.array[this_spin+1, nbr_sum+4]
    def dump(self):
        print(self.array)


def count_neighbors_and_pick_flips(spins, ratios):
    """
    Returns a boolean array which is true for spins that would flip,
    over the entire array (not just the red or black squares)
    """
    nbr_counts = (np.roll(spins, 1, 0)
                  + np.roll(spins, -1, 0)
                  + np.roll(spins, 1, 1)
                  + np.roll(spins, -1, 1)
    )
    flip_probs = ratios.get(nbr_counts, spins)
    #
    # Decide whether or not to flip each spin.  We don't need to worry
    # about the checkerboard business here; that is taken care of in
    # 'metrop' below.  We just need to make a boolean value for each
    # grid location, True if the spin is to flip.
    #
    does_this_spin_flip = ???  # SOME FORMULA GOES HERE
    return does_this_spin_flip


def metrop( spins, ratios, checkerboards):
    """
    Updates the spins based on the given ratios.  Returns
    the updated spins and the fraction of spins that were updated.
    """
    checkerboard_red, checkerboard_black = checkerboards

    # For the 'red' squares first, flip appropriate spins
    does_this_spin_flip = count_neighbors_and_pick_flips(spins, ratios)
    does_this_spin_flip = np.logical_and(does_this_spin_flip,
                                         checkerboard_red)
    num_flips = np.count_nonzero(does_this_spin_flip)
    spins = np.choose(does_this_spin_flip, [spins, -spins])

    # Now do the 'black' squares
    does_this_spin_flip = count_neighbors_and_pick_flips(spins, ratios)
    does_this_spin_flip = np.logical_and(does_this_spin_flip,
                                         checkerboard_black)
    num_flips += np.count_nonzero(does_this_spin_flip)
    spins = np.choose(does_this_spin_flip, [spins, -spins])

    return spins, num_flips/NSPIN

        
def measure(spins, b, j):
    """
    Given the spin matrix and the current values of b and j,
    returns magnetization and total system energy, in that order
    """
    # This way of calculating the number of pairs takes care to count
    # each pair only once.
    pairs = np.sum(spins * (np.roll(spins, -1, 0) + np.roll(spins, -1, 1)))
    magsweep = np.sum(spins) / NSPIN
    esweep = (????) / NSPIN  # SOME FORMULA GOES HERE
    
    return magsweep, esweep


def main():
    b = 0.0  # magnetic field strength
    j = 0.5  # critical value is 0.4406868
    accept = 0.0  # acceptance ratio
    isweep = 0  # sweep index
    energy = 0.0  # total system energy
    mag = 0.0  # magnetization

    ratios = MetropolisRatio()
    for nnbrloop in range(-4, 5, 2):   # -4, -2, 0, 2, 4
        ratios.set(nnbrloop, -1, ????)  # SOME FORMULA GOES HERE
        ratios.set(nnbrloop, 1, ????)  # SOME FORMULA GOES HERE
    ratios.dump()
    
    spins = make_random_spin_array()
    #print('initial state:')
    #print(spins)

    checkerboard_red = checkerboard(spins.shape)
    #print('checkerboard_red')
    #print(checkerboard_red)
    checkerboard_black = 1 - checkerboard_red
    #print('checkerboard_black')
    #print(checkerboard_black)
    checkerboards = (checkerboard_red, checkerboard_black)    
    
    # Thermalize initial config
    for itherm in range(NTHERM):
        spins, accept = metrop(spins, ratios, checkerboards=checkerboards)
        print(f'Thermalization sweep {itherm}, acceptance ratio = {accept}')
        #print(spins)

    energy = 0.0  # running total of energy
    mag = 0.0  # running total of magnetization
    nmeasure = 0  # how many measurements have been made
    for iter in range(NFREQ*NSIZE):
        spins, accept = metrop(spins, ratios, checkerboards=checkerboards)
        #print(accept)
        #print(spins)
        if (iter % NFREQ == 0):
            magsweep, esweep = measure(spins, b, j)
            mag += np.abs(magsweep)
            energy += esweep
            nmeasure += 1
            print(f'     Measurement number={nmeasure}, energy={esweep}, '
                  f'magnetization={magsweep}')
            #writeBOV(spins)

    energy /= nmeasure
    mag /= nmeasure
    print(f'\n\n     Measurements={nmeasure}, average energy={energy}, '
          f'average magnetization={mag} at j={j}, b={b}')

if __name__ == "__main__":
    main()

