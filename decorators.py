import time, functools


def profile(f):
    def g(x):
        start = time.time()
        value = f(x)
        end = time.time()
        print("time: {0}s".format(end - start))
        return value

    return g


def memoize(f):
    cache = {}

    def g(x):
        if x not in cache:
            cache[x] = f(x)
        return cache[x]

    return g


def trace(f):
    f.indent = 0

    def g(x):
        print("|  " * f.indent + "|--", f.__name__, x)
        f.indent += 1
        value = f(x)
        print("|  " * f.indent + "|--", "return", repr(value))
        f.indent -= 1
        return value

    return g


def vectorize(f):
    def g(l, *args, **kwargs):
        return [f(x, *args, **kwargs) for x in l]

    return g


def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__

        arg_lst = []
        if args:
            arg_lst.append(", ".join(repr(arg) for arg in args))
        if kwargs:
            pairs = ["%s=%r" % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(", ".join(pairs))
        arg_str = ", ".join(arg_lst)
        if len(arg_str) > 200:
            arg_str = arg_str[:200] + " ..."

        print("[%0.8fs] %s(%s)" % (elapsed, name, arg_str))
        return result

    return clocked


if __name__ == "__main__":

    @trace
    @memoize
    def fib(n):
        if n is 0 or n is 1:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)

    @profile
    def rev(l):
        return l[::-1]

    vlen = vectorize(len)
    vlen(["dog", "bear"])

    vpow = vectorize(pow)
    vpow([4, 5, 6], 3)

    @vectorize
    def square(x):
        return x * x
