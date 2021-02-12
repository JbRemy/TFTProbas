import numpy as np
from scipy.stats import hypergeom


def build_univariate_transition_matrix(N, n, p):
    """
        N (int): The number of remaining cards in the tier pool
        n (int): The number of remaining desired champion card in the tier pool
        p (float): The tier proba
    """
    size = np.min((10, n + 1))
    transition_matrix = np.zeros((size, size))
    for i in range(size):
        transition_matrix[i, :] = build_univariate_transition_matrix_row(i, N, n, p, size)

    transition_matrix[:, size - 1] = 1 - np.sum(transition_matrix[:, :size - 1], axis=1)

    return transition_matrix


def build_univariate_transition_matrix_row(i, N, n, p, size):
    """
        i (int): row index
        N (int): The number of remaining cards in the tier pool.
        n (int): The number of remaining desired champion card in the tier pool.
        p (float): The tier proba
        size (int): size of the matrix
    """
    row = np.zeros(size)
    for j in range(size):
        if j >= i and j <= i + 5:
            row[j] = hypergeom.pmf(j - i, int((N - i) / p), n - i, 5)

    return row
