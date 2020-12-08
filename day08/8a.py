from copy import deepcopy

class prog:
    lines = []
    seen = []
    step = 0
    acc = 0

    def __init__(self, lines):
        for line in lines:
            code = line.split()[0]
            val = int(line.split()[1])
            self.lines.append([code, val])
    
    def run(self) -> bool:
        self.seen = []
        self.acc = 0
        self.step = 0
        while self.step < len(self.lines) and self.step not in self.seen:
            self.seen.append(self.step)
            instr = self.lines[self.step]
            code = instr[0]
            val = instr[1]
            if code == "acc":
                self.acc += val
                self.step += 1
            elif code == "nop":
                self.step += 1
            else:
                self.step += val
        print(f"Program stopped at line { self.step }.")
        print(f"Accumulator at stop: { self.acc }")
        if self.step in self.seen:
            print(f"Program halted due to loop.")
            return False
        return True

    def recover(self):
        print()
        print(f"Attempting to recover. . .")
        last_seen = deepcopy(self.seen)
        last_acc = self.acc
        last_step = self.step
        count = 0
        changes = 0
        while self.step < len(self.lines):
            self.seen = deepcopy(last_seen)
            self.acc = last_acc
            self.step = last_step
            for _ in range(count+1):
                self.step == self.seen.pop()
            while self.lines[self.step][0] == "acc":
                self.step = self.seen.pop()
                count += 1
            
            this_step = self.step
            code = self.lines[this_step][0]
            print()
            if code == "nop":
                print(f"Recovering... changed instruction { this_step } from { code } to jmp")
                self.lines[this_step][0] = "jmp"
                changes += 1
            else:
                print(f"Recovering... changed instruction { this_step } from { code } to nop")
                self.lines[this_step][0] = "nop"
                changes += 1
            if not self.run():
                self.lines[this_step][0] = code
        print(f"Recovered after { changes } attempts.")

if __name__ == "__main__":
    with open('day8.in') as f:
        lines = f.read().splitlines()
    p = prog(lines)
    p.run()
    p.recover()