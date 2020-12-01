import sys

expenses = []
with open('day1.in') as f:
    for line in f:
        expenses.append(line)

for i in range(0, len(expenses)-1):
    ex1 = int(expenses[i])
    for j in range(i, len(expenses)):
        ex2 = int(expenses[j])
        if ex1 + ex2 == 2020:
            print(f"{ ex1 } + { ex2 } = { ex1 + ex2 }")
            print(f"{ ex1 } * { ex2 } = { ex1 * ex2 }")
            sys.exit()