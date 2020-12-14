import re
import itertools

with open('day14.in') as f:
    lines = f.read().splitlines()

mem = {}
mem_v2 = {}
mask_str = ""
or_mask = 0b0
and_mask = 0b1

for line in lines:
    if line[:4] == "mask":
        # Mask
        maskline = re.match(r"mask = ([0X1]+)", line)
        mask_str = maskline.groups()[0]
        and_mask = int('0b' + ''.join([c for c in mask_str.replace('X','1')]), base=2)
        or_mask = int('0b' + ''.join([c for c in mask_str.replace('X','0')]), base=2)
        float_list = ['0' if c != 'X' else c for c in mask_str]
        float_offsets = []
        num_floats = float_list.count('X')
        indices = [float_list.index('X')]
        for i in range(1, num_floats):
            indices.append(float_list.index('X', indices[-1] + 1))
        for r in range(len(indices)+1):
            comb = itertools.combinations(indices, r)
            for c in comb:
                for i in indices:
                    if i in c:
                        float_list[i] = '1'
                    else:
                        float_list[i] = '0'
                float_offsets.append(int('0b' + ''.join(float_list), base=2))

    else:
        # Mem
        memline = re.match(r"mem\[(\d+)\] = (\d+)", line)
        address = int(memline.groups()[0])
        value = int(memline.groups()[1])
        new_value = value & and_mask | or_mask
        mem[address] = new_value
        for m in float_offsets:
            addr = (address | and_mask) - m
            mem_v2[addr] = value

s = sum(mem.values())
print(f"Day 14 Part 1: { s }")

s = sum(mem_v2.values())
print(f"Day 14 Part 2: { s }")