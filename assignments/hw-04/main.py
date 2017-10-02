from option_value import price_option
from gbm_simulator import simulate_gbm
import pandas as pd

def main():

    # Parameters
    n          = 1000
    s          = 100
    k          = 100
    #mu        = 0.08 # Only r is used
    r          = .03
    div_yield  = 0.025
    t          = 0
    t_terminal = 1
    dt         = 0.01
    dt2        = 0.001
    sigma      = 0.75
    seed       = 123

    # GBM Sims
    gbm_euler_t01  = simulate_gbm(n, s, r, div_yield, t, t_terminal, dt,  sigma, method = "euler", seed = seed)
    gbm_euler_t001 = simulate_gbm(n, s, r, div_yield, t, t_terminal, dt2, sigma, method = "euler", seed = seed)

    # Option prices
    am_call_t01  = price_option(gbm_euler_t01,  k, r, t_terminal, call_put = "call", option_type = "american")
    am_put_t01   = price_option(gbm_euler_t01,  k, r, t_terminal, call_put = "put",  option_type = "american")
    am_call_t001 = price_option(gbm_euler_t001, k, r, t_terminal, call_put = "call", option_type = "american")
    am_put_t001  = price_option(gbm_euler_t001, k, r, t_terminal, call_put = "put",  option_type = "american")

    # Price dataframe
    option_prices = pd.DataFrame({
        'dt': [".01", ".01", ".001", ".001"],
        'option_type': ["american"] * 4,
        'call_put': ["call", "put"] * 2,
        'MC_option_value': [
            am_call_t01,
            am_put_t01,
            am_call_t001,
            am_put_t001
        ]
    })

    return option_prices


if __name__ == "__main__":
    print(main())