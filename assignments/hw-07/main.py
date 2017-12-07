'''
### Description

This README is intended to guide the user in how to use HW-07.

The assignment is hosted on github here:

https://github.com/DavisVaughan/uncc-math-6204/tree/master/assignments/hw-07

### General

* Author   - Davis Vaughan
* Date     - 10/31/2017
* Homework - 07

### Purpose

The purpose of this module is to calculate the value of European call and put
options using fourier transforms. The theory is developed in presentation 07,
and the pricing integral is calculated through the FFT. The benefit of this
method is that it prices a range of options at once, varied by the strike.
The documentation of each function presents the closed form solutions of
the pricing integrals and the pieces involved to evaluate them.

### Thoughts on numerical accuracy

The values of alpha all converge on the correct prices. However, alpha = -10 does produce an error.
When evaluating the option price, the calculation exp(-alpha * k_n) produces infinity values for
large k_n. I think this is just a numerical accuracy problem, but it may be a small error on my
part somewhere. I looked but couldn't find anything.

### Numerical methods used

For the theoretical work, the fourier transform and inverse fourier transform
were used to find the solution to the option price. To implement them,
the inverse fft was used to approximate the integral after picking an
upper bound on the frequency domain.

### Included files

`main.py` - (DRIVER) Price the option over a number of different values of alpha and K.

`price_option_fft.py` - Contains functions that price the European option.

### How to run

Because the main.py file includes the code:


if __name__ == "__main__":
    print(main())


the easiest way to run the example is from the terminal.

Within your command line / terminal, navigate to the folder containing the main.py script, and just run:

python2 main.py


A pandas data frame should output:

alpha  option_price
0    2.5     31.811887
1   -2.5      7.910241
2    5.0     31.811887
3   -5.0      7.910241
4   10.0     31.811887
5  -10.0      7.910241

'''


from price_option_fft import price_option_fft
import pandas as pd
import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt

def main():

    # Parameters
    n          = 2 ** 10
    b          = 50
    h          = float(b) / (n - 1)
    s_0        = 100
    k          = 80
    k_min      = 20
    r          = 0.05
    t_0        = 0
    t_T        = 1
    sigma      = 0.50
    alpha_1    = 2.5
    alpha_2    = 5
    alpha_3    = 10

    # Set up alphas to iterate over
    alphas = [alpha_1, -alpha_1, alpha_2, -alpha_2, alpha_3, -alpha_3]

    # Set up holder data frame
    prices = pd.DataFrame({
        'option_price' : np.repeat(0.0, np.size(alphas)),
        'alpha'        : alphas
    })

    figure, axes = plt.subplots(3, 2, sharex = True, sharey = False)

    # Calculate the option price for each alpha
    i = [0, 0, 1, 1, 2, 2]
    j = [0, 1, 0, 1, 0, 1]
    a = 0

    for alpha in alphas:
        # Calculate the range of option prices
        price_vec, k_vec = price_option_fft(s_0, k_min, r, t_0, t_T, sigma, n, h, alpha)

        # Interpolate to get right at K = 80
        interp_fun = interpolate.interp1d(k_vec, price_vec)
        price_at_k = interp_fun(k)
        prices.option_price[a] = price_at_k

        # Set up the plotting range (only plot a subset)
        k_plot_range = np.arange(20, 100, .01)
        V_plot_range = interp_fun(k_plot_range)

        # Plot V VS K
        axes[i[a], j[a]].plot(k_plot_range, V_plot_range)
        axes[i[a], j[a]].set_title(r'K VS V with $\alpha =$ ' + str(alpha))
        axes[i[a], j[a]].set_xlabel('K')
        axes[i[a], j[a]].set_ylabel('V')

        a = a + 1

    plt.tight_layout()
    plt.show()

    return prices


if __name__ == "__main__":
    print(main())