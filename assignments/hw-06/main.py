from price_option_trapezoid_method import price_option_trapezoid_method
import pandas as pd
import numpy as np

def main():

    # Parameters
    n          = 1000
    h          = 0.05
    s_0        = 100
    k          = 80
    r          = 0.05
    t_0        = 0
    t_T        = 1
    sigma      = 0.50
    alpha_1    = 2.5
    alpha_2    = 5
    alpha_3    = 10

    alphas = [alpha_1, -alpha_1, alpha_2, -alpha_2, alpha_3, -alpha_3]

    prices = pd.DataFrame({
        'option_price' : np.repeat(0.0, 6),
        'alpha'        : alphas
    })

    i = 0
    for alpha in alphas:
        prices.option_price[i] = price_option_trapezoid_method(s_0, k, r, t_0, t_T, sigma, n, h,  alpha)
        i = i + 1

    return prices


if __name__ == "__main__":
    print(main())