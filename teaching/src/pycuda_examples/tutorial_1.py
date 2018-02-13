# This example is from https://documen.tician.de/pycuda/tutorial.html

import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

import numpy
a = numpy.random.randn(4,4)  # create some data

a = a.astype(numpy.float32)  # convert to 32 because most GPUs have no doubles

a_gpu = cuda.mem_alloc(a.nbytes)  # Alloc device space

cuda.memcpy_htod(a_gpu, a)  # push data to device

# This is actual cuda code to compile and apply
mod = SourceModule("""
  __global__ void doublify(float *a)
  {
    int idx = threadIdx.x + threadIdx.y*4;
    a[idx] *= 2;
  }
  """)

func = mod.get_function("doublify")  # Get our function by name...
func(a_gpu, block=(4,4,1))           # ...and apply it to a_gpu

a_doubled = numpy.empty_like(a)  # make space on host for the result
cuda.memcpy_dtoh(a_doubled, a_gpu)  # pull the data back
print a_doubled  # and print
print a


