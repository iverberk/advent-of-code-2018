import re
import sys

coordinates = []

with open('input') as f:
    for index, coordinate in enumerate(f):
        m = re.match(
            r".*<([\s\d-]+),([\s\d-]+)> .*<([\s\d-]+),([\s\d-]+)>", coordinate)
        (x, y, vx, vy) = [int(n) for n in m.groups()]
        coordinates.append({
            'position': (x, y),
            'velocity': (vx, vy)
        })

second = 0
while True:
    min_x, min_y, max_x, max_y = sys.maxsize, sys.maxsize, 0, 0
    positions = set()
    for coordinate in coordinates:
        x, y = coordinate['position']
        vx, vy = coordinate['velocity']
        nx, ny = x+(vx*second), y+(vy*second)
        if nx < min_x:
            min_x = nx
        elif nx > max_x:
            max_x = nx
        elif ny < min_y:
            min_y = ny
        elif ny > max_y:
            max_y = ny

        positions.add((nx, ny))

    neighbours = 0
    for position in positions:
        x, y = position
        if ((x-1, y) in positions or
            (x+1, y) in positions or
            (x, y-1) in positions or
            (x, y+1) in positions or
            (x-1, y-1) in positions or
            (x+1, y-1) in positions or
            (x-1, y+1) in positions or
                (x+1, y+1) in positions):
            neighbours += 1

    ratio = neighbours / len(positions)
    if ratio > 0.99:
        print('Letters appeared in the Sky after:', second)
        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):
                if (x, y) in positions:
                    print('#', end='')
                else:
                    print('.', end='')
            print()
        break

    second += 1
