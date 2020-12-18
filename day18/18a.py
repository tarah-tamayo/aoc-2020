# Make Postfix:
# ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
# --> 2 4 + 9 * 6 9 + 8 * 6 + * 6 + 2 + 4 + 2 *
# 2 * 4 + 2 + (6 + (6 + 8 * 9 + 6) * (9 * 4 + 2))
# --> 2 4 * 2 + 6 6 8 + 9 * 6 + + 9 4 * 2 + * +
# close parens pops op from op stack, pushes op to stack
# op pushes to op stack
# number pops from op stack, pushes op to stack
def postfix(line: str) -> list:
    # this splits by spaces but keeps parens in place. Check parens level
    articles = line.split()
    # parens level
    parens = 0
    stack = []
    op = []
    aclose = 0
    for a in articles:
        if a in ['*', '+']:
            op.append(a)
        elif '(' in a:
            aparens = a.count('(')
            parens += aparens
            stack.append(int(a[aparens:]))
        elif ')' in a:
            aclose = a.count(')')
            parens -= aclose
            stack.append(int(a[:-aclose]))
            stack.append(op.pop())
            for i in range(aclose):
                if len(op) > 0:
                    stack.append(op.pop())
        else:
            stack.append(int(a))
            if len(op) > 0:
                stack.append(op.pop())
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
    print(stack[0])
    return(stack.pop())
                
with open('day18.in') as f:
    lines = f.read().splitlines()

stacks = []
for line in lines:
    stacks.append(postfix(line))

eqnsum = 0
for eqn in stacks:
    eqnsum += solve(eqn)
print(f"Day 18 Part 1: { eqnsum }")