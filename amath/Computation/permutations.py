from .Basic import fac
import gmpy2 as gmp


def comb(n, k):
    n = float(n)
    k = float(k)
    if k > n:
        return 0
    if k < 0:
        return 0
    return float(fac(n)) / float(fac(k) * fac(n - k))


def perm(n, k):
    # k = float(k)
    # n = float(n)
    # if k > n:
    #     return 0
    # if k < 0:
    #     raise ValueError("k must be non-negative")
    # return float(fac(n)) / float(fac(n - k))
    if k > n:
        return 0
    if k < 0:
        raise ValueError("k must be non-negative")
    return gmp.fac(n) / (fac(k) * fac(n - k))
