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

```python
if __name__ == "__main__":
    print(main())
```

the easiest way to run the example is from the terminal.

Within your command line / terminal, navigate to the folder containing the main.py script, and just run:

```bash
python3 main.py
```

^ Note that this homework actually uses python3 not python2 as I normally do.

A numpy array should output:

```python
[ 4.5454547   0.90909092  3.63636377  1.81818181  2.72727287  2.72727279
  1.81818181  3.63636365  0.90909089  4.54545454]
```
