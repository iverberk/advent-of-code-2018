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

region = 0
for y in range(0, max_y):
    for x in range(0, max_x):
        total_distance = 0
        for coordinate, index in coordinates.items():
            total_distance += manhattan_distance((x, y), coordinate)
        if total_distance < 10000:
            region += 1

print(region)
