from gbm_simulator import simulate_gbm
import numpy as np
import scipy.optimize as scipy_opt

def pricing_function_monte_carlo(option_type, option_price_at_T):
    '''Retrieve the Monte Carlo pricing function for a european/american call/put

    American options are priced using the Regression 2 Method
    European options are priced using GBM simulations discounted back to t=0
    '''

    if option_type == "european":

        def pricing_function_monte_carlo_european(s, k, r, div_yield, sigma, t_terminal, t, n, dt, seed):

            s = simulate_gbm(n, s, r, div_yield, t, t_terminal, dt, sigma, method = "euler", seed = seed)

            s_T = s[:, -1]

            # Apply call / put option value at T
            v_T = option_price_at_T(s_T, k)

            # Discount
            v_0 = np.exp(- r * t_terminal) * np.mean(v_T)

            return v_0

        return pricing_function_monte_carlo_european

    elif option_type == "american":

        def pricing_function_monte_carlo_american(s, k, r, div_yield, sigma, t_terminal, t, n, dt, seed):

            s = simulate_gbm(n, s, r, div_yield, t, t_terminal, dt, sigma, method = "euler", seed=seed)

            dt = t_terminal / float(s.shape[1] - 1)
            g = np.zeros(s.shape)
            tau = np.zeros(s.shape[0]) + g.shape[1] - 1

            # At i = M = T, use value at T
            g[:, -1] = option_price_at_T(s[:, -1], k)

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
                s_ik_v = option_price_at_T(s_ik, k)

                # Restrict x and y to in the money points. Payoff > 0
                itm_indices = s_ik_v > 0
                itm_s_ik = s_ik[itm_indices]
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
            C_0 = np.mean(g[:, 0])
            payoff_0 = option_price_at_T(s[0, 0], k)

            v_0 = max(C_0, payoff_0)

            return v_0

        return pricing_function_monte_carlo_american

