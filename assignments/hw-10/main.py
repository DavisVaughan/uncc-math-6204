'''
### Description

This README is intended to guide the user in how to use HW-10.

The assignment is hosted on github here:

https://github.com/DavisVaughan/uncc-math-6204/tree/master/assignments/hw-10

### General

* Author   - Davis Vaughan
* Date     - 12/07/2017
* Homework - 10

### Purpose

This HW is an all-purpose option pricer that allows the user to price
European or American options using a range of different techniques.

### Thoughts on numerical accuracy

Each algorithm has its own flaws and drawbacks, but the combination
of algorithms together should give the user a reasonable idea of what
the option price should be, even if an exact answer cannot be given.

The ability to control some of the underlying options should allow the
user to achieve higher levels of precision

### Numerical methods used

- SOR
- PSOR
- Thomas
- Brennan
- Finite difference methods
- Monte Carlo simulation
- Black scholes exact solutions

### Included files

`main.py` - (DRIVER) Driver for the entire program.

`SOR.py` - Contains functions that solve the system using the SOR algo.

`PSOR.py` - Contains functions that solve the system using the PSOR algo.

`PSOR.py` - Contains functions that solve the system using the PSOR algo.

`thomas.py` - Contains functions that solve the system using the Thomas algo.

`brennan.py` - Contains functions that solve the system using the Brennan algo.

`dispatch_pricing_function.py` - Retrieve the correct pricing function based on user input.

`gbm_simulator.py` - Simulate stock prices using geometric brownian motion

`price_option.py` - Main interface function that does the validation and hands off to the dispatcher

`pricing_function_closed_form.py` - Solves the Black Scholes European closed form option price.

`pricing_function_fdm.py` - Returns a solving function that implements the chosen FDM method/solver combination.

`pricing_function_monte_carlo.py` - Performs monte carlo simulation and discounts the prices back to time 0 to
get an option price.

`solvers.py` - Handles the solver lookup operation

### How to run

Because the main.py file includes the code:


if __name__ == "__main__":
    print(main())


the easiest way to run the example is from the terminal.

Within your command line / terminal, navigate to the folder containing the main.py script, and just run:

python3 main.py

You should get:

European option prices:
                     Method       Call        Put  Call_Error  Put_Error
0               Closed Form $23.727169 $22.742053   $0.000000  $0.000000
1               Monte Carlo $27.191132 $22.263111   $3.463963 $-0.478942
2                  Explicit $23.686678 $22.701779  $-0.040491 $-0.040274
3     SOR - Crank Nicholson $23.708316 $22.723106  $-0.018853 $-0.018947
4            SOR - Implicit $23.690751 $22.705237  $-0.036418 $-0.036816
5  Thomas - Crank Nicholson $23.708322 $22.723110  $-0.018847 $-0.018943
6         Thomas - Implicit $23.690786 $22.705261  $-0.036383 $-0.036792


American option prices:
                      Method       Call        Put
0                Monte Carlo $28.821161 $22.908044
1                   Explicit $23.698560 $22.841751
2     PSOR - Crank Nicholson $23.719982 $22.854661
3            PSOR - Implicit $23.702019 $22.832963
4  Brennan - Crank Nicholson $23.720096 $22.853696
5         Brennan - Implicit $23.702505 $22.831401

'''


import pandas as pd
from price_option import price_option

