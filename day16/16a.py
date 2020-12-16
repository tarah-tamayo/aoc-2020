import re

with open('day16.in') as f:
    lines = f.read().splitlines()

rule_names = {}
rule_nums = {}
my = []

i = 0
while lines[i] != 'your ticket:':
    # Read rules
    match = re.match(r'([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)', lines[i])
    if match is not None:
        g = match.groups()
        rule_names[g[0]] = [[g[1], g[2]], [g[3], g[4]]]
        for r in rule_names[g[0]]:
            for n in range(int(r[0]), int(r[1]) + 1):
                if n not in rule_nums.keys():
                    rule_nums[n] = []
                rule_nums[n].append(g[0])
    i += 1

i += 1
my = [int(x) for x in lines[i].split(',')]

tickets = [my]
i += 3
while i < len(lines):
    tickets.append([int(x) for x in lines[i].split(',')])
    i += 1

s = 0
i = 0
while i < len(tickets):
    t = tickets[i]
    valid = True
    for n in t:
        if n not in rule_nums.keys():
            s += n
            valid = False
    if not valid:
        tickets.pop(i)
    else:
        i += 1

print(f"Day 16 Part 1: { s }")

fields = [[x for x in rule_names.keys()] for _ in range(len(my))]
resolved = [None for _ in range(len(my))]
for t in tickets:
    # Go through all tickets until all fields are resolved
    for i in range(len(t)):
        # go through each numeric field in the ticket by index
        j = 0
        while j < len(fields[i]):
            # Go through all fields already checked by index
            if fields[i][j] not in rule_nums[t[i]]:
                # if the field is not in the list of rules that match that number, remove it
                fields[i].pop(j)
            else:
                # do not increment j if it was popped
                j += 1
        if len(fields[i]) == 1:
            # If there's only one possible field left, update the resolved list
            resolved[i] = fields[i][0]

i = 0
while i < len(resolved):
    # Go through the resolved list by index. May be resetting a bunch of times
    if resolved[i] is not None:
        for j in range(len(fields)):
            # This length is the same as resolved, but it helps keep i and j separate
            if j != i:
                # the resolved field should not be updated
                if resolved[i] in fields[j]:
                    # if the resolved field is in the fields list, remove it
                    fields[j].pop(fields[j].index(resolved[i]))
                    if len(fields[j]) == 1:
                        #if there's only  one left, resolve it and restart from 0
                        resolved[j] = fields[j][0]
                        i = -1
                        break
    i += 1

mult = 1
for i in range(len(resolved)):
    if 'departure' in resolved[i]:
        mult *= my[i]

print(f"Day 16 Part 2: { mult }")