/*
 * Compile and link with: cc -O3 -msse2 -march=core2 notfibonacci.c
 *
 * For assembly src, compile with: cc -O3 -msse2 -march=core2 -S notfibonacci.c
 */

#include <stdio.h>

#define LEN 14

void trickfun(int len, float* a, float* b, float* c)
{
  while (len--) {
    *a++ = *b++ + *c++;
  }
}

void restrictfun(int len, float* restrict a, float* restrict b, float* restrict c)
{
  while (len--) {
    *a++ = *b++ + *c++;
  }
}


int main()
{
	float a[LEN] __attribute__ ((aligned (16)));
	float b[LEN] __attribute__ ((aligned (16)));
	float c[LEN] __attribute__ ((aligned (16)));
	int len = LEN;

	printf("\n---used as intended---\n");
	for (int i=0; i<LEN; i++) { a[i] = 1; b[i] = 2; c[i] = 3; }
	trickfun(len, a, b, c);
	for (int i=0; i<LEN; i++) {
		printf("%d: %8.0f\n", i, a[i]);
	}

	printf("\n---without restrict---\n");
	a[0] = 1.0; a[1] = 2.0;
	trickfun(len-2, a+2, a, a+1);
	for (int i=0; i<LEN; i++) {
		printf("%d: %8.0f\n", i, a[i]);
	}
  
	printf("\n---with restrict---\n");
	a[0] = 1.0; a[1] = 2.0;
	restrictfun(len-2, a+2, a, a+1);
	for (int i=0; i<LEN; i++) {
		printf("%d: %8.0f\n", i, a[i]);
	}

	return 0;
}
