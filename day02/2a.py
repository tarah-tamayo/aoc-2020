data = [] # List of lists
          # [s,f] = start, finish
          # c = character
          # p = password

with open('day2.in') as f:
    lines = f.read().splitlines()

i = 0
for line in lines:
    entry = line.split(' ')
    entry[0] = [int(x) for x in entry[0].split('-')]
    entry[1] = entry[1][0]
    data.append(entry)
    n = entry[2].count(entry[1])
    if n >= entry[0][0] and n <= entry[0][1]:
        i += 1
        print(entry)
print(i)