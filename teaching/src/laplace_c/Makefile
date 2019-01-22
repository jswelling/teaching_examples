CFLAGS = -g -std=c99
LIBS = -lm

laplace: laplace_main.o update.o
	$(CC) -o $@ $& laplace_main.o update.o $(LIBS)

laplace_main.o: laplace_main.c update.h

update.o: update.c update.h

clean:
	rm *.o

