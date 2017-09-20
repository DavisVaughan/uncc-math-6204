from gbm_simulator import simulate_gbm
from option_value import price_option
from option_value_exact import price_eur_call, price_eur_put
import numpy as np
import pandas as pd

def main():

    # Parameters
    n          = 1000
    s          = 100
    k          = 100
    #mu         = 0.08 # Only r is used
    r          = .03
    div_yield  = 0.025
    t          = 0
    t_terminal = 1
    dt         = 0.01
    dt2        = 0.001
    sigma      = 0.75
    seed       = 10

    # Sims
    # Should i be using r or mu here? r seems to get me close to the real answer
    gbm_euler_t01     = simulate_gbm(n, s, r, div_yield, t, t_terminal, dt,  sigma, method = "euler",    seed = seed)
    gbm_milstein_t01  = simulate_gbm(n, s, r, div_yield, t, t_terminal, dt,  sigma, method = "milstein", seed = seed)
    gbm_euler_t001    = simulate_gbm(n, s, r, div_yield, t, t_terminal, dt2, sigma, method = "euler",    seed = seed)
    gbm_milstein_t001 = simulate_gbm(n, s, r, div_yield, t, t_terminal, dt2, sigma, method = "milstein", seed = seed)

    # Exact prices
    euro_call = price_eur_call(s, k, r, div_yield, t_terminal, t, sigma)
    euro_put  = price_eur_put(s, k, r, div_yield, t_terminal, t, sigma)

    # Prices
    option_prices =  pd.DataFrame({
        'algorithm'         : ["euler"] * 4 + ["milstein"] * 4,
        'dt'                : [".01", ".01", ".001", ".001"] * 2,
        'option_type'       : ["european"] * 8,
        'call_put'        : ["call", "put"] * 4,
        "exact_option_value": [euro_call, euro_put] * 4,
        'MC_option_value'   : [
            price_option(gbm_euler_t01,     k, r, t_terminal, "call", "european"),
            price_option(gbm_euler_t01,     k, r, t_terminal, "put",  "european"),
            price_option(gbm_euler_t001,    k, r, t_terminal, "call", "european"),
            price_option(gbm_euler_t001,    k, r, t_terminal, "put",  "european"),
            price_option(gbm_milstein_t01,  k, r, t_terminal, "call", "european"),
            price_option(gbm_milstein_t01,  k, r, t_terminal, "put",  "european"),
            price_option(gbm_milstein_t001, k, r, t_terminal, "call", "european"),
            price_option(gbm_milstein_t001, k, r, t_terminal, "put",  "european")
        ]
    })

    option_prices['Absolute error'] = np.abs(option_prices.MC_option_value - option_prices.exact_option_value)

    return option_prices

if __name__ == "__main__":
    print(main())