from math import log
from math import sqrt
import numpy as np
from scipy.stats import norm

# Parameters
k = 100
s_0 = 100
t = 0
t_terminal = 1
div_yield = 0.025
r = 0.05
sigma = 0.10


def d_1(s, k, r, div_yield, t_terminal, t, sigma):
    numer = log(s / k) + (r - div_yield + sigma**2 / 2) * (t_terminal - t)
    denom = sigma * sqrt(t_terminal - t)
    return numer / denom
    
def d_2(s, k, r, div_yield, t_terminal, t, sigma):
    return d_1(s, k, r, div_yield, t_terminal, t, sigma) - sigma * sqrt(t_terminal - t)
    
def V_eur_call(s, k, r, div_yield, t_terminal, t, sigma):
    
    F_d_1 = norm.cdf(d_1(s, k, r, div_yield, t_terminal, t, sigma))
    F_d_2 = norm.cdf(d_2(s, k, r, div_yield, t_terminal, t, sigma))
    
    V = s * np.exp(-1 * div_yield * (t_terminal - t)) * F_d_1 - k * np.exp(-1 * r * (t_terminal - t)) * F_d_2
    return V
    
    
V_eur_call(s_0, k, r, div_yield, t_terminal, t, sigma)



