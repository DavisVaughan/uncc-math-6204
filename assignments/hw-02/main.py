from gbm_simulator import gbm
import numpy as np
import matplotlib.pyplot as plt

def main():

    # Parameters
    n          = 5
    s          = 100
    mu         = .1
    div_yield  = .025
    t          = 0
    t_terminal = 1
    dt         = .001
    sigma      = .2
    seed       = 100

    # Sims
    gbm_paths = gbm(n, s, mu, div_yield, t, t_terminal, dt, sigma, seed)

    # Plot vars needed
    t_steps = int((t_terminal - t) / dt)
    index = np.linspace(0, t_steps, t_steps + 1)

    # Build and show plot
    plt.figure()
    [plt.plot(index, gbm_paths[i, :]) for i in range(0, n)]
    plt.title('5 Sample Paths of GBM')
    plt.xlabel('time (t)')
    plt.ylabel('S(t)')
    plt.show()

    # Print it
    return gbm_paths


# Main will not be executed during `import main`
# Main will be executed when `python main.py` is run from terminal
if __name__ == "__main__":
    print(main())