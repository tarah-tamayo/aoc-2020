from itertools import combinations

preamble_length = 25

with open('day9.in') as f:
    values = [int(x) for x in f]

for i in range(preamble_length, len(values)):
    preamble = values[i-preamble_length:i]
    sums = set([sum(x) for x in combinations(preamble, 2)])

    if values[i] not in sums:
        print(f"Day 9 Part 1: { values[i] } is not in preamble sums.")
        invalid = values[i]
        invalid_idx = i

sumstart = 0
for i in range(invalid_idx):
    while sum(values[sumstart:i+1]) > invalid:
        sumstart += 1
    if sum(values[sumstart:i+1]) == invalid:
        minval = min(values[sumstart:i+1])
        maxval = max(values[sumstart:i+1])
        print(f"Day 9 Part 2: { minval } + { maxval } = { minval + maxval }")