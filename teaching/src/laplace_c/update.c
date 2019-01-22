#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#include "update.h"

void update(int rowdim, int coldim,
	    double temp[][coldim], double temp_last[][coldim]) {
  int i;
  int j;
    
  // main calculation: average my four neighbors
  for(i = 1; i < rowdim-1; i++) {
    for(j = 1; j < coldim-1; j++) {
      temp[i][j] = 0.25 * (temp_last[i+1][j]
			   + temp_last[i-1][j]
			   + temp_last[i][j+1]
			   + temp_last[i][j-1]);
    }
  }
}


