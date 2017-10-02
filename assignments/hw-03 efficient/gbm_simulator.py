import numpy as np
import sys
import numba

def simulate_gbm(n, s, r, div_yield, t, t_terminal, dt, sigma, method = "euler", seed = None):
    """
    Simulate a geometric brownian motion path
    :param n:          Number of simulations
    :param s:          Stock price at time t
    :param r:          Risk free interest rate
    :param div_yield:  Continuous dividend yield
    :param t_terminal: Terminal time
    :param t:          Starting time
    :param dt:         Discretization time step size
    :param sigma:      Volatility
    :param method:     Simulation method, either "euler" or "milstein"
    :param seed:       Random seed used
    :return:           An array containing the n simulations as rows and the time steps as columns
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
    '''
    Dispatch the simulation to the appropriate algorithm
    :return: s_t filled with the simulation values
    '''

    if method == "euler":

        s_t = simulate_gbm_euler(n, s, r, div_yield, dt, sigma, z)

    elif method == "milstein":

        s_t = simulate_gbm_milstein(n, s, r, div_yield, dt, sigma, z)

    else:

        sys.exit("Method not supported.")

    return s_t


def simulate_gbm_euler(n, s, r, div_yield, dt, sigma, z):
    '''
    GBM simulation using a Euler discretization
    :return: s_t filled with the simulation values by Euler
    '''

    cumprod_z = np.cumprod(1 + (r - div_yield) * dt + sigma * np.sqrt(dt) * z,
                           axis = 1)

    cumprod_z = np.column_stack((np.ones([n, 1]), cumprod_z))

    s_t = s * cumprod_z

    return s_t


def simulate_gbm_milstein(n, s, r, div_yield, dt, sigma, z):
    '''
    GBM simulation using a Milstein discretization
    :return: s_t filled with the simulation values by Milstein
    '''

    cumprod_z = np.cumprod(1 + (r - div_yield) * dt + sigma * np.sqrt(dt) * z \
                           + .5 * sigma * sigma * ((np.sqrt(dt) * z) ** 2 - dt),
                           axis = 1)

    cumprod_z = np.column_stack((np.ones([n, 1]), cumprod_z))

    s_t = s * cumprod_z

    return s_t