import numpy as np
from scipy.sparse import spdiags
from scipy.interpolate import interp1d
from solvers import get_solver_function

def pricing_function_fdm(method, solver, option_type, call_put):
    '''Retrieve the FDM pricing function based on user inputs

    This returns the unique pricing function that is some combination of:
    method = Crank Nicholson, Implicit, Explicit
    call_put = call, put
    solver = Thomas, Brennan, SOR, PSOR

    The implementation follows the Prototype Core algorithm

    '''

    # Only thing that changes put/call
    if call_put == "call":
        g = g_call
    elif call_put == "put":
        g = g_put

    # Define theta
    if method == "crank_nicholson":
        theta = 0.5
    elif method == "implicit_fdm":
        theta = 1
    elif method == "explicit_fdm":
        theta = 0

    # Get the correct solver function
    solver_function = get_solver_function(option_type, solver)

    def pricing_function_fdm_implementation(s, k, r, div_yield, sigma, t_terminal, t, x_min, x_max, dx, dtau, omega = None, tol = None):

        lamba = dtau / (dx ** 2)

        # Space steps
        N = int((x_max - x_min) / dx)
        x_vec = x_min + np.arange(N+1) * dx      # 0:N

        # Time steps
        M = int(0.5 * sigma ** 2 * t_terminal * (1 / dtau))
        tau_vec = np.arange(M+1) * dtau          # 0:M

        # Set the tridiagonal matrix A
        size = N-1
        main_diag = 1 + 2 * theta * lamba * np.ones(size)
        sub_diag = - lamba * theta * np.ones(size)
        sup_diag = sub_diag
        A_data = np.array([main_diag, sub_diag, sup_diag])
        tri_set = np.array([0, -1, 1])
        A = spdiags(A_data, tri_set, size, size).toarray()

        # Set up the g grid
        g_grid = np.zeros([N+1, M+1])
        for i in range(M+1):
            g_grid[:, i] = g(x_vec, tau_vec[i], r, div_yield, sigma)

        # Set up the w grid
        w_grid = np.zeros([N+1, M+1])

        # Init w grid with boundaries
        w_grid[:, 0]   = g_grid[:, 0]
        w_grid[0, :]   = g_grid[0, :]
        w_grid[N, :]   = g_grid[N, :]


        # tau loop
        for i in range(M):

            # Set up and fill b_i
            b_i = np.zeros([N - 1, 1]) # 1:(N-1)

            for j in range(1, N): # 1:(N-1)
                b_i[j-1] = w_grid[j, i] + (1-theta) * lamba * (w_grid[j - 1, i] - 2 * w_grid[j, i] + w_grid[j + 1, i])

                if(j == 1):
                    b_i[j-1] = b_i[j-1] + theta * lamba * w_grid[0, i + 1]

                if(j == N - 1):
                    b_i[j-1] = b_i[j-1] + theta * lamba * w_grid[N, i + 1]


            # Pass v, b_i, and A to the solver
            # The result is the w^(i+1) subset of the grid
            # if Iterative solving
            if(omega is not None and tol is not None):

                # Create guess
                # w_i and g_{i+1} are subsets of their grids without the first and last rows
                w_i = w_grid[1:N, i]
                g_ip1 = g_grid[1:N, i + 1]
                v = np.maximum(w_i, g_ip1)

                if(option_type == "european"):
                    # SOR
                    w_grid[1:N, i + 1] = solver_function(A, b_i, guess = v, relax_param = omega, tol = tol)
                else:
                    # PSOR
                    w_grid[1:N, i + 1] = solver_function(A, b_i, g_ip1, guess = v, relax_param = omega, tol = tol)

            # Else directly solving
            else:
                if(option_type == "european"):
                    # Thomas
                    w_grid[1:N, i + 1] = solver_function(A, b_i)
                else:
                    # Brennan
                    g_ip1 = g_grid[1:N, i + 1]
                    w_grid[1:N, i + 1] = solver_function(A, b_i, g_ip1)


        # Convert back to real world variables
        s_vec = k * np.exp(x_vec)
        q     = calc_q(r, sigma)
        q_div = calc_q_div(r, sigma, div_yield)
        tau_max = tau_vec[M]
        option_values = k * np.exp(-0.5 * (q_div - 1) * x_vec - (0.25 * (q_div - 1) ** 2 + q) * tau_max) * w_grid[:, M]

        # Interpolate to find the exact option value
        interp_fun = interp1d(s_vec, option_values)
        option_v = interp_fun(s).item()

        return option_v


    return pricing_function_fdm_implementation

def g_put(x, tau, r, div_yield, sigma):
    q = calc_q(r, sigma)
    q_div = calc_q_div(r, sigma, div_yield)

    g = np.exp( (0.25 * (q_div - 1) ** 2.0 + q) * tau) * \
        np.maximum(np.exp(x/2.0 * (q_div - 1)) - np.exp(x/2.0 * (q_div + 1)), 0)

    return g

def g_call(x, tau, r, div_yield, sigma):
    q = calc_q(r, sigma)
    q_div = calc_q_div(r, sigma, div_yield)

    g = np.exp( (0.25 * (q_div - 1) ** 2.0 + q) * tau) * \
        np.maximum(np.exp(x/2.0 * (q_div + 1)) - np.exp(x/2.0 * (q_div - 1)), 0)

    return g

def calc_q(r, sigma):
    return(2 * r / (sigma**2))

def calc_q_div(r, sigma, div_yield):
    return(2 * (r - div_yield) / (sigma**2))

