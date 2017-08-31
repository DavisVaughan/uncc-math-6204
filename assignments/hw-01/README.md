### Description

This README is intended to guide the user in how to use the Black Scholes module.

The README is written in Markdown, and is much easier to read on GitHub:

https://github.com/DavisVaughan/uncc-math-6204/tree/master/assignments/hw-01

### General

* Author   - Davis Vaughan

* Date     - 8/31/2017

* Homework - 01

### Purpose

The purpose of this module is to generate the black scholes price of European call and put options.

### Numerical methods used 

The closed form solution of black scholes is used to generate the value of the options.
Within the closed form solution, the normal cdf function from scipy is used.

### Included files

`main.py`         - (DRIVER) a demo of the black scholes functions using the parameters set in the HW-1.

`option_value.py` - the functions that generate the black scholes option prices

### How to run 

Because the main.py file includes the code:

```python
if __name__ == "__main__":
    print(main())
```

the easiest way to run the example is from the terminal.

Within your command line / terminal, navigate to the folder containing the main.py script, and just run:

```bash
python main.py
```

A pandas dataframe should be printed to the console with the following form:

```python
   Euro Call   Euro Put  Volatility
0   5.164625   2.756577         0.1
1   8.936678   6.528629         0.2
2  12.729164  10.321115         0.3
3  16.503136  14.095087         0.4
4  20.243459  17.835410         0.5
5  23.939254  21.531205         0.6
6  27.581121  25.173073         0.7
7  31.160489  28.752441         0.8
8  34.669431  32.261382         0.9
9  38.100617  35.692569         1.0
```
