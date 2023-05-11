import matplotlib.pyplot as plt
from fuzz import FuzzySet, TrapezoidFuzzySet

def main():
    vtall_people = TrapezoidFuzzySet(200, 215, 250, 250)
    tall_people = TrapezoidFuzzySet(175, 190, 250, 250)
    short_people = TrapezoidFuzzySet(0, 0, 160, 175)
    vshort_people = TrapezoidFuzzySet(0, 0, 147, 160)
    avg_people = TrapezoidFuzzySet(165, 170, 180, 185)

    vtall_people.plot()
    tall_people.plot()
    vshort_people.plot()
    short_people.plot()
    avg_people.plot()
    plt.show(block=False)

    while True:
        try:
            name, height = input("Type a name and height in the format 'name, height<cm>': ").split(", ")
            height = float(height)

            print(f"{name} is {height}cm")
            print(f"\
Very tall?.. {vtall_people.store_result(name, height)}\n\
Tall?....... {tall_people.store_result(name, height)}\n\
Average?.... {avg_people.store_result(name, height)}\n\
Short?...... {short_people.store_result(name, height)}\n\
Very short?. {vshort_people.store_result(name, height)}\n")
        except ValueError:
            break

if __name__ == "__main__":
    main()

# Heights:
# Ruth Bader Ginsburg: 152.4
# Rishi Sunak: 170
# Yao Ming: 201
