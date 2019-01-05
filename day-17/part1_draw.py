from PIL import Image, ImageDraw
from collections import defaultdict, deque
import re

SAND, WATER_REST, WATER_FLOW, CLAY = '.', '~', '|', '#'

r = re.compile(r'.*=(\d+).*=(\d+)..(\d+)')
ground = defaultdict(lambda: '.')

with open('test') as f:
    for line in f:
        axis = line[0]
        pos, r_min, r_max = map(int, r.match(line).groups())

        for i in range(r_min, r_max+1):
            location = (pos, i) if axis == 'x' else (i, pos)
            ground[location] = CLAY


def draw_ground(name):
    points = ground.keys()
    min_x, max_x = min(points)[0], max(points)[0]
    max_y = max(points, key=lambda p: p[1])[1]

    img = Image.new('RGB', ((max_x-min_x)*15, max_y*10), color=(0, 0, 0))

    d = ImageDraw.Draw(img)

    for y in range(0, max_y+1):
        for x in range(min_x, max_x+1):
            d.text(((x-min_x)*10, y*10), ground[(x, y)], fill=(255, 255, 0))
    img.save(name + '.png')


points = ground.keys()
max_y = max(points, key=lambda p: p[1])[1]


springs = deque([(500, 0)])


def fill_bucket(position):
    x, y = position

    rounds = 0
    next_bucket = False
    while y <= max_y:
        rounds += 1

        if rounds == 51:
            print("Writing image")
            draw_ground("ground")
            break

        element = ground[(x, y+1)]

        # Move down if we can
        if element == SAND:
            y += 1
            if y <= max_y:
                ground[(x, y)] = WATER_FLOW
            continue

        if next_bucket:
            break

        # Move left and right on the current level
        elif element in [CLAY, WATER_REST]:
            ground[(x, y)] = WATER_REST

            start = x
            while ground[(x-1, y)] == SAND:
                x -= 1
                ground[(x, y)] = WATER_REST

                # Check if we can flow down from here
                if ground[(x, y+1)] == SAND:
                    springs.append((x, y))
                    next_bucket = True
                    break

            x = start
            while ground[(x+1, y)] == SAND:
                x += 1
                ground[(x, y)] = WATER_REST

                # Check if we can flow down from here
                if ground[(x, y+1)] == SAND:
                    springs.append((x, y))
                    next_bucket = True
                    break

            x = start
            y -= 1


while springs:
    fill_bucket(springs.popleft())

draw_ground()
# print(len([e for e in ground.values() if e in [WATER_FLOW, WATER_REST]]))
