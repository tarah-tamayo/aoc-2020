class node:
    turn = 0
    start = 0
    cur = False
    nxt = False
    turns = None

    coord = None
    neighbors = None
    nodes = None

    def __init__(self, nodes, x,y,z, turn=0):
        self.nodes = nodes
        self.coord = tuple([x,y,z])
        self.turn = turn
        self.start = turn
        self.turns = []
        self.neighbors = []
    
    def __str__(self):
        return '#' if self.cur else '.'
    
    def __repr__(self):
        return str(self)
    
    def get_next(self):
        c = 0
        for ncoord in self.neighbors:
            n = self.nodes.get(ncoord)
            if n.cur:
                c += 1
        self.nxt = False
        if self.cur:
            if c == 2:
                self.nxt = True
        if c == 3:
            self.nxt = True
    
    def next_turn(self):
        self.turns.append(self.nxt)
        self.turn += 1
        self.cur = self.nxt
        self.nxt = False
    
    def share_neigh(self):
        if self.cur:
            # Should only need well defined neighbors if this node is ON
            self.nodes.get_neigh(self)
        for ncoord in self.neighbors:
            n = self.nodes.get(ncoord)
            if self.coord not in n.neighbors:
                n.neighbors.append(self.coord)

class nodes:
    turn = 0
    nodes = None
    offsets = []

    def __init__(self):
        self.nodes = {}
        val = [0,1,-1]
        for x in val:
            for y in val:
                for z in val:
                    if x != 0 or y != 0 or z != 0:
                        self.offsets.append([x,y,z])
    
    def get(self, coord: tuple) -> object:
        if coord in self.nodes.keys():
            return self.nodes[coord]
        else:
            return None
    
    def gen_node(self, x,y,z, init=False):
        tup = tuple([x,y,z])
        if tup in self.nodes.keys():
            n = self.nodes[tup]
        else:
            n = node(self, x,y,z, self.turn)
        n.cur = init
        self.nodes[tup] = n
        if init:
            self.get_neigh(n)
    
    def get_neigh(self, node):
        neighs = []
        tup = node.coord
        for offset in self.offsets:
            x = tup[0] + offset[0]
            y = tup[1] + offset[1]
            z = tup[2] + offset[2]
            t = tuple([x,y,z])
            if t not in self.nodes.keys():
                self.gen_node(x,y,z)
            neighs.append(self.nodes[t].coord)
        node.neighbors = neighs

    def share_neigh(self):
        n = list(self.nodes.values())
        for node in n:
            node.share_neigh()

    def run_turn(self):
        self.share_neigh()
        for n in self.nodes.values():
            n.get_next()
        for n in self.nodes.values():
            n.next_turn()
        self.turn += 1
        self.share_neigh()
    
    def run_to(self, turn):
        while self.turn < turn:
            self.run_turn()

    def count(self) -> int:
        c = 0
        for n in self.nodes.values():
            if n.cur:
                c += 1
        return c
    
    def z_level(self, z):
        kdic = {}
        keys = list(filter(lambda k: k[2] == z, self.nodes.keys()))
        for k in keys:
            if k[1] not in kdic.keys():
                kdic[k[1]] = {}
            kdic[k[1]][k[0]] = '#' if self.nodes[k].cur else '.'
        print(f"z={ z }")
        for y in sorted(list(kdic.keys())):
            print(''.join([kdic[y][x] for x in sorted(list(kdic[y].keys()))]))
        print()


if __name__ == '__main__':
    N = nodes()

    with open('day17.in') as f:
        lines = f.read().splitlines()
    
    z = 0
    for y in range(len(lines)):
        chars = [x for x in lines[y]]
        for x in range(len(chars)):
            if chars[x] == '#':
                N.gen_node(x,y,z,True)
    
    N.run_to(6)
    print(f"Day 17 Part 1: { N.count() }")