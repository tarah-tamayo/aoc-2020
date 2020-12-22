import sys
import re
from copy import deepcopy

class monster:
    monster = None

    def __init__(self):
        self.monster = []
        lines = ["                  # ", "#    ##    ##    ###", " #  #  #  #  #  #   "]
        for line in lines:
            print(line)
            m = ['1' if x == "#" else '0' for x in line]
            self.monster.append(int('0b' + ''.join(m), 2))

    def find_monsters(self, t) -> int:
        c = 0
        #for i in range(len(t.grid)-len(self.monster)):
        for i in range(1, len(t.grid)-1):
            for j in range(len(t.grid[i]) - 20):
                key = int('0b' + ''.join(t.bingrid[i][j:j+20]), 2)
                if (key & self.monster[1]) == self.monster[1]:
                    print(f"OwO? [{i}][{j}]")
                    print(''.join(t.grid[i-1][j:j+20]))
                    print(''.join(t.grid[i][j:j+20]))
                    print(''.join(t.grid[i+1][j:j+20]))
                    print()
                    key = int('0b' + ''.join(t.bingrid[i+1][j:j+20]), 2)
                    if (key & self.monster[2]) == self.monster[2]:
                        print(f"OwO? What's this? [{ i }][{ j }]")
                        c += 1
                    else:
                        print(f"no wo :'( ")
                #grid = []
                #for k in range(len(self.monster)):
                #    g = [True if x == '#' else False for x in t.grid[i+k][j:j+20]]
                #    grid.append(g)
                    #grid.append(int('0b'+''.join(g), 2))
                    #grid[k] = grid[k] & self.monster[k]
                #if self.check_grid(grid):
                #    print("OwO!")
                #    c += 1
                #if grid == self.monster:
                #    c += 1
        return c
    
    def check_grid(self, grid: list) -> bool:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                grid[i][j] = grid[i][j] and self.monster[i][j]
        return grid == self.monster

