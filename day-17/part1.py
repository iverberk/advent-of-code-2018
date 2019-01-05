from collections import defaultdict, deque
import re

SAND, WATER, CLAY = '.', '*', '#'

r = re.compile(r'.*=(\d+).*=(\d+)..(\d+)')
ground = defaultdict(lambda: '.')

with open('input') as f:
    for line in f:
        axis = line[0]
        pos, r_min, r_max = map(int, r.match(line).groups())

        for i in range(r_min, r_max+1):
            location = (pos, i) if axis == 'x' else (i, pos)
            ground[location] = CLAY


def draw_ground():
    points = ground.keys()
    min_x, max_x = min(points)[0], max(points)[0]
    max_y = max(points, key=lambda p: p[1])[1]
    # max_y = 125

    for y in range(0, max_y):
        for x in range(min_x, max_x+1):
            print(ground[(x, y)], end='')
        print()
    print()


points = ground.keys()
max_y = max(points, key=lambda p: p[1])[1]

springs = deque([(500, 0, 500, 500)])


def fill_bucket(spring, round, p=False):
    x, y, left_x, right_x = spring
    # print(x, y, left_x, right_x)
    edge = False

    if ground[(x, y)] == WATER:
        return

    while y <= max_y:
        element = ground[(x, y+1)]

        # Move down if we can
        if element in [SAND]:
            y += 1
            if y <= max_y:
                ground[(x, y)] = WATER
            continue

        # Move left and right on the current buckets
        elif element in [CLAY, WATER]:

            if p:
                print(x, left_x, right_x)

            if (x < left_x or x > right_x) and element == WATER:
                return

            ground[(x, y)] = WATER

            start = x
            edges = []

            if ground[(x-1, y)] == CLAY and x < left_x:
                left_x = x

            while ground[(x-1, y)] != CLAY:
                x -= 1

                if element == CLAY and x < left_x:
                    left_x = x

                if ground[(x, y+1)] == SAND:
                    edges.append((x, y-1))
                    break

                ground[(x, y)] = WATER

            if round == 32:
                print("blabla", x)

            x = start
            if ground[(x+1, y)] == CLAY and x > right_x:
                if round == 32:
                    print("Setting 1", x)
                right_x = x

            while ground[(x+1, y)] != CLAY:
                x += 1

                if element == CLAY and x > right_x:
                    if round == 32:
                        print("Setting 2", x)
                    right_x = x

                # Check if we can flow down from here
                if ground[(x, y+1)] == SAND:
                    edges.append((x, y-1))
                    break

                ground[(x, y)] = WATER

            if edges:
                for edge in edges:
                    x, y = edge
                    springs.append((x, y, left_x, right_x))
                break

            x = start
            y -= 1


count = 0
while springs:
    count += 1
    fill_bucket(springs.popleft(), count, count == 34)
    if count == 34:
        print(springs)
        break

draw_ground()
print(len([e for e in ground.values() if e == WATER]))
