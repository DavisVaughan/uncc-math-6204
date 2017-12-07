import sys
from dispatch_pricing_function import dispatch_pricing_function
import numpy as np


def price_option(s, k, r, div_yield, sigma, t_terminal, t, method, option_type = "european", call_put = "call", solver = None, options = None):
    '''Main interface to price an American or European option by a number of methods

    Parameters
    ----------
    s : double
        The initial price of the asset.
    k : double
        The stike price for the option.
    r : double
        The risk free interest rate to discount at.
    div_yield : double
        The dividend yield
    t : double
        The initial time.
    t_terminal : double
        The terminal time.
    sigma : double
        The volatility of the stock.
    method : string
        One of: "crank_nicholson", "monte_carlo", "explicit_fdm", "implicit_fdm", "closed_form". Used to price the option.
    option_type : string
        Either: "european" or "american"
    call_put : string
        Either: "call" or "put"
    solver : string
        Either: "direct" or "iterative". This uses either Thomas / Brennan for direct, and SOR / PSOR for iterative
    options : dict
        A named dict containing overrides for various method specific parameters. Use get_option_defaults(method, solver)
        to see the options for a specfic method/solver combination.


    Returns
    -------
    prices: named tuple
        A tuple of length 2 containing the prices and the corresponding strike prices, K.
    '''

    # Validation
    validate_option_type(option_type)
    validate_call_put(call_put)
    validate_method_solver_combination(method, solver, option_type)

    # Set option defaults and update to user defined options
    option_values = replace_options(options, get_option_defaults(method, solver))

    pricing_function = dispatch_pricing_function(method, solver, option_type, call_put)

    option_price = pricing_function(s, k, r, div_yield, sigma, t_terminal, t, **option_values)

    return option_price

    print(option_values)

# ----------------------------------------------------------------------------------------------------------------------
# Option defaults and updating

def get_option_defaults(method, solver):

    if method in ["crank_nicholson", "explicit_fdm", "implicit_fdm"]:

        option_defaults = {"x_min" : -2.5,
                           "x_max" : 2.5,
                           "dx"    : 0.05,
                           "dtau"  : 0.00125}

        if solver == "iterative" :
            option_defaults["omega"] = 1.1
            option_defaults["tol"]   = 1e-6

    elif method == "monte_carlo":

        option_defaults = {"n"    : 500,
                           "dt"   : 0.00125,
                           "seed" : np.random.randint(1, 1000000)}

    elif method == "closed_form":

        option_defaults = {}

    return option_defaults


def replace_options(new_opts, old_opts):
    '''Replace old options with user defined overrides
    '''

    # If user supplied nothing, return old options
    if new_opts == None:
        return old_opts

    # Make a copy of defaults for updating
    replaced_opts = old_opts

    # Iterate over all combinations, if new = old then update that option
    for new_name,new_value in new_opts.items():
        for old_name, old_value in old_opts.items():
            if old_name == new_name :
                replaced_opts[old_name] = new_value

        # If a new option was specified that is not in the list of possible options, warn it will be ignored
        if new_name not in replaced_opts.keys() :
            print("Ignoring misspecified option: " + new_name)

    return replaced_opts

# ----------------------------------------------------------------------------------------------------------------------
# Validation functions

def validate_option_type(option_type):

    valid_option_types = ["american", "european"]

    if option_type not in valid_option_types :
        sys.exit("Invalid option_type. Valid option types are: " + ', '.join(valid_option_types))

    return


def validate_call_put(call_put):

    valid_call_put = ["call", "put"]

    if call_put not in valid_call_put :
        sys.exit("The call_put argument must be set to one of: " + ', '.join(valid_call_put))


def validate_method_solver_combination(method, solver, option_type):

    valid_methods = ["crank_nicholson", "monte_carlo", "explicit_fdm", "implicit_fdm", "closed_form"]
    valid_solvers = ["direct", "iterative"]

    methods_with_solver = ["crank_nicholson", "implicit_fdm"]

    if(method in valid_methods):

        if((method not in methods_with_solver) & (solver is not None)):
            sys.exit("This method does not require a solver specification. Leave the solver argument blank.")

        if ((method in methods_with_solver) & (solver not in valid_solvers)):
            sys.exit("This method requires a solver, but a valid solver has not been specified. Valid solvers are: " + ', '.join(valid_solvers))

        if((method == "closed_form") & (option_type == "american")):
            sys.exit("Closed form solutions are not available for american options.")

    else:

        sys.exit("Incorrect method. Valid methods are: " + ', '.join(valid_methods))

    return