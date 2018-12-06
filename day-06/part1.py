from collections import defaultdict


def X(point):
    x, y = point
    return x


def Y(point):
    x, y = point
    return y


def manhattan_distance(p1, p2):
    return abs(X(p2) - X(p1)) + abs(Y(p2) - Y(p1))


coordinates = {}
max_x, max_y = 0, 0
with open('input') as f:
    for index, coordinate in enumerate(f):
        (x, y) = list(map(int, coordinate.strip().split(',')))
        max_x, max_y = max(max_x, x), max(max_y, y)
        coordinates[(x, y)] = index

counts = defaultdict(int)
infinite = set()
for y in range(0, max_y+1):
    for x in range(0, max_x+1):
        min_distance = max_x + max_y
        min_index = 0
        distances = []
        for coordinate, index in coordinates.items():
            distance = manhattan_distance((x, y), coordinate)
            distances.append(distance)

            if distance < min_distance:
                min_distance = distance
                min_index = index

        distances.sort()

        if distances[0] != distances[1]:
            counts[min_index] += 1

            if x == 0 or x == max_x or y == 0 or y == max_y:
                infinite.add(min_index)

print(max({k: v for k, v in counts.items() if k not in infinite}.values()))
