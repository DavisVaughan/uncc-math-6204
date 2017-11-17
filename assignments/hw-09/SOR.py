import numpy as np
from numpy.linalg import norm

def sor_solver(A, b, relax_param = 1, tol = 1e-6, max_iter = 100000):
    '''
    This solver solves the linear system of Ax=b using SOR.
    It does so using the iterative approach, and not the matrix approach,
    so there may be room for speed improvements.

    The SOR algorithm is a mix of Gauss Siedel with the previous iteration's value,
    weighted by the relaxation parameter.

    Parameters
    ----------
    A : Numpy 2D matrix
        The 'A' matrix in Ax=b
    b : Numpy 1D array
        The 'b' vector in Ax=b
    relax_param : double
        The relaxation parameter used in SOR. Must be 0 < relax_param < 2.
    tol : double
        The tolerance level for convergence.
    max_iter : int
        The maximum number of iterations before timing out.

    Returns
    -------
    x : Numpy 1D array
        The solution to Ax = b
    '''

    N = b.shape[0]

    # Set up holders for x
    x_last = np.zeros(N)
    x_this = np.zeros(N)

    # A loop to control the total number of iterations
    for iter in range(max_iter):

        # Moving along the x vector
        for i in range(N):

            relax_multiple = relax_param / A[i, i]

            # Set up the 4 pieces needed to calculate x_this[i]
            first  = (1 - relax_param) * x_last[i]
            second = b[i]

            third = 0.0
            for j in range(i):
                third = third + A[i, j] * x_this[j]

            fourth = 0.0
            for j in range(i + 1, N):
                fourth = fourth + A[i, j] * x_last[j]

            x_this[i] = first + relax_multiple * (second - third - fourth)

        # Exit if we have reached convergence, otherwise copy and continue
        if(norm(x_this - x_last) <= tol):
            print("Converged after " + str(iter) + " iterations.")
            return x_this
        else:
            x_last = x_this.copy()

    print("Solution did not converge, returning closest solution:")
    return x_this