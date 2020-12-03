

class treegrid:
    grid = []
    max_v = 0
    max_h = 0

    def __init__(self, textgrid: list):
        """
        Constructor input: text grid as a list of strings.
        '.' is open space
        '#' is tree
        (v) Y-axis (first index) is unique and finite
        (h) X-axis (second index) repeats and is infinite
        """
        for textline in textgrid:
            line = [True if x == '#' else False for x in textline]
            self.grid.append(line)
        self.max_v = len(self.grid)
        self.max_h = len(self.grid[0])
        
    def count_slope(self, right:int, down: int) -> int:
        """
        Counts the number of trees encountered with the provided slope, starting 
        at (0,0) - upper left corner
        """
        h = 0
        count = 0
        for v in range(0, self.max_v, down):
            if h >= self.max_h:
                h = h - self.max_h
            if self.grid[v][h]:
                count += 1
            h += right
        return count
    
    def multiply_slopes(self, slopes: list) -> int:
        mult = 1
        for slope in slopes:
            mult = mult * self.count_slope(slope[0], slope[1])
        return mult
        
if __name__ == "__main__":
    with open('day3.in') as f:
        textgrid = f.read().splitlines()

    tg = treegrid(textgrid)
    print(f"part 1: { tg.count_slope(3,1) }")
    
    slopes = [[1,1],[3,1],[5,1],[7,1],[1,2]]
    print(f"part 2: { tg.multiply_slopes(slopes) }")