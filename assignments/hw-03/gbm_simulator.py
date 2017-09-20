import numpy as np
import sys

def simulate_gbm(n, s, r, div_yield, t, t_terminal, dt, sigma, method = "euler", seed = None):
    """
    Simulate a geometric brownian motion path
    :param n:          Number of simulations
    :param s:          Stock price at time t
    :param r:          Risk free interest rate
    :param div_yield:  Continuous dividend yield
    :param t_terminal: Terminal time
    :param t:          Starting time
    :param dt:         Discretization time step
    :param sigma:      Volatility
    :param method:     Simulation method, either "euler" or "milstein"
    :param seed:       Random seed used
    :return:           An array containing the n simulations as rows and the time steps as columns
    """

    # Set seed if the user specifies it
    if seed:
        np.random.seed(seed = seed)

    # Total time steps
    t_total   = int((t_terminal - t) / dt)

    # Initialize s_t matrix. First column is initial stock price
    s_t       = np.empty([n, t_total + 1])
    s_t[:, 0] = s

    # Random normal matrix Z ~ N(0,1)
    # Only t_total - 1 steps are needed
    z = np.random.standard_normal(size = (n, t_total))

    # Fill in the simulation matrix
    if method == "euler":

        for i in range(1, t_total + 1):
            s_t[:, i] = s_t[:, i-1] + (r - div_yield) * s_t[:, i-1] * dt + sigma * s_t[:, i-1] * np.sqrt(dt) * z[:, i-1]

    elif method == "milstein":

        # Euler method + second order term
        for i in range(1, t_total + 1):
            s_t[:, i] = s_t[:, i-1] + (r - div_yield) * s_t[:, i-1] * dt + sigma * s_t[:, i-1] * np.sqrt(dt) * z[:, i-1] \
                        + 0.5 * sigma * s_t[:, i-1] * sigma * ( (np.sqrt(dt) * z[:, i-1]) ** 2 - dt)

    else:
        sys.exit("Method not supported.")



    return s_t