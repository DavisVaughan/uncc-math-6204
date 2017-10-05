'''
### Description

This README is intended to guide the user in how to use HW-05.

The assignment is hosted on github here:

https://github.com/DavisVaughan/uncc-math-6204/tree/master/assignments/hw-05

### General

* Author   - Davis Vaughan
* Date     - 10/05/2017
* Homework - 05

### Purpose

The purpose of this module is to calculate the Monte Carlo value of American options
using the regression 2 approach from the Tools for Computational Finance book.

### Thoughts on numerical accuracy

I think that the values in HW5 are MUCH more accurate than those in HW4.
With our computational constraints, only considering the in the money values
allows our numerical method to converge to the true value of the option much faster.

### Numerical methods used

The Euler discretization of GBM was used to simulate the sample paths.

This method prices the American option using a regression method.
The continuation value at time t is calculated by regressing
the discounted value of the option at time t+1 on the
price at time t. The continuation value is then compared to
the value of the payoff at time t, and the max is chosen as the
value of the option at t.

Notably, this is regression method 2, which only considers points that are
in the money when running the regression and making updating decisions.

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

if __name__ == "__main__":
    print(main())

the easiest way to run the example is from the terminal.

Within your command line / terminal, navigate to the folder containing the main.py script, and just run:

`python2 main.py`

^ Make sure you are using python2.

A pandas data frame should output:

   MC_option_value call_put    dt option_type
0        31.389674     call   .01    american
1        28.906298      put   .01    american
2        15.292809     call  .001    american
3        29.552257      put  .001    american

'''

from option_value import price_option
from gbm_simulator import simulate_gbm
import pandas as pd

def main():

    # Parameters
    n          = 1000
    s          = 100
    k          = 100
    #mu        = 0.08 # Only r is used
    r          = .03
    div_yield  = 0.025
    t          = 0
    t_terminal = 1
    dt         = 0.01
    dt2        = 0.001
    sigma      = 0.75
    seed       = 123

    # GBM Sims
    gbm_euler_t01  = simulate_gbm(n, s, r, div_yield, t, t_terminal, dt,  sigma, method = "euler", seed = seed)
    gbm_euler_t001 = simulate_gbm(n, s, r, div_yield, t, t_terminal, dt2, sigma, method = "euler", seed = seed)

    # Option prices
    am_call_t01  = price_option(gbm_euler_t01,  k, r, t_terminal, call_put = "call", option_type = "american")
    am_put_t01   = price_option(gbm_euler_t01,  k, r, t_terminal, call_put = "put",  option_type = "american")
    am_call_t001 = price_option(gbm_euler_t001, k, r, t_terminal, call_put = "call", option_type = "american")
    am_put_t001  = price_option(gbm_euler_t001, k, r, t_terminal, call_put = "put",  option_type = "american")

    # Price dataframe
    option_prices = pd.DataFrame({
        'dt': [".01", ".01", ".001", ".001"],
        'option_type': ["american"] * 4,
        'call_put': ["call", "put"] * 2,
        'MC_option_value': [
            am_call_t01,
            am_put_t01,
            am_call_t001,
            am_put_t001
        ]
    })

    return option_prices


if __name__ == "__main__":
    print(main())