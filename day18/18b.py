# Make Postfix: -- + > *
# ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
# --> 2 4 + 9 * 6 9 + 8 6 + * 6 + * 2 + 4 + 2 *
# 2 * 4 + 2 + (6 + (6 + 8 * 9 + 6) * (9 * 4 + 2))
# --> 2 4 2 + 6 6 8 + 9 6 + * + 9 4 2 + * * + *
#
# close parens pops op from op stack, pushes op to stack
# op pushes to op stack
# number pops from op stack, pushes op to stack UNLESS '*'
# '*' stays on and only removed for close parens (all stars in parens)
#
# (5 * 4 + 7 + 4 + 8) + 9 * ((5 * 4) + 2 + (6 + 2 + 8 + 7 + 4 + 5)) * 5
# --> 5 4 7 + 4 + 8 + * 9 + 5 4 * 2 + 6 2 + 8 + 7 + 4 + 5 + + 5 *
#
def postfix(line: str) -> list:
    # this splits by spaces but keeps parens in place. Check parens level
    articles = line.split()
    # parens level
    parens = 0
    stack = []
    op = [[]]
    for a in articles:
        if a in ['*', '+']:
            op[-1].append(a)
        elif '(' in a:
            aparens = a.count('(')
            parens += aparens
            for _ in range(aparens):
                op.append([])
            stack.append(int(a[aparens:]))
        elif ')' in a:
            aparens = a.count(')')
            parens -= aparens
            stack.append(int(a[:-aparens]))
            for _ in range(aparens):
                parens_op = op.pop()
                while len(parens_op) > 0:
                    stack.append(parens_op.pop())
            if len(op[-1]) != 0:
                if op[-1][-1] != '*':
                    stack.append(op[-1].pop())
        else:
            stack.append(int(a))
            if len(op[-1]) != 0:
                if op[-1][-1] != '*':
                    stack.append(op[-1].pop())
    lastop = op.pop()
    while len(lastop) > 0:
        stack.append(lastop.pop())
    return stack

def solve(eqn: list) -> int:
    eqn.reverse()
    stack = []
    while len(eqn) > 0:
        action = eqn.pop()
        if action not in ['+', '*']:
            stack.append(action)
        else:
            v1 = stack.pop()
            v2 = stack.pop()
            if action == '+':
                stack.append(v1 + v2)
            else:
                stack.append(v1 * v2)
    #print(stack)
    return(stack.pop())
                
with open('day18.in') as f:
    lines = f.read().splitlines()

stacks = []
for line in lines:
    stacks.append(postfix(line))

eqnsum = 0
for eqn in stacks:
    eqnsum += solve(eqn)
print(f"Day 18 Part 2: { eqnsum }")
