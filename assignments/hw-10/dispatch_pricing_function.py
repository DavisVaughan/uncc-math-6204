import numpy as np
from pricing_function_closed_form import pricing_function_closed_form
from pricing_function_fdm import pricing_function_fdm
from pricing_function_monte_carlo import pricing_function_monte_carlo

def dispatch_pricing_function(method, solver, option_type, call_put):
    '''Dispatch to get the correct pricing function based on the user's inputs
    '''

    # Get the function specific to a call or put option price at time T
    if call_put == "call":
        option_price_at_T = option_price_at_T_call
    elif call_put == "put":
        option_price_at_T = option_price_at_T_put

    # Return the pricing function
    if method == "monte_carlo":
        pricing_function = pricing_function_monte_carlo(option_type, option_price_at_T)

    elif method == "closed_form":
        # Always a European option
        pricing_function = pricing_function_closed_form(call_put)

    elif method in ["crank_nicholson", "implicit_fdm", "explicit_fdm"]:
        pricing_function = pricing_function_fdm(method, solver, option_type, call_put)

    return pricing_function

# ----------------------------------------------------------------------------------------------------------------------
# Option price at T for call/put

def option_price_at_T_call(s_T, k):

    v_T = np.maximum(s_T - k, 0)

    return v_T

def option_price_at_T_put(s_T, k):

    v_T = np.maximum(k - s_T, 0)

    return v_T