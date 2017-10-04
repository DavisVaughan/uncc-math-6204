### Description

This README is intended to guide the user in how to use HW-04.

The assignment is hosted on github here:

https://github.com/DavisVaughan/uncc-math-6204/tree/master/assignments/hw-04

### General

* Author   - Davis Vaughan
* Date     - 10/04/2017
* Homework - 04

### Purpose

The purpose of this module is to calculate the Monte Carlo value of American options 
using the regression 1 approach from the Tools for Computational Finance book.

### Thoughts on numerical accuracy

I am not sure how accurate these values are. The European option value is ~28 for the 
same parameters, and I can't imagine the price of the American option being a lot more than
that. It should obviously be more expensive, but I don't think it should be >10 dollars more.

### Numerical methods used 

* The Euler discretization of GBM was used to simulate the sample paths. 

* This method prices the American option using a regression method.
    The continuation value at time t is calculated by regressing
    the discounted value of the option at time t+1 on the
    price at time t. The continuation value is then compared to
    the value of the payoff at time t, and the max is chosen as the
    value of the option at t.

### Included files

`main.py`         - (DRIVER) Simulates the GBM and calculates the American option values at different
degrees of accuracy.

`gbm_simulator.py` - The functions that generate the stock price simulations using
 Euler methods.
 
`option_value.py` - The `price_option()` function in this file is the interface that
prices the option based on the user's inputs. It dispatches to find the correct pricing
function using the functions in `option_value_dispatch.py`.
 
`option_value_dispatch.py` - These function support `option_value.py` and are used 
to return the correct option pricing function (European VS American and Call VS Put).

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

A pandas data frame should output:

```python
   MC_option_value call_put    dt option_type
0        43.226182     call   .01    american
1        37.582431      put   .01    american
2        45.613229     call  .001    american
3        41.250757      put  .001    american
```