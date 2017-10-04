### Description

This README is intended to guide the user in how to use HW-04.

The README is written in Markdown, and is much easier to read on GitHub:

https://github.com/DavisVaughan/uncc-math-6204/tree/master/assignments/hw-03

Documentation for the modules is hosted by github pages at



### General

* Author   - Davis Vaughan
* Date     - 9/21/2017
* Homework - 03

### Purpose

The purpose of this module is to calculate the Monte Carlo value of European options in multiple
ways using varying methods of accuracy.

### Comments

IMPORTANT! - The seed is set at the C++ level using Numba, not at the Python level. Because of this,
we will not get the same results unless you implement this with Numba. Setting a seed of 100 at 
the C++ level will generate a different stream of random numbers than setting a seed of 100 at 
the Python level.

### Thoughts on numerical accuracy

It seems like using a smaller time step seems to greatly increase the accuracy.
Adding the second order term did not help the accuracy as much as I had expected.
The biggest benefits seem to come from increasing the number of simulations.
Using n = 50000 greatly increases the accuracy of the final results.

### Numerical methods used 

* Both Euler and Milstein discretization of GBM were used to simulate the sample paths. 

* Using the value of S_T from the sample paths, the average payoffs of the option were calculated,
and discounted back to time zero.

* The exact solution to the GBM SDE was also used to compare accuracy results.

### Included files

`main.py`         - (DRIVER) a demo of the GBM functions using the parameters set in the HW-2 pdf.

`gbm_simulator.py` - The functions that generate the stock price simulations using either
 Euler or Miltstein methods.
 
`option_value.py` - Functions to calculate the value of the option from the simulated values.
 
`option_value_exact.py` - Previous HW code to generate the exact value of the options.

### How to run 

Because the main.py file includes the code:

```python
if __name__ == "__main__":
    print(main())
```

the easiest way to run the example is from the terminal.

Within your command line / terminal, navigate to the folder containing the main.py script, and just run:

```bash
python2 main.py
```

^ Make sure you are using python2.

A plot will pop up first with the 5 paths, and once you close the plot a numpy array
will be printed to the console that looks like this:

```python
   MC_option_value algorithm call_put    dt  exact_option_value option_type  \
0        28.189921     euler     call   .01           28.684884    european   
1        29.255651     euler      put   .01           28.198446    european   
2        28.164755     euler     call  .001           28.684884    european   
3        28.579581     euler      put  .001           28.198446    european   
4        27.931396  milstein     call   .01           28.684884    european   
5        29.136742  milstein      put   .01           28.198446    european   
6        28.118083  milstein     call  .001           28.684884    european   
7        28.570122  milstein      put  .001           28.198446    european   

   absolute_error  
0        0.494962  
1        1.057205  
2        0.520129  
3        0.381135  
4        0.753487  
5        0.938296  
6        0.566800  
7        0.371676 
```
