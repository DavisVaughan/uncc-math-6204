from call_option_value import V_eur_call, V_eur_put

def main():

    # Parameters
    k          = 100
    s_0        = 100
    t          = 0
    t_terminal = 1
    div_yield  = 0.025
    r          = 0.05
    sigma      = 0.10

    eur_call = V_eur_call(s_0, k, r, div_yield, t_terminal, t, sigma)
    eur_put  = V_eur_put(s_0, k, r, div_yield, t_terminal, t, sigma)

    print()
    print(V_eur_put(s_0, k, r, div_yield, t_terminal, t, sigma))

main()
