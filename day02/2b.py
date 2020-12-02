#data = [] # List of lists
          # [s,f] = start, finish
          # c = character
          # p = password

with open('day2.in') as f:
    lines = f.read().splitlines()

i = 0
for line in lines:
    entry = line.split(' ')
    sf = [int(x) for x in entry[0].split('-')]
    c = entry[1][0]
    p = entry[2]
    if p[sf[0]-1] != p[sf[1]-1] and (p[sf[0]-1] == c or p[sf[1]-1] == c):
        print(entry)
        i += 1
print(i)