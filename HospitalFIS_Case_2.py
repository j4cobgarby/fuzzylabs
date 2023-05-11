from juzzyPython.generic.Tuple import Tuple
from juzzyPython.generic.Output import Output
from juzzyPython.generic.Input import Input
from juzzyPython.generic.Plot import Plot
from juzzyPython.type1.system.T1_Rule import T1_Rule
from juzzyPython.type1.system.T1_Antecedent import T1_Antecedent
from juzzyPython.type1.system.T1_Consequent import T1_Consequent
from juzzyPython.type1.system.T1_Rulebase import T1_Rulebase
from juzzyPython.type1.sets.T1MF_Gaussian import T1MF_Gaussian
from juzzyPython.type1.sets.T1MF_Trapezoidal import T1MF_Trapezoidal
from juzzyPython.type1.sets.T1MF_Triangular import T1MF_Triangular

import matplotlib.pyplot as pl

class PatientUrgencyFLS:
    def __init__(self):
        self.headache = Input("headache", Tuple(0,100), inputMF=T1MF_Gaussian("headache_input_mf", 0, 5))
        self.temperature = Input("temperature", Tuple(0, 60), inputMF=T1MF_Gaussian("temperature_input_mf", 0, 0.5))
        self.age = Input("age", Tuple(0, 130), inputMF=T1MF_Gaussian("age_input_mf", 0, 0.5))

        self.urgency = Output("urgency", Tuple(0,100))

        # self.plot = Plot()

        h_very_severe  = T1_Antecedent(T1MF_Gaussian("mf_very_severe", 84.3, 9.9), self.headache, "very_severe")
        h_severe       = T1_Antecedent(T1MF_Gaussian("mf_severe", 67.5, 13.5), self.headache, "severe")
        h_moderate     = T1_Antecedent(T1MF_Gaussian("mf_moderate", 29.2, 13.8), self.headache, "moderate")
        h_mild         = T1_Antecedent(T1MF_Gaussian("mf_mild", 13.9, 8.0), self.headache, "mild")
        h_none         = T1_Antecedent(T1MF_Gaussian("mf_none", 1.4, 3.8), self.headache, "none")
        h_mfs = [h_very_severe.getMF(), h_severe.getMF(), h_moderate.getMF(), h_mild.getMF(), h_none.getMF()]

        t_normal = T1_Antecedent(T1MF_Gaussian("mf_normal", 37.04, 2 * 0.36), self.temperature, "normal")
        t_hypothermia = T1_Antecedent(T1MF_Trapezoidal("mf_hypothermia", [0,0,32,35]), self.temperature, "hypothermia")
        t_hyperpyrexia = T1_Antecedent(T1MF_Trapezoidal("mf_hyperpyrexia", [38.3, 40, 60, 60]), self.temperature, "hyperpyrexia")
        t_mfs = [t_normal.getMF(), t_hypothermia.getMF(), t_hyperpyrexia.getMF()]

        a_child = T1_Antecedent(T1MF_Trapezoidal("mf_child", [0, 0, 10, 18]), self.age, "child")
        a_grown_up = T1_Antecedent(T1MF_Trapezoidal("mf_grown-up", [10, 18, 70, 85]), self.age, "grown-up")
        a_elderly = T1_Antecedent(T1MF_Trapezoidal("mf_elderly", [70, 85, 130, 130]), self.age, "elderly")
        a_mfs = [a_child.getMF(), a_grown_up.getMF(), a_elderly.getMF()]

        urgency_terms_names = ["very_low", "low", "moderate", "high", "very_high"]
        spacing = 100.0 / (len(urgency_terms_names)-1)

        # Generate equally spaced triangular terms for urgency
        u_terms = {nm :
            T1_Consequent(T1MF_Triangular("mf_" + nm, 
                (i-1) * spacing, i * spacing, (i+1) * spacing), 
                self.urgency, nm
            )

            for i, nm in enumerate(urgency_terms_names)
        }
        u_mfs = [v.getMF() for v in u_terms.values()]

        self.rb = T1_Rulebase()

        self.rb.addRule(T1_Rule([t_hypothermia], u_terms["very_high"]))
        self.rb.addRule(T1_Rule([t_hyperpyrexia], u_terms["very_high"]))

        self.rb.addRule(T1_Rule([h_severe], u_terms["moderate"]))
        self.rb.addRule(T1_Rule([h_very_severe], u_terms["high"]))

        self.rb.addRule(T1_Rule([t_normal, h_none], u_terms["very_low"]))

        self.rb.addRule(T1_Rule([a_child, h_severe], u_terms["very_high"]))
        self.rb.addRule(T1_Rule([a_elderly, h_severe], u_terms["very_high"]))
        self.rb.addRule(T1_Rule([a_child, h_very_severe], u_terms["very_high"]))
        self.rb.addRule(T1_Rule([a_elderly, h_very_severe], u_terms["very_high"]))

        # Set both to Minimum operator
        self.rb.setImplicationMethod(1)
        self.rb.setInferenceMethod(1)

        print(self.rb.toString())

        # self.plotMFs("Headache MFs", h_mfs, self.headache.getDomain(), 100)
        # self.plotMFs("Temperature MFs", t_mfs, self.temperature.getDomain(), 100)
        # self.plotMFs("Age MFs", a_mfs, self.age.getDomain(), 100)
        # self.plotMFs("Urgency MFs", u_mfs, self.urgency.getDomain(), 100)
        # self.plot.show()

    def urgency_of(self, age, temperature, headache):
        self.age.setInput(age)
        self.temperature.setInput(temperature)
        self.headache.setInput(headache)
        
        return self.rb.evaluate(1)[self.urgency]

    def plotMFs(self,name,sets,xAxisRange,discretizationLevel):
        """Plot the lines for each membership function of the sets"""
        self.plot.figure()
        self.plot.title(name)
        for i in range(len(sets)):
            self.plot.plotMF(name.replace("Membership Functions",""),sets[i].getName(),sets[i],discretizationLevel,xAxisRange,Tuple(0.0,1.0),False)
        self.plot.legend()

if __name__ == "__main__":
    fls = PatientUrgencyFLS()

    cases_adult_healthytemp = [
        [30, 37.04, x] for x in range(0, 100, 5)
    ]

    cases_elderly_healthytemp = [
        [100, 37.04, x] for x in range(0, 100, 5)
    ]

    cases_adult_mild_headache = [
        [26, x, 14.0] for x in range(30, 45, 1)
    ]

    cases_child_mild_headache = [
        [26, x, 14.0] for x in range(30, 45, 1)
    ]
    
    xs = []
    ys = []

    for c in cases_adult_healthytemp:
        xs.append(c[2])
        ys.append(fls.urgency_of(*c))
    pl.scatter(xs, ys, c="red", marker="x", label="Age=30")

    xs = []
    ys = []

    for c in cases_elderly_healthytemp:
        xs.append(c[2])
        ys.append(fls.urgency_of(*c))
    pl.scatter(xs, ys, c="blue", marker="x", label="Age=100")

    pl.xlabel("Headache Severity")
    pl.ylabel("Urgency")
    pl.title("The effect of headache severity. Temperature = 37.04")
    pl.legend()

    pl.show()

    print(fls.urgency_of(20, 37.04, 0))