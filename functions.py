from Symbols import *
import amath as m
from gmpy2 import mpc, mpfr, mpq, mpz
import gmpy2 as gmp


def clear(var: str) -> bool:
    return True


def N(value, prec=6):
    pre_prec = gmp.get_context().precision
    adj_prec = int((prec * (gmp.log(2) + gmp.log(5))) / gmp.log(2))
    gmp.get_context().precision = adj_prec
    try:
        x, y = getattr(value, 'numerator'), getattr(value, 'denominator')
        return x / y
    except AttributeError:
        return value


functions = dict(print=Function("print", print), clear=Function("clear", clear), N=Function("N", N))  # The functions

for f in m.__all__:
    if callable(getattr(m, f)):
        if not any(word in f for word in ["type", "Type", "Attribute"]):
            functions.update({f: Function(f, getattr(m, f))})

requiredFunctionsFromGMP = ['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'exp', 'exp10', 'exp2',
                            'expm1', 'fac', 'factorial', 'fib', 'fib2', 'floor', 'frexp', 'gamma', 'gcd', 'hypot',
                            'is_bpsw_prp', 'is_euler_prp', 'is_even', 'is_extra_strong_lucas_prp', 'is_fermat_prp',
                            'is_fibonacci_prp', 'is_finite', 'is_inf', 'is_infinite', 'is_integer', 'is_lessgreater',
                            'is_lucas_prp', 'is_nan', 'is_number', 'is_odd', 'is_power', 'is_prime', 'is_regular',
                            'is_selfridge_prp', 'is_signed', 'is_square', 'is_strong_bpsw_prp', 'is_strong_lucas_prp',
                            'is_strong_prp', 'is_strong_selfridge_prp', 'is_unordered', 'is_zero', 'lcm', 'lgamma',
                            'lngamma', 'log10', 'log1p', 'log2', 'root', 'sec', 'sech', 'sign', 'sin', 'sin_cos',
                            'sinh', 'sinh_cosh', 'sqrt', 'tan', 'tanh', ]

for f in requiredFunctionsFromGMP:
    functions.update({f: Function(f, getattr(gmp, f))})
