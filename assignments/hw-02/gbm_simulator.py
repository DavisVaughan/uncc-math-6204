import numpy as np


def gbm(n, s, mu, div_yield, t, t_terminal, dt, sigma, seed = None):
    """
    Simulate a geometric brownian motion path
    :param n:          Number of simulations
    :param s:          Stock price at time t
    :param div_yield:  Continuous dividend yield
    :param t_terminal: Terminal time
    :param t:          Starting time
    :param dt:         Discretization time step
    :param sigma:      Volatility
    :param seed:       Random seed used
    :return:           Value of the european call option at time t
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
    for i in range(1, t_total + 1):
        s_t[:, i] = s_t[:, i-1] + (mu - div_yield) * s_t[:, i-1] * dt + sigma * s_t[:, i-1] * np.sqrt(dt) * z[:, i-1]

    return s_t