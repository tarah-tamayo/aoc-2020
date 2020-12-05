with open('day5.in') as f:
    seats = f.read().splitlines()

trans = { ord('B'): ord('1'),
          ord('F'): ord('0'),
          ord('R'): ord('1'),
          ord('L'): ord('0') }

seat_bin = map(lambda x: int(x.translate(trans), 2), seats)
seat_sorted = sorted(list(seat_bin))

seat_min = min(seat_sorted)
seat_max = max(seat_sorted)

my_seat = 0
for i in range(1, len(seat_sorted)-1):
    if seat_sorted[i+1] - seat_sorted[i] > 1:
        my_seat = seat_sorted[i] + 1

print(f"Day 5 Part 1: { seat_max }")
print(f"Day 5 Part 2: { my_seat }")

