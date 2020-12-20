import sys
import re
from copy import deepcopy

class tile:
    tid = 0
    grid = None
    edges = None

    neighbors = None

    def __init__(self, lines):
        self.grid = []
        self.edges = []
        self.neighbors = []
        self.parse(lines)
        self.find_edges()
    
    def parse(self, lines):
        for line in lines:
            match = re.match(r"Tile ([0-9]+):", line)
            if match:
                self.tid = int(match.groups()[0])
            else:
                self.grid.append([x for x in line])

    def find_edges(self):
        """
        find_edges() - Finds the edges of the tile grid

        convention is that edges are CLOCKWISE. This means the left edge and bottom edge
        must be reversed! In order, edges are defined as:
        [0] - TOP
        [1] - RIGHT
        [2] - BOTTOM
        [3] - LEFT
        """
        self.edges = [deepcopy(self.grid[0]), [], deepcopy(self.grid[-1]), []]
        for g in self.grid:
            self.edges[3].append(g[0])
            self.edges[1].append(g[-1])
        self.edges[2].reverse()
        self.edges[3].reverse()
    
    def lr_flip(self):
        """
        lr_flip() - Flips grid Left / Right
        """
        for g in self.grid:
            g.reverse()
        self.find_edges()
    
    def cw_rotate(self):
        """
        cw_rotate() - Rotates grid clockwise 90 deg
        """
        self.grid = list(zip(*self.grid[::-1]))
    
    def compare(self, t2) -> bool:
        """
        compare(t2) - Finds whether a common edge with tile t2 is present
        """
        for e in self.edges:
            for e2 in t2.edges:
                if e == e2:
                    if t2 not in self.neighbors:
                        self.neighbors.append(t2)
                    if self not in t2.neighbors:
                        t2.neighbors.append(self)
                    return True
                if list(reversed(e)) == e2:
                    if t2 not in self.neighbors:
                        self.neighbors.append(t2)
                    if self not in t2.neighbors:
                        t2.neighbors.append(self)
                    return True
    
    def find_common_neighbors(self, t2) -> list:
        """
        find_common_neighbors(t) - Returns a list of common neighbors
        """
        neighs = []
        for n in self.neighbors:
            if n in t2.neighbors:
                neighs.append(n)
        return neighs
    
    def __str__(self):
        s = f"\n ----- Tile { self.tid } -----"
        for g in self.grid:
            s += "\n" + ''.join(g)
        return s

class image:
    # Dict of tiles by id
    tiles = None
    # 2d grid of tile IDs and rotations
    grid = None
    # Found corners
    corners = None

    def __init__(self, lines):
        """
        image() - Constructor

        Takes ALL tile lines and parses them to make a dictionary of tiles
        """
        self.tiles = {}
        self.parse(lines)
        self.find_neighbors()
        self.find_corners()
        self.build_grid_top()
        self.build_grid_left()
        self.fill_grid()
    
    def parse(self, lines):
        tile_lines = []
        for line in lines:
            if 'Tile' in line:
                if len(tile_lines):
                    t = tile(tile_lines)
                    self.tiles[t.tid] = t
                tile_lines = [line]
            elif len(line):
                tile_lines.append(line)
    
    def find_neighbors(self):
        for i in range(len(self.tiles.keys())):
            t1 = self.tiles[list(self.tiles.keys())[i]]
            for j in range(i+1, len(self.tiles.keys())):
                t2 = self.tiles[list(self.tiles.keys())[j]]
                t1.compare(t2)
    
    def find_corners(self):
        self.corners = []
        for tile in self.tiles.values():
            if len(tile.neighbors) == 2:
                self.corners.append(tile)
        s = ""
        for t in self.corners:
            s += f" { t.tid }"
        print(s)
    
    def build_grid_top(self):
        c = self.corners[0]
        t = c.neighbors[0]
        self.grid = [[c, t]]
        n = len(t.neighbors)
        while n == 3:
            for nbr in t.neighbors:
                if len(nbr.neighbors) == 3 and nbr not in self.grid[0]:
                    t = nbr
                elif len(nbr.neighbors) == 2 and nbr not in self.grid[0]:
                    t = nbr
            self.grid[0].append(t)
            n = len(t.neighbors)
    
    def build_grid_left(self):
        c = self.corners[0]
        t = c.neighbors[1]
        left = [c, t]
        n = len(t.neighbors)
        while n == 3:
            for nbr in t.neighbors:
                if len(nbr.neighbors) == 3 and nbr not in left:
                    t = nbr
                elif len(nbr.neighbors) == 2 and nbr not in left:
                    t = nbr
            left.append(t)
            n = len(t.neighbors)
        for i in range(1, len(left)):
            self.grid.append([None for _ in range(len(self.grid[0]))])
            self.grid[i][0] = left[i]
    
    def fill_grid(self):
        for i in range(1,len(self.grid)):
            for j in range(1,len(self.grid[i])):
                neighs = self.grid[i][j-1].find_common_neighbors(self.grid[i-1][j])
                for n in neighs:
                    self.print_grid_ids()
                    print(n)
                    print()
                    if n not in self.grid[i-1]:
                        self.grid[i][j] = n
    
    def print_grid_ids(self):
        for g in self.grid:
            s = ""
            for t in g:
                if t is None:
                    s += " None -"
                else:
                    s += f" { t.tid } -"
            print(s)

if __name__ == '__main__':
    file = sys.argv[1]
    with open(file) as f:
        lines = f.read().splitlines()
    
    img = image(lines)
    mult = 1
    for t in img.corners:
        mult *= t.tid
    
    print(f"Day 20 Part 1: { mult }")
    
    img.print_grid_ids()