def main():

    # Parameters
    s          = 100
    k          = 100
    #mu        = 0.05 # Only r is used
    r          = 0.02
    div_yield  = 0.01
    t          = 0
    t_terminal = 1
    sigma      = 0.6

    # Common arguments
    args = {"s" : s, "k" : k, "r" : r, "div_yield" : div_yield, "t_terminal" : t_terminal, "t" : t, "sigma" : sigma}

    option_prices_euro = pd.DataFrame({
        'Method': [
             "Closed Form",
             "Monte Carlo",
             "Explicit",
             "SOR - Crank Nicholson",
             "SOR - Implicit",
             "Thomas - Crank Nicholson",
             "Thomas - Implicit"
        ],

        'Call': [
            price_option(**args, method = "closed_form",     option_type = "european", call_put = "call"),
            price_option(**args, method = "monte_carlo",     option_type = "european", call_put = "call", options = {"seed": 123}),
            price_option(**args, method = "explicit_fdm",    option_type = "european", call_put = "call"),
            price_option(**args, method = "crank_nicholson", option_type = "european", call_put = "call", solver = "iterative"),
            price_option(**args, method = "implicit_fdm",    option_type = "european", call_put = "call", solver = "iterative"),
            price_option(**args, method = "crank_nicholson", option_type = "european", call_put = "call", solver = "direct"),
            price_option(**args, method = "implicit_fdm",    option_type = "european", call_put = "call", solver = "direct")
        ],

        'Put': [
            price_option(**args, method = "closed_form",     option_type = "european", call_put = "put"),
            price_option(**args, method = "monte_carlo",     option_type = "european", call_put = "put", options = {"seed": 123}),
            price_option(**args, method = "explicit_fdm",    option_type = "european", call_put = "put"),
            price_option(**args, method = "crank_nicholson", option_type = "european", call_put = "put", solver = "iterative"),
            price_option(**args, method = "implicit_fdm",    option_type = "european", call_put = "put", solver = "iterative"),
            price_option(**args, method = "crank_nicholson", option_type = "european", call_put = "put", solver = "direct"),
            price_option(**args, method = "implicit_fdm",    option_type = "european", call_put = "put", solver = "direct")
        ]
    }, columns = ['Method','Call','Put'])

    option_prices_euro['Call_Error'] = option_prices_euro.Call - price_option(**args, method = "closed_form", option_type = "european", call_put = "call")
    option_prices_euro['Put_Error']  = option_prices_euro.Put  - price_option(**args, method = "closed_form", option_type = "european", call_put = "put")

    option_prices_americ = pd.DataFrame({
        'Method': [
             "Monte Carlo",
             "Explicit",
             "PSOR - Crank Nicholson",
             "PSOR - Implicit",
             "Brennan - Crank Nicholson",
             "Brennan - Implicit"
        ],

        'Call': [
            price_option(**args, method = "monte_carlo",     option_type = "american", call_put = "call", options = {"seed": 123}),
            price_option(**args, method = "explicit_fdm",    option_type = "american", call_put = "call"),
            price_option(**args, method = "crank_nicholson", option_type = "american", call_put = "call", solver = "iterative"),
            price_option(**args, method = "implicit_fdm",    option_type = "american", call_put = "call", solver = "iterative"),
            price_option(**args, method = "crank_nicholson", option_type = "american", call_put = "call", solver = "direct"),
            price_option(**args, method = "implicit_fdm",    option_type = "american", call_put = "call", solver = "direct")
        ],

        'Put': [
            price_option(**args, method = "monte_carlo",     option_type = "american", call_put = "put", options = {"seed": 123}),
            price_option(**args, method = "explicit_fdm",    option_type = "american", call_put = "put"),
            price_option(**args, method = "crank_nicholson", option_type = "american", call_put = "put", solver = "iterative"),
            price_option(**args, method = "implicit_fdm",    option_type = "american", call_put = "put", solver = "iterative"),
            price_option(**args, method = "crank_nicholson", option_type = "american", call_put = "put", solver = "direct"),
            price_option(**args, method = "implicit_fdm",    option_type = "american", call_put = "put", solver = "direct")
        ]
    }, columns = ['Method','Call','Put'])

    # A bit of formatting
    pd.options.display.float_format = '${:,.6f}'.format

    print("European option prices:")
    print(option_prices_euro)

    print('\n')

    print("American option prices:")
    print(option_prices_americ)


if __name__ == "__main__":
    main()