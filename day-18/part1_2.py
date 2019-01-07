from collections import defaultdict
from copy import copy

area = defaultdict(lambda: 'X')

OPEN, TREE,  LUMBERYARD = '.', '|', '#'
WIDTH, HEIGHT = 50, 50

with open('input') as f:
    for y, line in enumerate(f):
        for x, c in enumerate(line):
            area[(x, y)] = c

resource_values = []
cycle, cycle_diff = 0, 0
minute = 1
while True:
    old_area = copy(area)
    area.clear()

    for y in range(HEIGHT):
        for x in range(WIDTH):
            neighbours = [(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)]

            pos = old_area[(x, y)]
            if pos == OPEN:
                num_trees = len([n for n in neighbours if old_area[n] == TREE])
                area[(x, y)] = TREE if num_trees >= 3 else OPEN

            if pos == TREE:
                num_lumberyards = len([n for n in neighbours if old_area[n] == LUMBERYARD])
                area[(x, y)] = LUMBERYARD if num_lumberyards >= 3 else TREE

            if pos == LUMBERYARD:
                num_trees = len([n for n in neighbours if old_area[n] == TREE])
                num_lumberyards = len([n for n in neighbours if old_area[n] == LUMBERYARD])
                area[(x, y)] = LUMBERYARD if (num_trees > 0 and num_lumberyards > 0) else OPEN

    wooded = len([a for a in area.values() if a == TREE])
    lumberyards = len([a for a in area.values() if a == LUMBERYARD])

    resource_value = wooded*lumberyards

    if minute == 10:
        print("part 1:", resource_value)

    if resource_value not in resource_values:
        resource_values.append(resource_value)
    else:
        if minute - cycle == cycle_diff:
            print("part 2:", resource_values[(1000000000-minute) % cycle_diff-1])
            break
        else:
            cycle_diff = minute - cycle
            cycle = minute
            resource_values = []

    minute += 1
