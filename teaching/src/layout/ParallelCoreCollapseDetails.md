# Final Project Details - Parallelize Your Core Collapse Code #

This is a project for two people, at least one of which should have a good solution to last semester's final project handy.  You'll need to coordinate with your partner.  Maybe a private github repo?

## Stage 1 - getting the framework right ##
1. Turn your ipython notebook into a python program.
2. Set up global communication to coorindate the ranks.  I've found an MPI bcast to distribute a dict to all ranks works well for this; rank 0 can make decisions and then share them with the other ranks.
3. Restructure your coordinates and grid to form slabs in the Y-Z plane.  You can keep the corners of the _global_ grid at the same spatial coordinates, which means that each _local_ grid will have the same corner coordinates for Y and Z but different spatial coordinates for X.  I would suggest keeping the individual grid cells cubic, which means changing each individual grid from 128x128x128 to something more slab-like.
4. Connect your time step calculation to pick a _global_ time step
5. I will supply a parallel version of writebov, which each rank will have to call individually in a coordinated way.

## Stage 2 - particle transport (can be in parallel with stage 3) ##
Particles have to move smoothly from rank to rank when they cross the Z values which form the thresholds to other ranks.  Obviously the number of particles in any given rank can change; you'll have to adjust the size of your coordinate table (or keep a counter to limit the part of the table which you use).  Each rank could use an algorithm something like this to figure out which particles to send where:
1. Sort your particles according to their Z coordinates.  That will put particles with the same destination rank next to each other.
2. Count particles going to each rank and the offsets into the coordinate array that bound each group.
3. Use an MPI alltoall to exchange information, so that each rank knows how many particles to expect from each.
4. Use a series of MPI isend and irecv calls to exchange the particles, now that each rank knows how many particles to expect from each.

To test, just create a cloud of particles with random velocities and watch as they move across the boundaries.  It's OK if the particles just stop when they reach the outer boundary of the global grid, since this is just a test.

Remember to modify your particle-onto-grid code and your gravity-force-to-particle code to use the Nearest Grid Point method rather than the Cloud In Cell method.  The CIC method would require you to use ghost zones when gridding and calculating forces, which is a little too much work for this assignment.

## Stage 3 - parallel FFT (can be in parallel with stage 2) ##

To do the 3D FFT needed to calculate the gravitational potential, the algorithm needs to:
1) Perform a 2D FFT in the Y-Z plane.  In the slab configuration each rank holds the whole grid in that plane, so the 2D FFT can be performed simply.
2) Shuffle the data between ranks so that each rank holds a pencil of data in the X direction.  (Perhaps a better way to think of this as shuffling the ranks while holding all the data fixed in space!)
3) Perform a 1D FFT in the X direction.
4) Undo step (2) by performing the inverse of that first shuffle.

The mpi4py-fft module, available via pip, should be able to handle these shuffles.  

![Slab and pencil layouts](slab_to_pencil.png)

## Stage 4 - run the whole thing together! ##

Now it is time to generate a spherical cloud of points and run the simulation.  Remember that the sphere is global, so only a fraction of the sphere (perhaps none of it!) will exist in the grid space of any specific rank.  A few possible ways to get the initial sphere of well-sampled points would be:
* Have each rank calculate the fraction of the sphere it contains, and generate that fraction of the total random points.
* Have each rank calculate the same fraction of the total points, distributed on a sphere in the global grid space.  Then immediately use your particle exchange algorithm to send every point to its correct rank.
* Have one rank calculate all the points, and then distribute each to the rank where it belongs.

Efficiency isn't too important here, since it only happens once, but don't be embarrassingly inefficient.

Once all the points are created, you should be able to just run the simulation!
