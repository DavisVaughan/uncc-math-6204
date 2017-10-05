import numpy as np
import scipy.optimize as scipy_opt

def dispatch_pricing_method(call_put = "call", option_type = "european"):
    """Formulate the correct option pricing function from user inputs.

    Called by :py:func:`option_value.price_option`.

    Parameters
    ----------
    call_put : {"call", "put"}, default "call"
        Specifications for the side of the option to price.
    option_type : {"european", "american"}, default "european"
        The type of option to price.

    Returns
    ----------
    pricing_method : function
        A function that prices the specified type of option

    """

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
    """Formulate a function that prices a European option.

    This method discounts the time T values of the payoffs
    calculated from the simulations back to time 0, then takes an average.

    Parameters
    ----------
    call_put_option_price_at_T : function
        A pricing function that prices the value of the option at T. This is different
        depending on whether the option is a call or a put.

    Returns
    ----------
    pricing_method : function
        A function that prices the specified type of option

    See also
    ----------
    american

    """

    # Create the European pricing function to return
    def european_pricing_method(s, k, r, T):
        """Price a european option from simulated values.

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

        Returns
        ----------
        v_0 : double
            The price of the European option

        See also
        ----------
        option_value.european

        """

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
    """Formulate a function that prices an American option.

    This method prices the option using a regression method.
    The continuation value at time t is calculated by regressing
    the discounted value of the option at time t+1 on the
    price at time t. The continuation value is then compared to
    the value of the payoff at time t, and the max is chosen as the
    value of the option at t.

    Notably, this is regression method 2, which only considers points that are
    in the money when running the regression and making updating decisions.

    The regression method is well documented
    `here <https://people.math.ethz.ch/~hjfurrer/teaching/LongstaffSchwartzAmericanOptionsLeastSquareMonteCarlo.pdf>`_.

    Parameters
    ----------
    call_put_option_price_at_T : function
        A pricing function that prices the value of the option at T. This is different
        depending on whether the option is a call or a put.

    Returns
    ----------
    pricing_method : function
        A function that prices the specified type of option.

    See also
    ----------
    european

    """

    def american_pricing_method(s, k, r, T):
        """Price an american option from simulated values.

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

        Returns
        ----------
        v_0 : double
            The price of the American option

        See also
        ----------
        option_value.american

        """

        dt  = T / float(s.shape[1] - 1)
        g   = np.zeros(s.shape)
        tau = np.zeros(s.shape[0]) + g.shape[1] - 1

        # At i = M = T, use value at T
        g[:, -1] = call_put_option_price_at_T(s[:, -1], k)

        # Basis function for continuation value
        def basis_func_C(x, a0, a1, a2, a3):
            return a0 + (a1 * x) + (a2 * x ** 2) + (a3 * x ** 3)

        # Iterate backwards
        iteration = (np.arange(g.shape[1] - 2) + 1)[::-1]

        for i in iteration:

            # x and y values for each regression
            s_ik = s[:, i]
            yvalues = np.exp(-r * (tau - i) * dt) * g[:, i + 1]

            # Calculate the value of the option if this was time T
            s_ik_v = call_put_option_price_at_T(s_ik, k)

            # Restrict x and y to in the money points. Payoff > 0
            itm_indices = s_ik_v > 0
            itm_s_ik    = s_ik[itm_indices]
            itm_yvalues = yvalues[itm_indices]

            # Fit the 3rd ordered curve
            C_fit = scipy_opt.curve_fit(basis_func_C, itm_s_ik, itm_yvalues)
            params = C_fit[0]

            # Use the optimal parameters
            C_hat = basis_func_C(s_ik, *params)

            # For ALL values, which satisfy the update condition?
            update_indices = s_ik_v >= C_hat

            # Logical AND operation to find:
            # which values are in the money and satisfy the update condition?
            itm_update_indices = np.logical_and(itm_indices, update_indices)

            # Copy g back a column
            g[:, i] = g[:, i + 1]

            # For the values of g that need to be updated, do the update
            g[itm_update_indices, i] = s_ik_v[itm_update_indices]

            # For values of tau that need to be updated, do the update
            tau[itm_update_indices] = i

        # Discount time 1 to time 0, taking into account the correct number of discounts to use
        g[:, 0] = np.exp(-r * tau * dt) * g[:, 1]

        # Average the paths and take the max to get the Monte Carlo result
        C_0      = np.mean(g[:, 0])
        payoff_0 = call_put_option_price_at_T(s[0,0], k)

        v_0 = max(C_0, payoff_0)

        return v_0

    return american_pricing_method


def option_price_at_T_call(s_T, k):
    """Return a function that calculates the value of a call option at time T

    The value of the option is calculated as, :math:`max(S_T - K, 0)`

    Parameters
    ----------
    s_T : vector
        The simulated paths at time T
    k : double
        The strike price for the option.

    Returns
    ----------
    v_T : vector
        The price of the call option at time T

    See also
    ----------
    option_price_at_T_put

    """

    v_T = np.maximum(s_T - k, 0)

    return v_T


def option_price_at_T_put(s_T, k):
    """Return a function that calculates the value of a put option at time T

    Parameters
    ----------
    s_T : vector
        The simulated paths at time T
    k : double
        The strike price for the option.

    Returns
    ----------
    v_T : vector
        The price of the put option at time T

    See also
    ----------
    option_price_at_T_call

    """

    v_T = np.maximum(k - s_T, 0)

    return v_T