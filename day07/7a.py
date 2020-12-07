import re

class bag:
    bagType = ''
    # dictionary of tuples (num, ref) by bag name
    contains = None
    # dictionary of references by bag name
    contained_by = None

    def __init__(self, bagType):
        self.bagType = bagType
        self.contains = {}
        self.contained_by = {}
    
    def __str__(self):
        return self.bagType

    def __repr__(self):
        return self.bagType
    
    def prt(self):
        print(f"{ list(self.contained_by.keys()) } --> { self.bagType } --> { list(self.contains.keys()) }")
    
    def add_contains(self, num: int, bagRef):
        if bagRef.bagType in self.contained_by.keys():
            raise Exception(f"ERROR: Bag _{ self.bagType }_ cannot contain and be contained by _{ bagRef.bagType }_")
        if bagRef.bagType in self.contains.keys():
            raise Exception(f"ERROR: Bag _{ self.bagType }_ already contains _{ bagRef.bagType }_")
        bag_tup = [num, bagRef]
        self.contains[bagRef.bagType] = bag_tup
    
    def add_contained_by(self, bagRef):
        if bagRef.bagType in self.contains.keys():
            raise Exception(f"ERROR: Bag _{ self.bagType }_ cannot contain and be contained by _{ bagRef.bagType }_")
        self.contained_by[bagRef.bagType] = bagRef
    
    def count_succ(self) -> int:
        count = 0
        if len(self.contains.keys()) == 0:
            return 0
        for succ in self.contains.values():
            # Add one to include bag with its contents
            count += succ[0] * (succ[1].count_succ() + 1)
        return count

class bags:
    # dictionary of bag references
    bags = {}

    def get(self, bagType) -> object:
        if bagType not in self.bags.keys():
            raise Exception(f"ERROR: _{ bagType }_ not found!")
        return self.bags[bagType]

    def parse_line(self, line):
        container = line[:line.find('bags')].strip()
        if container in self.bags.keys():
            c = self.bags[container]
        else:
            c = bag(container)
            self.bags[container] = c
        contents = re.findall('([0-9]+) ((?!(bag))[a-zA-Z ]+) bags?[,.]', line.partition('contain ')[2])
        for cont in contents:
            # cont is a tuple of # and bag name
            if cont[1] in self.bags.keys():
                b = self.bags[cont[1]]
            else:
                b = bag(cont[1])
                self.bags[cont[1]] = b
            b.add_contained_by(c)
            c.add_contains(int(cont[0]), b)
    
    def count_pred(self, bagType) -> int:
        b = self.get(bagType)
        todo = list(b.contained_by.values())
        done = []
        while len(todo) > 0:
            pred = todo.pop()
            if pred not in done and pred != b:
                todo.extend(list(pred.contained_by.values()))
                done.append(pred)
        return len(done)
    
if __name__ == "__main__":
    with open('day7.in') as f:
        lines = f.read().splitlines()
    
    all_bags = bags()

    for line in lines:
        all_bags.parse_line(line)
    
    num_can_have_sgb = all_bags.count_pred("shiny gold")
    num_in_sgb = all_bags.get("shiny gold").count_succ()
    
    print(f"Day 7 Part 1: { num_can_have_sgb }")
    print(f"Day 7 Part 2: { num_in_sgb }")