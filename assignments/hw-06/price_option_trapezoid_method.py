import numpy as np
from math import pi

def price_option_trapezoid_method(s_0, k, r, t_0, t_T, sigma, n, h, alpha):
    '''
    Price a European option by the trapezoid method. This method calculates the pricing integral
    obtained from an inverse fourier transform involving the fourier transform of the normalized option price.
    Parameters
    ----------
    s_0 : double
        The initial price of the asset.
    k : double
        The stike price for the option.
    r : double
        The risk free interest rate to discount at.
    t_0 : double
        The initial time.
    t_T : double
        The terminal time.
    sigma : double
        The volatility of the stock.
    n : int
        The number of points to discretize over. Together with h, this determines the frequency domain
        endpoint on [0, B]. B = n * h.
    h : double
        The size of the discretization steps.
    alpha : double
        The damping parameter.

    Returns
    -------
    price: double
        The price of the option.
    '''

    ## Setup
    # Total time difference
    t_discount = t_T - t_0
    # Steps from 0:N
    discretized_steps = np.arange(0, n + 1)
    # Must use log(s_0) and log(k)
    x_0     = np.log(s_0)
    log_k   = np.log(k)

    # Create the delta_omega_n sequence of time steps. Trapezoid rule requires h/2 at the beginning and end
    delta_omega_m = np.append(np.append(h / 2.0, np.repeat(h, n - 1)), h / 2.0)

    # omega_m = delta_omega_m * m
    omega_m = delta_omega_m * discretized_steps

    # Calculate the fourier transform of the modified price
    nu_vec = nu_hat(omega_m, x_0, r, t_discount, sigma, alpha)

    # Calculate the complex price
    V_complex = np.exp(-alpha * log_k) / pi * sum(np.exp(1j * omega_m * log_k) * nu_vec * delta_omega_m)

    # Only take the real part
    price = V_complex.real

    return price

def nu_hat(omega_m, x_0, r, t_discount, sigma, alpha):

    q = q_hat(omega_m + (alpha + 1) * 1j, x_0, r, sigma)

    numerator = np.exp(-r * t_discount) * q
    denominator = (alpha - 1j * omega_m) * (alpha - 1j * omega_m + 1)

    return numerator / denominator

def q_hat(omega, x_0, r, sigma):

    return np.exp(-1j * (x_0 + r - sigma ** 2 / 2.0) * omega - sigma ** 2 / 2.0 * omega ** 2)
