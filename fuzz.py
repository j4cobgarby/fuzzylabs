import matplotlib.pyplot as plt
import numpy as np

class FuzzySet:
    cache = {}
    plot_axis = None

    def __init__(self, axis, f = lambda x : 0):
        self.f = f
        self.plot_axis = axis
    
    def get(self, x):
        if x in self.cache:
            return self.cache[x]
        return self.f(x)

    def store_result(self, key, x):
        val = self.get(x)
        self.cache[key] = val
        return val

    def get_cached(key):
        return self.cache[key]

    def get_cache():
        return self.cache

    def plot(self, xs):
        self.plot_axis.plot(xs, [self.get(x) for x in xs])

    def centroid(self, lo, hi, steps):
        numerator = 0
        denominator = 0

        for x in np.linspace(lo, hi, steps):
            numerator += x * self.get(x)
            denominator += self.get(x)

        if denominator == 0:
            return (lo + hi) / 2
        else:
            return numerator/denominator

class TrapezoidFuzzySet(FuzzySet):
    def trapezoid(self, x):
        if self.a <= x < self.b:
            return (x-self.a) / (self.b-self.a)
        elif self.b <= x <= self.c:
            return 1
        elif self.c < x < self.d:
            return (self.d-x) / (self.d-self.c)
        else:
            return 0

    def __init__(self, axis, a, b, c, d):
        self.plot_axis = axis
        self.xs = [a,b,c,d]
        self.a, self.b, self.c, self.d = a, b, c, d
        self.f = self.trapezoid

    def plot(self):
        super().plot(self.xs)