from copy import deepcopy

class seats:
    orig = []
    seats = []
    previous = []
    peers = None
    max_mult = 1
    max_seen = 4

    def __init__(self, seat_grid):
        self.peers = {}
        for y_grid in seat_grid:
            self.orig.append([x for x in y_grid])
        self.reset()
    
    def find_peers(self):
        self.peers = {}
        for y in range(len(self.orig)):
            self.peers[y] = {}
            for x in range(len(self.orig[y])):
                if self.orig[y][x] == 'L':
                    self.peers[y][x] = []
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            pos = self.get_pos(x, y, dx, dy)
                            if pos is not None:
                                self.peers[y][x].append(pos)
    
    def get_pos(self, x, y, dx, dy):
        if dx == 0 and dy == 0: return None
        for mult in range(1, self.max_mult+1):
            test_y = y + dy * mult
            test_x = x + dx * mult
            if test_y < 0: return None
            if test_x < 0: return None
            if test_y >= len(self.orig): return None
            if test_x >= len(self.orig[test_y]): return None
            c = self.orig[test_y][test_x]
            if c == 'L': return [test_x, test_y]
        return None

    def reset(self):
        self.seats = deepcopy(self.orig)
    
    def _get(self, pos) -> bool:
        x = pos[0]
        y = pos[1]
        c = self.previous[y][x]
        if c in '.L': return False
        if c == '#': return True
    
    def _set(self, x, y, val):
        if self.seats[y][x] == '.':
            return
        if val:
            self.seats[y][x] = '#'
        else:
            self.seats[y][x] = 'L'
    
    def decide(self, x, y) -> bool:
        count = 0
        for peer in self.peers[y][x]:
            if self._get(peer):
                count += 1
        me = self._get([x, y])
        if me and count >= self.max_seen:
            self._set(x, y, False)
        elif not me and count == 0:
            self._set(x, y, True)
    
    def run(self, max_seen = 4, mult = False):
        self.reset()
        self.max_seen = max_seen
        if mult:
            self.max_mult = min([len(self.orig), len(self.orig[0])])
        self.find_peers()
        turn = 0
        while str(self) != self.strprev():
            turn += 1
            self.previous = deepcopy(self.seats)
            for y in self.peers.keys():
                for x in self.peers[y].keys():
                    self.decide(x, y)
        print(f"Steady state reached in { turn } turns. { self.count() } seats occupied.")
    
    def count(self):
        count = 0
        for y in range(len(self.seats)):
            for x in range(len(self.seats[0])):
                if self._get([x, y]):
                    count += 1
        return count
    
    def __str__(self):
        return '\n'.join([''.join(x) for x in self.seats])
    
    def strprev(self):
        return '\n'.join([''.join(x) for x in self.previous])

if __name__ == '__main__':
    with open('day11.in') as f:
        seat_grid = f.read().splitlines()
    
    s = seats(seat_grid)
    print("Day 11 Part 1:")
    s.run()
    print()
    print("Day 11 Part 2:")
    s.run(max_seen = 5, mult = True)
