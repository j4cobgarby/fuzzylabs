#!/usr/bin/python
import numpy as np
from simpful import *

fs = FuzzySystem(show_banner=False)

class Gausstep_MF(MF_object):
    def __init__(self, mu, sigma, gaussian_side):
        self._mu = mu
        self._sigma = sigma
        self._gaussian_side = gaussian_side

        if gaussian_side not in ["left", "right"]:
            print("WARNING: gaussian_side should be left or right.")
        if sigma <= 0: 
            print("WARNING: sigma should be positive.")

    def _gaussian(self, x, mu, sig):
        return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

    def _execute(self, x):
        if self._gaussian_side == "left" and x < self._mu:
            return self._gaussian(x, self._mu, self._sigma)
        elif self._gaussian_side == "right" and x > self._mu:
            return self._gaussian(x, self._mu, self._sigma)
        else:
            return 1.0

class GausstepFuzzySet(FuzzySet):
    def __init__(self, mu, sigma, gaussian_side, term):
        gausstep = Gausstep_MF(mu, sigma, gaussian_side)
        super().__init__(function=gausstep, term=term)

    def set_params(self, mu=None, sigma=None, gaussian_side=None):
        if mu is not None: self._funpointer._mu = mu
        if sigma is not None: self._funpointer._sigma = sigma
        if gaussian_side is not None: self.funpointer._gaussian_side = gaussian_side

# Numerical data from B. Aicher et al., 2011
fs.add_linguistic_variable("headache", LinguisticVariable(
[
    # GausstepFuzzySet(84.3, 9.9, "left", "very_severe"),
    # GausstepFuzzySet(67.5, 13.5, "left", "severe"),
    # GausstepFuzzySet(29.2, 13.8, "left", "moderate"),
    # GausstepFuzzySet(13.9, 8, "left", "mild"),
    # GausstepFuzzySet(1.4, 3.8, "right", "none"),

    # GaussianFuzzySet(mu=98.7, sigma=4.9, term="most_severe"),
    GaussianFuzzySet(mu=84.3, sigma=9.9,  term="very_severe"),
    GaussianFuzzySet(mu=67.5, sigma=13.5, term="severe"),
    GaussianFuzzySet(mu=29.2, sigma=13.8, term="moderate"),
    GaussianFuzzySet(mu=13.9, sigma=8.0,  term="mild"),
    GaussianFuzzySet(mu=1.4,  sigma=3.8,  term="none"),
], universe_of_discourse=[0,100]))

temp_mean = 37.04
temp_sd = 0.36
fs.add_linguistic_variable("temperature", LinguisticVariable(
[
    GaussianFuzzySet(temp_mean, 2 * temp_sd, "normal"),

    TrapezoidFuzzySet(0, 0, 32, 35, "hypothermia"),
    TrapezoidFuzzySet(38.3, 40, 60, 60, "hyperpyrexia"),
], universe_of_discourse=[0, 60]))

fs.add_linguistic_variable("age", LinguisticVariable(
[
    TrapezoidFuzzySet(0, 0, 10, 18, "child"),
    TrapezoidFuzzySet(10, 18, 70, 85, "grown-up"),
    TrapezoidFuzzySet(70, 85, 130, 130, "elderly"),
], universe_of_discourse=[0,130]))

fs.add_linguistic_variable("urgency", AutoTriangle(
    n_sets=5,
    terms=["very_low", "low", "moderate", "high", "very_high"],
    universe_of_discourse=[0,100]
))

# fs.add_linguistic_variable("urgency", LinguisticVariable(
# [
#     TrapezoidFuzzySet(0, 0, 10, 25, "very_low"),
#     TrapezoidFuzzySet(10, 25, 35, 50, "low"),
#     TrapezoidFuzzySet(40, 45, 55, 60, "moderate"),
#     TrapezoidFuzzySet(50, 65, 75, 90, "high"),
#     TrapezoidFuzzySet(75, 90, 100, 100, "very_high"),
# ], universe_of_discourse=[0,100]))

## Rules

# fs.add_rules([
#     "IF (temperature IS hypothermia) OR (temperature IS hyperpyrexia) THEN (urgency IS very_high)",

#     "IF (headache IS severe) THEN (urgency IS moderate)",
#     "IF (headache IS very_severe) THEN (urgency IS high)",

#     "IF (temperature IS normal) AND (headache IS none) THEN (urgency IS very_low)",

#     "IF ((age IS child) OR (age IS elderly)) AND ((headache IS severe) OR\
# (headache IS very_severe)) THEN (urgency IS very_high)",
# ])

fs.add_rules([
    "IF (temperature IS hypothermia) THEN (urgency IS very_high)",
    "IF (temperature IS hyperpyrexia) THEN (urgency IS very_high)",
    "IF (headache IS severe) THEN (urgency IS moderate)",
    "IF (headache IS very_severe) THEN (urgency IS high)",
    "IF (temperature IS normal) AND (headache IS none) THEN (urgency IS very_low)",
    "IF (age IS child) AND (headache IS severe) THEN (urgency IS very_high)",
    "IF (age IS elderly) AND (headache IS severe) THEN (urgency IS very_high)",
    "IF (age IS child) AND (headache IS very_severe) THEN (urgency IS very_high)",
    "IF (age IS elderly) AND (headache IS very_severe) THEN (urgency IS very_high)",
])

# fs.plot_variable("headache")
# fs.plot_variable("temperature")
# fs.plot_variable("age")
fs.plot_variable("urgency")

# fs.produce_figure(max_figures_per_row=2)

# test_values = [
# [22, 36.5, 0],
# [25, 34.5, 0],
# [10, 32, 0],
# [8, 30, 0],
# [30, , 
# ]

while True:
    age, temp, headache = [float(s) for s in input("<age>, <temp>, <headache> >> ").split(",")]
    fs.set_variable("age", age)
    fs.set_variable("temperature", temp)
    fs.set_variable("headache", headache)
    # fs.set
    inf = fs.inference()
    urgency = inf["urgency"]
    print(f"Urgency is {urgency}")
    # fs.produce_figure(max_figures_per_row=2, element_dict={
    #     "age": age,
    #     "temperature": temp,
    #     "headache": headache,
    #     "urgency": urgency,
    # }, outputfile=str(age)+","+str(temp)+","+str(headache)+".png")

# top=0.948,
# bottom=0.202,
# left=0.046,
# right=0.99,
# hspace=0.2,
# wspace=0.2