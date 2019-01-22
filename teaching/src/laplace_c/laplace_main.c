/*************************************************
 * Laplace Serial C Version
 *
 * Temperature is initially 0.0
 * Boundaries are as follows:
 *
 *      0         T         0
 *   0  +-------------------+  0
 *      |                   |
 *      |                   |
 *      |                   |
 *   T  |                   |  T
 *      |                   |
 *      |                   |
 *      |                   |
 *   0  +-------------------+ 100
 *      0         T        100
 *
 *  John Urbanic, PSC 2014
 *
 ************************************************/

#define _BSD_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <sys/time.h>
#include "update.h"

// size of plate
#define COLUMNS    1000
#define ROWS       1000

// largest permitted change in temp (This value takes about 3400 steps)
#define MAX_TEMP_ERROR 0.01

double Temperature[ROWS+2][COLUMNS+2];      // temperature grid
double Temperature_last[ROWS+2][COLUMNS+2]; // temperature grid from last iteration

//   helper routines
void initialize(int rowdim, int coldim, double temp[][coldim]);
void track_progress(int iter);


int main(int argc, char *argv[]) {

  int i, j;                                            // grid indexes
  int max_iterations;                                  // number of iterations
  int iteration=1;                                     // current iteration
  double dt=100;                                       // largest change in t
  struct timeval start_time, stop_time, elapsed_time;  // timers

  printf("Maximum iterations [100-4000]?\n");
  scanf("%d", &max_iterations);

  // Unix timer
  gettimeofday(&start_time,NULL); 

  // initialize Temp_last including boundary conditions
  initialize(ROWS+2, COLUMNS+2, Temperature_last); 

  // do until error is minimal or until max steps
  while ( dt > MAX_TEMP_ERROR && iteration <= max_iterations ) {

    update(ROWS+2, COLUMNS+2, Temperature, Temperature_last);
      
    dt = 0.0; // reset largest temperature change

    // copy grid to old grid for next iteration and find latest dt
    for(i = 1; i <= ROWS; i++){
      for(j = 1; j <= COLUMNS; j++){
	dt = fmax( fabs(Temperature[i][j]-Temperature_last[i][j]), dt);
	Temperature_last[i][j] = Temperature[i][j];
      }
    }

    // periodically print test values
    if((iteration % 100) == 0) {
      track_progress(iteration);
    }

    iteration++;
  }

  gettimeofday(&stop_time,NULL);
  timersub(&stop_time, &start_time, &elapsed_time); // Unix time subtract routine

  printf("\nMax error at iteration %d was %f\n", iteration-1, dt);
  printf("Total time was %f seconds.\n", elapsed_time.tv_sec+elapsed_time.tv_usec/1000000.0);

}


// initialize plate and boundary conditions
// Temp_last is used to to start first iteration
void initialize( int rowdim, int coldim, double temp[][coldim]){

  int i,j;

  for(i = 0; i < rowdim; i++){
    for (j = 0; j < coldim; j++){
      temp[i][j] = 0.0;
    }
  }

  // these boundary conditions never change throughout run

  // set left side to 0 and right to a linear increase
  for(i = 0; i <= ROWS+1; i++) {
    temp[i][0] = 0.0;
    temp[i][coldim - 1] = (100.0/(rowdim - 2))*i;
  }
    
  // set top to 0 and bottom to linear increase
  for(j = 0; j < coldim; j++) {
    temp[0][j] = 0.0;
    temp[rowdim-1][j] = (100.0/(coldim-2))*j;
  }
}


// print diagonal in bottom right corner where most action is
void track_progress(int iteration) {

  int i;

  printf("---------- Iteration number: %d ------------\n", iteration);
  for(i = ROWS-5; i <= ROWS; i++) {
    printf("[%d,%d]: %5.2f  ", i, i, Temperature[i][i]);
  }
  printf("\n");
}
