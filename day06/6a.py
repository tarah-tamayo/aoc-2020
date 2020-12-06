with open('day6.in') as f:
	groups = f.read().split('\n\n')
	
count1 = 0
count2 = 0
for group in groups:
	people = group.split()
	gset1 = set()
	gset2 = set(list(group))
	for person in people:
		pset = set(list(person.rstrip()))
		gset1 = gset1.union(pset)
		gset2 = gset2.intersection(pset)
	count1 += len(gset1)
	count2 += len(gset2)

print(f"Day 6 Part 1: { count1 }")
print(f"Day 6 Part 2: { count2 }")
