from simpful import *

fs = FuzzySystem()

obs_close   = FuzzySet(points=[[0.,1.],[8.,1.],[25.,0.],[50.,0.]], term="close")
obs_far     = FuzzySet(points=[[0.,0.],[25.,0.],[42.,1.],[50.,0.]], term="far")
steer_right = FuzzySet(points=[[0.,0.],[70.,0.],[90.,1.],[100.,1.]], term="right")
steer_left  = FuzzySet(points=[[0.,1.],[10.,1.],[30.,0.],[100.,0.]], term="left")
steer_mid   = FuzzySet(points=[[0.,0.],[25.,0],[45.,1.],[55.,1.],[75.,0.],[100.,0.]], term="mid")

fs.add_linguistic_variable("left_obstacle", LinguisticVariable([obs_close,obs_far]))
fs.add_linguistic_variable("right_obstacle", LinguisticVariable([obs_close,obs_far]))
fs.add_linguistic_variable("steering", LinguisticVariable([steer_left, steer_mid, steer_right]))

fs.add_rules([
    "IF (left_obstacle IS close) AND (right_obstacle IS far) THEN (steering IS right)",
    "IF (right_obstacle IS close) AND (left_obstacle IS far) THEN (steering IS left)",
    "IF (right_obstacle IS close) AND (left_obstacle IS close) THEN (steering IS right)",
    "IF (right_obstacle IS far) AND (left_obstacle IS far) THEN (steering IS mid)",
])

while True:
    left, right = [float(s) for s in input("<left, right>: ").split(",")]
    fs.set_variable("left_obstacle", left)
    fs.set_variable("right_obstacle", right)
    steer = fs.inference()
    print(f"Steering for <{left}, {right}> = {steer['steering']}.")
