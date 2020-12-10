from itertools import combinations

with open('day10.in') as f:
    adapters = sorted([int(x) for x in f])

jolts = 0
# built in adapter is always +3
adapter_diffs = [0,0,1]
for adapter in adapters:
    #print(f"J: { jolts } A: { adapter } D: { adapter_diffs }")
    adapter_diffs[adapter - jolts - 1] += 1
    jolts = adapter
print(f"Day 10 Part 1: { adapter_diffs[0] * adapter_diffs[2] }")

wall = 0
device = jolts+3

adapter_paths = {}
num_paths = {}
adapters.insert(0, wall)
adapters.append(device)
for adapter in adapters:
    if adapter == device:
        adapter_paths[adapter] = []
    else:
        adapter_paths[adapter] = list(filter(lambda a: a - adapter <= 3 and a - adapter > 0, adapters))

num_paths[device] = 1
def do_paths(jolts) -> int:
    paths = 0
    if jolts in num_paths.keys():
        return num_paths[jolts]
    for next_jolts in adapter_paths[jolts]:
        paths += do_paths(next_jolts)
    num_paths[jolts] = paths
    return paths

paths = do_paths(0)
print(f"Day 10 Part 2: { paths }")
