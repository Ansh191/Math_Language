import amath as m
import re
from Symbols import *
from functions import *
from gmpy2 import mpz, mpq, mpfr, mpc
import gmpy2 as gmp
import time

gmp.get_context().allow_complex = True

n = 1  # iterations

outputs = [None]  # all outputs
variables = {"Dir": functions.keys(), "%": outputs[-1], "time": True}  # all variables, % is last output
result = None  # final result of evaluation


def remove_whitespace(txt: str) -> str:
    parts = re.split(r"""("[^"]*"|'[^']*')""", txt)
    parts[::2] = map(lambda s: "".join(s.split()), parts[::2])  # outside quotes
    return "".join(parts)


def get_function(txt: str) -> object:
    for f in functions:
        if f in txt:  # find function in expression
            opos = txt.find(f)
            if opos != 0:
                continue
            pos = txt.find(f) + len(f)  # pos of character immediately after function name
            try:
                ch = txt[pos]
            except IndexError:
                return f  # if function alone
            if ch == '[':
                end_index = txt.find(']')
                if end_index == -1:
                    raise SyntaxError("missing ']' after {0}".format(f))
                start_index = txt.find(f)
                text_f = txt[start_index:end_index + 1]  # complete function usage
                try:
                    if txt[end_index + 1] in ['+', '-', '*', '/']:
                        return None
                except IndexError:
                    return f, text_f, txt.replace(text_f, '')  # function, function usage, remaining

    return None


def get_args(txt: str, f: str) -> list:
    pos = txt.find(f) + len(f)
    end_pos = txt.find(']')
    args = txt[pos + 1: end_pos]
    return args.split(',')


def evaluate(txt: str) -> object:
    global result
    num = False
    try:
        f, full_f, remaining = get_function(txt)
    except (ValueError, TypeError):
        if get_function(txt) is None:
            num = True
        else:
            return get_function(txt)

    # print(num)

    if not num:
        args = get_args(full_f, f)
        eval_args = []
        for arg in args:
            eval_args.append(evaluate(arg))
        return evaluate(str(functions[f](*eval_args)))
    elif num:

        try:
            txt = mpz(txt)
        except ValueError:
            try:
                txt = mpq(txt)
            except ValueError:
                try:
                    txt = mpc(txt)
                except ValueError:
                    if str(bool(txt)) == txt:
                        txt = bool(txt)
        try:
            if '=' in txt:
                return assign(txt)
            if '+' in txt:
                return binary_add(txt)
            if '-' in txt:
                return binary_sub(txt)
            if '*' in txt:
                return binary_mul(txt)
            if '/' in txt:
                return binary_div(txt)
        except TypeError:
            pass
        # print(txt)
        return txt


def assign(txt: str) -> object:
    l = txt.split("=")
    eval_l = []
    for side in l:
        eval_l.append(evaluate(side))
    var = eval_l[0]
    del eval_l[0]
    if isinstance(var, float) or isinstance(var, complex):
        raise SyntaxError("can't assign " + str(eval_l[0]) + " to " + str(var))
    elif '%' in var or var=="Dir":
        raise SyntaxError("can't assign " + str(eval_l[0]) + " to " + str(var))

    variables[var] = eval_l[0]

    return eval_l[0]


def binary_div(txt: str) -> object:
    l = txt.split("/")
    eval_l = []
    for side in l:
        eval_l.append(evaluate(side))

    total = eval_l[0]
    del eval_l[0]
    for side in eval_l:
        total /= side

    return total


def binary_mul(txt: str) -> object:
    l = txt.split("*")
    eval_l = []
    for side in l:
        eval_l.append(evaluate(side))
    total = eval_l[0]
    del eval_l[0]
    for side in eval_l:
        total *= side

    return total


def binary_add(txt: str) -> object:
    l = txt.split("+")
    eval_l = []
    for side in l:
        eval_l.append(evaluate(side))
    total = eval_l[0]
    del eval_l[0]
    for side in eval_l:
        total += side

    return total


def binary_sub(txt: str) -> object:
    l = txt.split("-")
    eval_l = []
    for side in l:
        eval_l.append(evaluate(side))
    total = eval_l[0]
    del eval_l[0]
    for side in eval_l:
        total -= side

    return total


def main(i: str):
    global n
    global result
    if variables["time"]:
        initial = time.perf_counter()
    n += 1
    i = remove_whitespace(i)
    if i == "exit":
        return True
    for variable in variables:
        if variable in i:
            try:
                l_before = i.find(variable) - 1
                i[l_before]
            except IndexError:
                l_before = None
            try:
                l_after = i.find(variable) + len(variable)
                i[l_after]
            except IndexError:
                l_after = l_before + 1
            if (i[l_before] in ['(', variable[-1]], '+', '-', '/', '*') \
                    and (i[l_after] in [')', ' ', variable[0], '*', '+', '/', '-']):
                i = i.replace(variable, str(variables[variable]))
    try:
        result = evaluate(i)
    except Exception as ex:
        result = f'{type(ex).__name__}: {ex}'
        # raise
    print(result)
    if variables["time"]:
        end = time.perf_counter()
        print("Elapsed time = {:.6f} microseconds".format((end - initial)*10**6))

    outputs.append(result)
    variables['%{0}'.format(n)] = result
    variables['%'] = result


if __name__ == '__main__':
    import cProfile
    pr = cProfile.Profile()
    pr.enable()
    while True:
        x = input("{0}: ".format(n))
        if main(x):
            break

    pr.disable()
    pr.dump_stats('profile.profile')
