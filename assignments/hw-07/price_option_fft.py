import numpy as np
import collections
from math import pi

def price_option_fft(s_0, k_min, r, t_0, t_T, sigma, n, h, alpha):
    '''Price a European option by the fft method.

    This method calculates the pricing integral obtained from an inverse fourier transform involving the
    fourier transform of the normalized option price. Different than the trapezoidal method, it calculates
    the value of a range of options, varied by their strike price. The range goes from k_min to k_min+N*delta_k.

    The approximation that it calculates is

    .. math:: V_{k_n} = Re \Big\{ \\frac{e^{-\\alpha k_n}}{\pi} \sum_{m = 0}^{N-1} e^{i \omega_m k_n} \hat{\\nu}(w_m) \Delta \omega_m \Big\}

    With

    .. math:: e^{i \omega_m k} = e^{2 \pi i \\frac{m n}{N}} e^{i \omega_m k_0}


    Parameters
    ----------
    s_0 : double
        The initial price of the asset.
    k_min : double
        The minimum stike price for the option.
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
        The damping parameter. If positive, it prices a call. If negative, a put.

    Returns
    -------
    prices: named tuple
        A tuple of length 2 containing the prices and the corresponding strike prices, K.
    '''

    ## Setup
    # Total time difference
    t_discount = t_T - t_0
    # Steps from 0:N-1
    discretized_steps = np.arange(0, n)
    # Must use log(s_0) and log(k)
    x_0     = np.log(s_0)
    log_k_0 = np.log(k_min)

    # Set up k_n vector to calculate the prices over
    delta_k = 2 * np.pi / (h * n)
    log_k_n = log_k_0 + discretized_steps * delta_k

    # Create the delta_omega_n sequence of time steps.
    # FFT requires h/2 at the beginning, and N-1 steps total.
    delta_omega_m = np.append(h / 2.0, np.repeat(h, n - 1))

    # omega_m = delta_omega_m * m
    omega_m = delta_omega_m * discretized_steps

    # Calculate the fourier transform of the modified price
    nu_vec = nu_hat(omega_m, x_0, r, t_discount, sigma, alpha)

    # Calculate A_m that gets the inverse fft
    A_m = np.exp(1j * omega_m * log_k_0) * nu_vec * delta_omega_m * n

    # Inverse fft a_n
    a_n = np.fft.ifft(A_m)

    # Value of the option
    V_k_n = np.exp(- alpha * log_k_n) / np.pi * a_n.real

    # Create a named tuple to return them
    option_price = collections.namedtuple('option_price', ['price', 'K'])
    prices = option_price(price = V_k_n, K = np.exp(log_k_n))

    return prices

def nu_hat(omega_m, x_0, r, t_discount, sigma, alpha):
    """Calculate the fourier transform of the normalized European option value.

    The transform is available in closed form as:

    .. math:: \hat{\\nu}_c(w) = \\frac{e^{-r(T-t)}}{(\\alpha - i  \omega)(\\alpha - i  \omega + 1)} \hat{q}(\omega + (\\alpha + 1)i)

    With q written as:

    .. math:: \hat{q}(\omega') = e^{-i (x_0 + (r - \delta - \sigma^2 / 2) (T - t_0) ) \omega' - \\frac{\sigma^2 (T - t_0)}{2} \omega' ^ 2}



    Parameters
    ----------
    omega_m : Numpy array
        The discretized domain the calculate the transform over.
    x_0 : double
        The log of the initial stock price.
    r : double
        The risk free interest rate to discount at.
    t_discount : double
        The difference of t_T - t_0. This is the discount rate.
    sigma : double
        The volatility of the stock.
    alpha : double
        The damping parameter. If positive, it prices a call. If negative, a put.

    Returns
    -------
    transform : Numpy array
        The transform calculated at each omega_m.

    See also
    ----------
    price_option_trapezoid_method

    """

    # Calculate q_hat
    q = q_hat(omega_m + (alpha + 1) * 1j, x_0, r, sigma)

    # Individually calculate pieces of nu_hat
    numerator = np.exp(-r * t_discount) * q
    denominator = (alpha - 1j * omega_m) * (alpha - 1j * omega_m + 1)

    return numerator / denominator

def q_hat(omega, x_0, r, sigma):

    return np.exp(-1j * (x_0 + r - sigma ** 2 / 2.0) * omega - sigma ** 2 / 2.0 * omega ** 2)
