import numpy as np
cimport numpy as np
import cython
from cython.view cimport array as cvarray


def thomas_solver(A, b):
    '''
    Solve the linear system Ax = b using the Thomas algorithm.
    This is an efficient solver for tridiagonal A matrices.

    It solves in two steps. A forward step that reduces the system
    in a way that all subdiagonal terms become 0. And a backwards
    step that solves the reduced system from the bottom up.

    Parameters
    ----------
    A : Numpy matrix
        A tridiagonal matrix to solve using the Thomas algorithm
    b : Numpy array
        The right hand side of Ax = b

    Returns
    -------
    x : Numpy array
        The solution to the linear system.
    '''

    [A_reduced, b_reduced] = forward_step(A, b)

    x = backward_step(A_reduced, b_reduced)

    return x

def forward_step(double [:, :] A, double[:] b):

    cdef int N = b.shape[0]
    cdef int i

    cdef double alpha_i, alpha_i_1, beta_i_1, gamma_i

    for i in range(1, N): # 1 to N-1

        alpha_i   = A[i,     i    ]
        alpha_i_1 = A[i - 1, i - 1]
        beta_i_1  = A[i - 1, i    ]
        gamma_i   = A[i,     i - 1]

        # Alter alpha
        A[i, i] = alpha_i - beta_i_1 * (gamma_i / alpha_i_1)

        # Set gamma to 0
        A[i, i-1] = 0

        # Alter b
        b[i] = b[i] - b[i-1] * (gamma_i / alpha_i_1)

    return A, b

def backward_step(double [:, :] A_reduced, double [:] b_reduced):

    cdef int N = b_reduced.shape[0]
    cdef int i
    cdef np.ndarray[np.float64_t, ndim = 1] x = np.zeros(N)

    # Set the last value of x, known
    x[N-1] = b_reduced[N-1] / A_reduced[N-1, N-1]

    cdef double b_i, beta_i, alpha_i

    for i in reversed(range(N-1)): # N-2 to 0

        b_i     = b_reduced[i]
        beta_i  = A_reduced[i, i + 1]
        alpha_i = A_reduced[i, i]

        # Iterate x
        x[i] = (b_i - beta_i * x[i + 1]) / alpha_i

    return x


# Below is the less modern way to do this. Below we access numpy C level types directly
# Above we are using typed memory views

# def forward_step(np.ndarray[np.float64_t, ndim = 2] A, np.ndarray[np.float64_t, ndim = 1] b):
#
#     cdef int N = b.shape[0]
#     cdef int i
#
#     cdef double alpha_i, alpha_i_1, beta_i_1, gamma_i
#
#     for i in range(1, N): # 1 to N-1
#
#         alpha_i   = A[i,     i    ]
#         alpha_i_1 = A[i - 1, i - 1]
#         beta_i_1  = A[i - 1, i    ]
#         gamma_i   = A[i,     i - 1]
#
#         # Alter alpha
#         A[i, i] = alpha_i - beta_i_1 * (gamma_i / alpha_i_1)
#
#         # Set gamma to 0
#         A[i, i-1] = 0
#
#         # Alter b
#         b[i] = b[i] - b[i-1] * (gamma_i / alpha_i_1)
#
#     return A, b
#
#
# def backward_step(np.ndarray[np.float64_t, ndim = 2] A_reduced, np.ndarray[np.float64_t, ndim = 1] b_reduced):
#
#     cdef int N = b_reduced.shape[0]
#     cdef int i
#     cdef np.ndarray[np.float64_t, ndim = 1] x = np.zeros(N)
#
#     # Set the last value of x, known
#     x[N-1] = b_reduced[N-1] / A_reduced[N-1, N-1]
#
#
#     cdef double b_i, beta_i, alpha_i
#
#     for i in reversed(range(N-1)): # N-2 to 0
#
#         b_i     = b_reduced[i]
#         beta_i  = A_reduced[i, i + 1]
#         alpha_i = A_reduced[i, i]
#
#         # Iterate x
#         x[i] = (b_i - beta_i * x[i + 1]) / alpha_i
#
#     return x