from option_value import price_eur_call, price_eur_put
import pandas as pd

def main():

    # Parameters
    k          = 100
    s_0        = 100
    t          = 0
    t_terminal = 1
    div_yield  = 0.025
    r          = 0.05
    sigma      = np.linspace(.1, 1, 10)

    # Calculate call and put values
    eur_call = price_eur_call(s_0, k, r, div_yield, t_terminal, t, sigma)
    eur_put  = price_eur_put(s_0, k, r, div_yield, t_terminal, t, sigma)

    # Structure as data frame
    result = pd.DataFrame({
        'Volatility' : sigma,
        'Euro Call'  : eur_call,
        'Euro Put'   : eur_put
    })

    return result


# Executing main
main()

