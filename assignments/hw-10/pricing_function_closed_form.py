# Imports
from math import log
from math import sqrt
from math import exp
from scipy.stats import norm

def pricing_function_closed_form(call_put):
    '''Retrieve the closed form solution pricing function for a european call/put
    '''


    if call_put == "call":
        pricing_function = pricing_function_closed_form_european_call
    elif call_put == "put":
        pricing_function = pricing_function_closed_form_european_put

    return pricing_function

def pricing_function_closed_form_european_call(s, k, r, div_yield, sigma, t_terminal, t):

    """
    Calculate the value of a european call option
    :param s:          Stock price at time t
    :param k:          Strike price at time T
    :param r:          Risk free rate
    :param div_yield:  Continuous dividend yield
    :param t_terminal: Terminal time
    :param t:          Starting time
    :param sigma:      Volatility
    :return:           Value of the european call option at time t
    """

    # Normal CDF values of d_1 and d_2 respectively
    F_d_1 = norm.cdf(d_1(s, k, r, div_yield, t_terminal, t, sigma))
    F_d_2 = norm.cdf(d_2(s, k, r, div_yield, t_terminal, t, sigma))

    # Value of the option from the closed form solution of Black Scholes
    V = s * exp(-1 * div_yield * (t_terminal - t)) * F_d_1 - k * exp(-1 * r * (t_terminal - t)) * F_d_2
    return V

def pricing_function_closed_form_european_put(s, k, r, div_yield, sigma, t_terminal, t):

    """
    Calculate the value of a european put option
    :param s:          Stock price at time t
    :param k:          Strike price at time T
    :param r:          Risk free rate
    :param div_yield:  Continuous dividend yield
    :param t_terminal: Terminal time
    :param t:          Starting time
    :param sigma:      Volatility
    :return:           Value of the european put option at time t
    """

    # Normal CDF values of -d_1 and -d_2 respectively
    F_neg_d_1 = norm.cdf(-1 * d_1(s, k, r, div_yield, t_terminal, t, sigma))
    F_neg_d_2 = norm.cdf(-1 * d_2(s, k, r, div_yield, t_terminal, t, sigma))

    # Value of the option from the closed form solution of Black Scholes
    V = -1 * s * exp(-1 * div_yield * (t_terminal - t)) * F_neg_d_1 + k * exp(-1 * r * (t_terminal - t)) * F_neg_d_2
    return V


### Utils


def d_1(s, k, r, div_yield, t_terminal, t, sigma):

    """
    Calculate d_1 as specified by Black Scholes
    """

    numerator   = log(s / k) + (r - div_yield + sigma**2 / 2) * (t_terminal - t)
    denominator = sigma * sqrt(t_terminal - t)

    return numerator / denominator

def d_2(s, k, r, div_yield, t_terminal, t, sigma):

    """
    Calculate d_2 as specified by Black Scholes
    """

    return d_1(s, k, r, div_yield, t_terminal, t, sigma) - sigma * sqrt(t_terminal - t)