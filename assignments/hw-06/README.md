### Description

This README is intended to guide the user in how to use HW-06.

The assignment is hosted on github here:

https://github.com/DavisVaughan/uncc-math-6204/tree/master/assignments/hw-06

### General

* Author   - Davis Vaughan
* Date     - 10/26/2017
* Homework - 06

### Purpose

The purpose of this module is to calculate the value of European call and put
options using fourier transforms. The theory is developed in presentation 07,
and the pricing integral is calculated through the trapezoidal rule. A more
efficient way to calculate the integral is by FFT. The documentation of each 
function presents the closed form solutions of the pricing integrals and 
the pieces involved to evaluate them.

### Thoughts on numerical accuracy

With the six values of alpha that are tested in this HW, the algorithm is 
stable. Given N = 1000, these values all converge to the same answer for a put/call.
With N = 100, the values are all close to each other, but aren't exactly the same.

This being said, it seems that the value of alpha works best in a certain range.
Increasing the alpha value to 50 makes the algorithm give wildly large answers
and decreasing the alpha value to .001 makes the algorithm give answers in the 
hundreds.

### Numerical methods used

For the theoretical work, the fourier transform and inverse fourier transform
were used to find the solution to the option price. To implement them, 
the trapezoidal rule was used to approximate the integral after picking an 
upper bound on the frequency domain.

### Included files

`main.py` - (DRIVER) Price the option over a number of different values of alpha.

`price_option_trapezoid_method.py` - Contains functions that price the European option.

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
0    2.5     31.792518
1   -2.5      7.890872
2    5.0     31.792518
3   -5.0      7.890872
4   10.0     31.792518
5  -10.0      7.890872
```