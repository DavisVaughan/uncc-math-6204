import numpy as np
import sys

def price_option(s, k, r, T, call_put = "call", option_type = "european"):
    '''
    Calculate the time 0 value of an option from Monte Carlo simulations
    :param s:           An array of the simulated paths of the option
    :param k:           The strike price for the option
    :param r:           The risk free interest rate to discount at
    :param T:           The number of years to discount
    :param call_put:    Either "call" or "put"
    :param option_type: The type of option. Currently only "european" is supported
    :return:            The Monte Carlo value of the European option
    '''

    # Error checking
    if call_put not in ["call", "put"]:
        sys.exit("Either 'call' or 'put' must be specified.")

    if option_type not in ["european"]:
        sys.exit("Option type must be 'european'.")


    # European option
    if option_type == "european":

        # Extract the s_T column
        # This is all that is needed for European options
        s_T = s[:, -1]

        # Calculate the eurpoean payoff based on call/put
        if call_put == "call":

            v_T = np.maximum(s_T - k, 0)

        elif call_put == "put":

            v_T = np.maximum(k - s_T, 0)

    # Discount
    v_0 = np.exp(- r * T) * 1 / len(v_T) * np.sum(v_T)

    return v_0




