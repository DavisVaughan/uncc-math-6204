import sys
from option_value_dispatch import dispatch_pricing_method

def price_option(s, k, r, T, call_put = "call", option_type = "european"):
    """Calculate the time 0 value of an option.

    Paths `s` are constructed from :py:func:`gbm_simulator.simulate_gbm` but

    The unique thing about this approach is that it takes advantage of Python allowing functions to
    be first class objects. The correct option pricing function is constructed, and the passed up as
    the variable `pricing_method`.

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
    gbm_simulator.simulate_gbm

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
