with open('day13.in') as f:
    time = int(f.readline())
    bus_list = f.readline().split(',')

busses = [int(x) for x in filter(lambda bus: bus != 'x', bus_list)]

next_bus = 0
next_bus_time = time*2
for bus in busses:
    bus_time = bus * (time//bus) + bus
    if bus_time < next_bus_time:
        next_bus_time = bus_time
        next_bus = bus

magic_answer = (next_bus_time - time) * next_bus
print(f"Day 13 Part 1: { magic_answer }")

constraints = []
for offset in range(len(bus_list)):
    if bus_list[offset] != "x":
        bus = int(bus_list[offset])
        constraints.append([bus, offset])

def get_common_mult(blist, bx, cx) -> list:
    """
    solves:
    b0 * m = b1 * n + c1
    returns [m, n]
    """
    b0, s0, m0, _ = blist[0]
    m = 0
    n = 1
    mx = []
    nx = []
    for _ in range(2):
        left = b0 * (s0 + m0 * m) + cx
        right = bx * n
        while left != right:
            if right > left:
                m += 1
            else:
                if n != left // bx:
                    n = left // bx
                else:
                    n += 1
            left = b0 * (s0 + m0 * m) + cx
            right = bx * n
        mx.append(m)
        nx.append(n)
        m += 1
        n += 1
    for bus in blist:
        b1_old = bus[1]
        bus[1] += mx[0] * bus[2]
        bus[2] = mx[1] * bus[2] + b1_old - bus[1]
    blist.append([bx, nx[0], nx[1] - nx[0], cx])
    return blist
        
blist = [[busses[0], 0, 1, 0]] # bus, mult, mult add, constant
for i in range(1, len(constraints)):
    blist = get_common_mult(blist, constraints[i][0], constraints[i][1])
print(f"Day 13 Part 2: { blist[0][0] * blist[0][1] }")