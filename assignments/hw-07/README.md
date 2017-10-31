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


```python
if __name__ == "__main__":
    print(main())
```


the easiest way to run the example is from the terminal.

Within your command line / terminal, navigate to the folder containing the main.py script, and just run:

```bash
python2 main.py
```


A pandas data frame should output:

```python
alpha  option_price
0    2.5     31.811887
1   -2.5      7.910241
2    5.0     31.811887
3   -5.0      7.910241
4   10.0     31.811887
5  -10.0      7.910241
```