class tile:
    tid = 0
    grid = None
    bingrid = None
    edges = None

    neighbors = None

    def __init__(self, lines, img=False):
        """
        tile(lines, img) - Constructor. Boolean img defaults to False. If True this is a tile holding
                           a full, stitched image. Edge detection is not required.
        """
        self.grid = []
        self.bingrid = []
        self.edges = []
        self.neighbors = []
        self.parse(lines)
        if not img:
            self.find_edges()
    
    def parse(self, lines):
        for line in lines:
            match = re.match(r"Tile ([0-9]+):", line)
            if match:
                self.tid = int(match.groups()[0])
            else:
                self.grid.append([x for x in line])
    
    def create_bingrid(self):
        self.bingrid = []
        for i in range(len(self.grid)):
            binstr = ['1' if x == '#' else '0' for x in self.grid[i]]
            self.bingrid.append(binstr)

    def find_edges(self):
        """
        find_edges() - Finds the edges of the tile grid

        convention is that top and bottom edges are --> and left and right edges are top-down
        In order, edges are defined as:
        [0] - TOP
        [1] - RIGHT
        [2] - BOTTOM
        [3] - LEFT
        """
        self.edges = [deepcopy(self.grid[0]), [], deepcopy(self.grid[-1]), []]
        for g in self.grid:
            self.edges[3].append(g[0])
            self.edges[1].append(g[-1])
        self.edges[2]
        self.edges[3]
    
    def lr_flip(self):
        """
        lr_flip() - Flips grid Left / Right
        """
        for g in self.grid:
            g.reverse()
    
    def td_flip(self):
        """
        td_flip() - Flips grid Top / Down
        """
        self.cw_rotate()
        self.cw_rotate()
        self.lr_flip()
        self.find_edges()
    
    def cw_rotate(self):
        """
        cw_rotate() - Rotates grid clockwise 90 deg
        """
        self.grid = [list(x) for x in zip(*self.grid[::-1])]
        self.find_edges()
    
    def orient(self, t2, left=False):
        """
        orient(t2, left) - reorients this tile to match t2. Left defaults to False and, if true, 
                           indicates that t2 is to the left of this tile. Otherwise it assumes
                           t2 is above this tile.
        """
        # In order, edges are defined as:
        # [0] - TOP
        # [1] - RIGHT
        # [2] - BOTTOM
        # [3] - LEFT
        edge_i = self.get_edge(t2)
        if left:
            edge_t = 3
            target = 1
        else:
            edge_t = 2
            target = 0
        while edge_i != edge_t:
            self.cw_rotate()
            edge_i = self.get_edge(t2)
        if list(reversed(self.edges[edge_t])) == t2.edges[target]:
            if left:
                self.td_flip()
            else:
                self.lr_flip()

    def get_edge(self, t2) -> int:
        """
        get_edge(t2) -> int - Returns the edge index of this tile that matches t2. If there is no common edge
                              returns -1.
        """
        for i in range(len(self.edges)):
            e = self.edges[i]
            for e2 in t2.edges:
                if e == e2:
                    if t2 not in self.neighbors:
                        self.neighbors.append(t2)
                    if self not in t2.neighbors:
                        t2.neighbors.append(self)
                    return i
                if list(reversed(e)) == e2:
                    if t2 not in self.neighbors:
                        self.neighbors.append(t2)
                    if self not in t2.neighbors:
                        t2.neighbors.append(self)
                    return i
        return -1
    
    def compare(self, t2) -> bool:
        """
        compare(t2) - Finds whether a common edge with tile t2 is present
        """
        return True if self.get_edge(t2) >= 0 else False
    
    def find_common_neighbors(self, t2) -> list:
        """
        find_common_neighbors(t) - Returns a list of common neighbors
        """
        neighs = []
        for n in self.neighbors:
            if n in t2.neighbors:
                neighs.append(n)
        return neighs
    
    def remove_edges(self):
        self.grid = self.grid[1:-1]
        for g in self.grid:
            g = g[1:-1]
    
    def __len__(self):
        self.create_bingrid()
        c = 0
        for bg in self.bingrid:
            g = [1 if x == '1' else 0 for x in bg]
            c += sum(g)
        return c

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
    # image stitched together
    image = None

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
        self.stitch_image()
    
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
        t = tile(tile_lines)
        self.tiles[t.tid] = t
    
    def find_neighbors(self):
        for i in range(len(self.tiles.keys())):
            t1 = self.tiles[list(self.tiles.keys())[i]]
            for j in range(0, len(self.tiles.keys())):
                t2 = self.tiles[list(self.tiles.keys())[j]]
                if t1 != t2:
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
        # orient to right side neighbor as top
        c.orient(t)
        # rotate clockwise to change top to right side
        c.cw_rotate()
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
        for i in range(1,len(self.grid[0])):
            self.grid[0][i].orient(self.grid[0][i-1], left=True)
        for i in range(1,len(self.grid)):
            for j in range(1,len(self.grid[i])):
                neighs = self.grid[i][j-1].find_common_neighbors(self.grid[i-1][j])
                for n in neighs:
                    if n not in self.grid[i-1]:
                        self.grid[i][j] = n
                        self.grid[i][j].orient(self.grid[i-1][j])
        for t in self.tiles.values():
            t.remove_edges()
    
    def print_grid_ids(self):
        for g in self.grid:
            s = ""
            for t in g:
                if t is None:
                    s += " None -"
                else:
                    s += f" { t.tid } -"
            print(s)

    def stitch_image(self):
        # Create an empty tile object for the full image
        tile_lines = ["Tile 1:"]
        self.image = tile(tile_lines, img=True)
        line = 0
        for g in self.grid:
            self.image.grid.extend([[] for _ in range(len(g[0].grid))])
            for t in g:
                for i in range(len(t.grid)):
                    self.image.grid[line+i].extend(t.grid[i])
            line += len(g[0].grid)
        self.image.create_bingrid()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        file = 'day20/day20.in'
    with open(file) as f:
        lines = f.read().splitlines()
    
    img = image(lines)
    mult = 1
    for t in img.corners:
        mult *= t.tid
    
    print(f"Day 20 Part 1: { mult }")

    m = monster()
    c = m.find_monsters(img.image)
    i = 0
    while c == 0 and i < 4:
        print("...rotating...")
        img.image.cw_rotate()
        img.image.create_bingrid()
        i += 1
    if c == 0:
        print("...flipping...")
        img.image.lr_flip
        img.image.create_bingrid()
        c = m.find_monsters(img.image)
        i = 0
        while c == 0 and i < 4:
            print("...rotating...")
            img.image.cw_rotate()
            i += 1
    print(img.image)
    print(c)
    print(f"Day 20 Part 2: { len(img.image) }")

    #lines = ['Tile 99:', '#...#', '.#...', '..#..', '...#.', '....#']
    #t = tile(lines)
    #print(t)
    #t.td_flip()
    #print(t)