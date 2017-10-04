import numpy as np
import sys
import scipy.optimize as scipy_opt

def price_option(s, k, r, T, call_put = "call", option_type = "european"):
    """
    Calculate the time 0 value of an option from Monte Carlo simulations.

    Parameters
    ----------
    s : Numpy array
        The simulated paths of the option.
    k : double
        The strike price for the option.
    r : double
        The risk free interest rate to discount at.
    T : double
        The expiration date of the option. Used to discount.
    call_put : {"call", "put"}, default "call"
        Specifications for the side of the option to price.
    option_type : {"european", "american"}, default "european"
        The type of option to price.

    Returns
    ----------
    price : double
        The Monte Carlo value of the option

    See also
    ----------
    simulate_gbm

    """

    # Error checking
    if call_put not in ["call", "put"]:
        sys.exit("Either 'call' or 'put' must be specified.")

    if option_type not in ["european", "american"]:
        sys.exit("Option type must be 'european' or 'american'.")

    # Get pricing method
    pricing_method = dispatch_pricing_method(call_put, option_type)

    # Apply pricing method
    v_0 = pricing_method(s, k, r, T)

    return v_0

#### Util --------------------------------------------------------------------------------------------------------------


def dispatch_pricing_method(call_put = "call", option_type = "european"):
    '''
    Formulate the correct option pricing function from user inputs
    :param call_put:     Either "call" or "put"
    :param option_type:  Either "european" or "american"
    :return:             A function that prices the specified type of option
    '''

    # Get the function specific to a call or put option price at time T
    if call_put == "call":

        option_price_at_T = option_price_at_T_call

    elif call_put == "put":

        option_price_at_T = option_price_at_T_put

    # Get the pricing method specific to european or american
    if option_type == "european":

        pricing_method = european(option_price_at_T)

    elif option_type == "american":

        pricing_method = american(option_price_at_T)

    return pricing_method


def european(call_put_option_price_at_T):
    '''
    Return a function that prices a European call/put
    :param call_put_option_price_at_T:  A pricing function that prices the value of the option at T. This is different
    depending on whether the option is a call or a put.
    :return:          European pricing function
    '''

    # Create the European pricing function
    def european_pricing_method(s, k, r, T):
        '''
        Price a european call / put from simulated values.
        :param s:  An array of simulated stock prices
        :param k:  Strike price
        :param r:  Discount rate
        :param T:  Number of periods to discount
        :return:   The price of the european option
        '''

        # Extract the s_T column
        # This is all that is needed for European options
        s_T = s[:, -1]

        # Apply call / put option value at T
        v_T = call_put_option_price_at_T(s_T, k)

        # Discount
        v_0 = np.exp(- r * T) * np.mean(v_T)

        return v_0

    return european_pricing_method


def american(call_put_option_price_at_T):
    '''
    Return a function that prices an American call/put
    :param call_put_option_price_at_T:  A pricing function that prices the value of the option at T. This is different
    depending on whether the option is a call or a put. The function should accept s_T and k as parameters.
    :return:          American pricing function
    '''

    def american_pricing_method(s, k, r, T):
        '''
        Price an American call/put option from simulated values.
        Uses regression method 1 from
        :param s:
        :param k:
        :param r:
        :param T:
        :return:
        '''

        dt = T / float(s.shape[1] - 1)
        v = np.zeros(s.shape)

        # At i = M = T, use value at T
        v[:, -1] = call_put_option_price_at_T(s[:, -1], k)

        # Basis function
        def basis_func_C(x, a0, a1, a2, a3):
            return a0 + (a1 * x) + (a2 * x ** 2) + (a3 * x ** 3)

        # Iterate backwards
        iteration = (np.arange(v.shape[1] - 2) + 1)[::-1]

        for i in iteration:

            # x and y values for each regression
            s_ik = s[:, i]
            yvalues = np.exp(-r * dt) * v[:, i + 1]

            # Fit the 3rd ordered curve
            C_fit = scipy_opt.curve_fit(basis_func_C, s_ik, yvalues)
            params = C_fit[0]

            # Use the optimal parameters
            C_hat = basis_func_C(s_ik, *params)

            # Calculate the value of the option if this was time T
            s_ik_v = call_put_option_price_at_T(s_ik, k)

            # Take the max of the two to be the current value
            v[:, i] = np.maximum(s_ik_v, C_hat)

        # Discount time 1 to time 0
        v[:, 0] = np.exp(-r * dt) * v[:, 1]

        # Average the paths to get the Monte Carlo result
        v_0 = np.mean(v[:, 0])

        return v_0

    return american_pricing_method


def option_price_at_T_call(s_T, k):
    '''
    Return the option value at time T for a call
    :param s_T:  Stock price at T
    :param k:    Strike price
    :return:     Option value at T
    '''

    v_T = np.maximum(s_T - k, 0)

    return v_T

def option_price_at_T_put(s_T, k):
    '''
    Return the option value at time T for a put
    :param s_T:  Stock price at T
    :param k:    Strike price
    :return:     Option value at T
    '''

    v_T = np.maximum(k - s_T, 0)

    return v_T