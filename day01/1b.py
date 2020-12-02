import sys

expenses = []
with open('day1.in') as f:
    for line in f:
        expenses.append(line)

for i in range(0, len(expenses)-1):
    ex1 = int(expenses[i])
    for j in range(i, len(expenses)):
        ex2 = int(expenses[j])
        if ex1 + ex2 < 2020:
            for k in range(j+1, len(expenses)):
                ex3 = int(expenses[k])
                if ex1 + ex2 + ex3 == 2020:
                    print(f"{ ex1 } + { ex2 } + { ex3 } = { ex1 + ex2 + ex3 }")
                    print(f"{ ex1 } * { ex2 } * { ex3 } = { ex1 * ex2 * ex3 }")
                    sys.exit()