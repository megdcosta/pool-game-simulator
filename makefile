CC = clang
CFLAGS = -Wall -pedantic -std=c99
PY_VER = python3.11
SWIG_TOOL = swig

all: a4

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

libphylib.so: phylib.o
	$(CC) -shared $< -lm -o $@

phylib_wrap.c phylib.py: phylib.i
	$(SWIG_TOOL) -python phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c $< -I/usr/include/$(PY_VER)/ -fPIC -o $@

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) -shared $< -L. -L/usr/lib/$(PY_VER) -l$(PY_VER) -lphylib -o $@

a4: libphylib.so _phylib.so 

clean:
	rm -f *.o *.so phylib_wrap.c phylib.py *.svg a4 phylib.db
