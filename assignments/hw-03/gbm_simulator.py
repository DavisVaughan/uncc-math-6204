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

    # Total time steps
    t_total   = int((t_terminal - t) / dt)

    # Initialize s_t matrix. First column is initial stock price
    s_t       = np.empty([n, t_total + 1])
    s_t[:, 0] = s

    # Fill in the simulation matrix
    s_t = dispatch_simulation(s_t, r, div_yield, t_total, dt, sigma, method, n, seed)

    return s_t


def dispatch_simulation(s_t, r, div_yield, t_total, dt, sigma, method, n, seed):
    '''
    Dispatch the simulation to the appropriate algorithm
    :return: s_t filled with the simulation values
    '''

    if method == "euler":

        s_t = simulate_gbm_euler(s_t, r, div_yield, t_total, dt, sigma, n, seed)

    elif method == "milstein":

        s_t = simulate_gbm_milstein(s_t, r, div_yield, t_total, dt, sigma, n, seed)

    else:

        sys.exit("Method not supported.")

    return s_t


@numba.jit
def simulate_gbm_euler(s_t, r, div_yield, t_total, dt, sigma, n, seed):
    '''
    GBM simulation using a Euler discretization
    :return: s_t filled with the simulation values by Euler
    '''

    # Set the seed at the C++ level
    # Note that this gives different results than setting the seed at the Python level
    if seed:
        np.random.seed(seed)

    for i in range(1, t_total + 1):

        # For memory reasons, only generate 1 column of z at a time
        # This happens at the C++ level and is extremely fast
        z = np.random.randn(n)

        s_t[:, i] = s_t[:, i - 1] + \
                    (r - div_yield) * s_t[:, i - 1] * dt + \
                    sigma * s_t[:, i - 1] * np.sqrt(dt) * z

    return s_t


@numba.jit
def simulate_gbm_milstein(s_t, r, div_yield, t_total, dt, sigma, n, seed):
    '''
    GBM simulation using a Milstein discretization
    :return: s_t filled with the simulation values by Milstein
    '''

    # Set the seed at the C++ level
    # Note that this gives different results than setting the seed at the Python level
    if seed:
        np.random.seed(seed)

    for i in range(1, t_total + 1):

        # For memory reasons, only generate 1 column of z at a time
        # This happens at the C++ level and is extremely fast
        z = np.random.randn(n)

        # Euler method + second order term
        s_t[:, i] = s_t[:, i - 1] + \
                    (r - div_yield) * s_t[:, i - 1] * dt + \
                    sigma * s_t[:, i - 1] * np.sqrt(dt) * z + \
                    0.5 * sigma * s_t[:, i - 1] * sigma * ((np.sqrt(dt) * z) ** 2 - dt)

    return s_t