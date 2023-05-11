from fuzz import FuzzySet, TrapezoidFuzzySet
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

'''
RULE 1: IF obstacle close on left AND obstacle far on right THEN steering is HIGH
RULE 2: IF obstacle close on right AND obstacle far on left THEN steering is LOW
RULE 3: IF obstacle close on left AND obstacle close on right THEN steering is HIGH
RULE 4: IF obstacle far on left AND obstacle far on right THEN steering is MID
'''

fig, axs = plt.subplots(3, 4)
plt.ylim([0,1])

obstacle_close = TrapezoidFuzzySet(axs[0,0], 0, 0, 8, 25)
obstacle_far = TrapezoidFuzzySet(axs[0,1], 25, 42, 50, 50)
steering_high = TrapezoidFuzzySet(axs[1,0], 70, 90, 100, 100)
steering_low  = TrapezoidFuzzySet(axs[1,1], 0, 0, 10, 30)
steering_mid = TrapezoidFuzzySet(axs[1,2], 25, 45, 55, 75)

def steer(left, right):
    close_left = obstacle_close.get(left)
    close_right = obstacle_close.get(right)
    far_left = obstacle_far.get(left)
    far_right = obstacle_far.get(right)
    close_left_and_right = min(close_left, close_right)
    far_left_and_right = min(far_left, far_right)
    close_left_and_far_right = min(close_left, far_right)
    close_right_and_far_left = min(close_right, far_left)

    print(f"\
Close left: {close_left}\n\
Close right: {close_right}\n\
Far left: {far_left}\n\
Far right: {far_right}\n\
Close left & right: {close_left_and_right}\n\
Far left & right: {far_left_and_right}")
    
    obstacle_close.plot()
    obstacle_far.plot()
    #plt.vlines([left, right], 0, 1)
    #axs[1.3].vlines([left, right], 0, 1)

    steering_high.plot()
    steering_low.plot()
    steering_mid.plot()

    rule1_set = FuzzySet(axs[2, 0], lambda x : min(close_left_and_far_right, steering_high.get(x)))
    rule2_set = FuzzySet(axs[2, 1], lambda x : min(close_right_and_far_left, steering_low.get(x)))
    rule3_set = FuzzySet(axs[2, 2], lambda x : min(close_left_and_right, steering_high.get(x)))
    rule4_set = FuzzySet(axs[2, 3], lambda x : min(far_left_and_right, steering_mid.get(x)))
    axs[2,0].set_title("Rule 1")
    axs[2,1].set_title("Rule 2")
    axs[2,2].set_title("Rule 3")
    axs[2,3].set_title("Rule 4")
    axs[0,0].set_title("Obst. close")
    axs[0,1].set_title("Obst. far")
    axs[1,0].set_title("Steer high")
    axs[1,1].set_title("Steer low")
    axs[1,2].set_title("Steer mid")

    rule1_set.plot(range(0,100,1))
    rule2_set.plot(range(0,100,1))
    rule3_set.plot(range(0,100,1))
    rule4_set.plot(range(0,100,1))

    output = FuzzySet(axs[1, 3], lambda x : max(rule1_set.get(x), rule2_set.get(x), rule3_set.get(x), rule4_set.get(x)))
    axs[1,3].set_title("Output")
    output.plot(range(0,100,1))

    ctr = output.centroid(0, 100, 200)

    print(left, close_left, right, close_right)
    axs[1,3].axvline(ctr, 0, 1)
    axs[0,0].axvline(left, 0, 1, color='r')
    axs[0,0].axvline(right, 0, 1, color='g')
    axs[0,1].axvline(left, 0, 1, color='r')
    axs[0,1].axvline(right, 0, 1, color='g')

    return ctr

while True:
    for ar in axs:
        for ax in ar:
            ax.clear()
    left, right = [float(s) for s in input("Enter 'left right': ").split()]
    output = steer(left, right)
    print(f"Steering ({left}, {right}): {output }")
    plt.draw()
    plt.pause(0.1)