import numpy as np
import sys

def simulate_gbm(n, s, r, div_yield, t, t_terminal, dt, sigma, method = "euler", seed = None):
    """Simulate a geometric brownian motion path

    The GBM is simulated using either the Euler or Milstein method. Instead of a loop, the algorithms have been
    vectorized for speed.

    Euler:

    :math:`S_{t+1} = S_{t} + \mu S_{t} dt + \sigma S_{t} \sqrt{dt} Z_{t+1}`

    Milstein:

    :math:`S_{t+1} = S_{t} + \mu S_{t} dt + \sigma S_{t} \sqrt{dt} Z_{t+1} + .5 \sigma ^ 2 ((\sqrt{dt} Z_{t+1}) ^ 2 - dt)`

    Parameters
    ----------
    n : double
        The number of paths to simulate
    s : double
        Initial stock price at time t.
    r : double
        The risk free interest rate.
    div_yield : double
        Dividend yield.
    t_terminal : double
        Terminal time T
    t : double
        Starting time
    dt : double
        Discretization time step size
    sigma : double
        Volatility
    method : {"euler", "milstein"}, defaults "euler"
        Numerical method to simulate with
    seed : int
        Random seed to set for random normal generation

    Returns
    ----------
    sims : Numpy array
        An array containing the n simulations as rows and the time steps as columns

    See also
    ----------
    option_value.price_option

    """

    # Set the seed
    if seed is not None:
        np.random.seed(seed)

    # Total time steps
    t_total = int((t_terminal - t) / dt)

    # Random normal generation
    z = np.random.randn(n, t_total)

    # Fill in the simulation matrix
    s_t = dispatch_simulation(n, s, r, div_yield, dt, sigma, z, method)

    return s_t


def dispatch_simulation(n, s, r, div_yield, dt, sigma, z, method):
    '''Dispatch the simulation to the appropriate algorithm'''

    if method == "euler":

        s_t = simulate_gbm_euler(n, s, r, div_yield, dt, sigma, z)

    elif method == "milstein":

        s_t = simulate_gbm_milstein(n, s, r, div_yield, dt, sigma, z)

    else:

        sys.exit("Method not supported.")

    return s_t


def simulate_gbm_euler(n, s, r, div_yield, dt, sigma, z):
    '''GBM simulation using a Euler discretization'''

    cumprod_z = np.cumprod(1 + (r - div_yield) * dt + sigma * np.sqrt(dt) * z,
                           axis = 1)

    cumprod_z = np.column_stack((np.ones([n, 1]), cumprod_z))

    s_t = s * cumprod_z

    return s_t


def simulate_gbm_milstein(n, s, r, div_yield, dt, sigma, z):
    '''GBM simulation using a Milstein discretization'''

    cumprod_z = np.cumprod(1 + (r - div_yield) * dt + sigma * np.sqrt(dt) * z \
                           + .5 * sigma * sigma * ((np.sqrt(dt) * z) ** 2 - dt),
                           axis = 1)

    cumprod_z = np.column_stack((np.ones([n, 1]), cumprod_z))

    s_t = s * cumprod_z

    return s_t