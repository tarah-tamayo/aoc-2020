import re
import string

def getlines(fname):
    with open(fname) as f:
        lines = f.read().splitlines()
    return lines

def parse_lines(lines):
    rules = {}
    msgs = []
    for line in lines:
        match = re.match(r"(\d+): (.*)$", line)
        if match:
            g = match.groups()
            if '"' not in g[1]:
                ors = [g[1]]
                if '|' in g[1]:
                    ors = g[1].split('|')
                rule = []
                for r in ors:
                    rule.append([x for x in r.split()])
                rules[g[0]] = rule
            else:
                rules[g[0]] = [g[1].strip('"')]
        else:
            msgs.append(line)
    return [rules, msgs]

def compile_rule(rules, rule, depth=0, maxdepth=25):
    ors = []
    for rule_or in rule:
        opt = []
        for r in rule_or:
            if r in string.ascii_letters:
                opt.append(r)
            elif depth <= maxdepth:
                s = compile_rule(rules, rules[r], depth=depth+1)
                if len(s) > 0:
                    opt.append(s)
        if len(opt) > 0:
            ors.append(opt)
    if len(ors) == 0: return ''
    if len(ors) == 1:
        return ''.join(ors[0])
    out = '(' + ''.join(ors[0])
    for o in range(1, len(ors)):
        out += "|" + ''.join(ors[o])
    out += ')'
    return out

def count_valid(rules, lines):
    rule = compile_rule(rules, rules['0'])
    match = re.compile('^' + rule + '$')
    count = 0
    for msg in msgs:
        if match.match(msg):
            count += 1
    return count

lines = getlines('day19.in')
rules, msgs = parse_lines(lines)
print(f"Day 19 Part 1: { count_valid(rules,lines) }")

lines = getlines('day19b.in')
rules, msgs = parse_lines(lines)
print(f"Day 19 Part 2: { count_valid(rules,lines) }")