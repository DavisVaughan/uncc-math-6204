'''
### Description

This README is intended to guide the user in how to use HW-09.

The assignment is hosted on github here:

https://github.com/DavisVaughan/uncc-math-6204/tree/master/assignments/hw-09

### General

* Author   - Davis Vaughan
* Date     - 11/17/2017
* Homework - 09

### Purpose

The purpose of this HW is to calculate the solution to a linear system Ax = b
using the SOR algorithm where A is a tridiagonal matrix.

### Thoughts on numerical accuracy

Thomas algorithm is definitely faster than SOR. When you increase the size of the A matrix,
the SOR algo get's pretty slow. Using Cython helps this a lot though, and significantly reduces
the time required.

### Numerical methods used

The SOR algo is used, and is a more general purpose solver than Thomas.
See the documentation of the sor_solver function for a description of the algo.

### Included files

`main.py` - (DRIVER) SOR algorithm example.

`SOR.py` - Contains functions that solve the system using the SOR algo.

`SOR2.py` - Contains functions that solve the system using the SOR algo using Cython for speed.

### How to run

Because the main.py file includes the code:


if __name__ == "__main__":
    print(main())


the easiest way to run the example is from the terminal.

Within your command line / terminal, navigate to the folder containing the main.py script, and just run:

python3 main.py

^ Note that this homework actually uses python3 not python2 as I normally do.

A numpy array should output:

[ 4.5454547   0.90909092  3.63636377  1.81818181  2.72727287  2.72727279
  1.81818181  3.63636365  0.90909089  4.54545454]

'''

import numpy as np
from scipy.sparse import spdiags
from SOR import sor_solver

def main():

    size = 10

    # Set up to create A
    main_diag = 2 * np.ones(size)
    sub_diag  = np.ones(size)
    sup_diag  = np.ones(size)
    A_data = np.array([main_diag, sub_diag, sup_diag])
    tri_set = np.array([0, -1, 1])

    # Create A and b
    A = spdiags(A_data, tri_set, size, size).toarray()
    b = 10 * np.ones(size)

    # Solve the system
    # After a bit of testing, 1.6 seems to be the fastest relaxation parameter in terms
    # of convergence
    x = sor_solver(A, b, relax_param = 1.6, tol = 1e-6)

    return x


if __name__ == "__main__":
    print(main())