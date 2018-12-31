from collections import defaultdict, deque

WALL, ELF, GOBLIN = '#', 'E', 'G'

cave = defaultdict(lambda: '.')
units, walls = [], []


class Unit:

    def __init__(self, kind, x, y):
        self.kind = kind
        self.position = (x, y)

        self.hit_points = 200
        self.attack_power = 3

    def dead(self):
        return self.hit_points <= 0

    def enemies_in_range(self):
        enemies = []

        x, y = self.position
        neighbours = [(x, y-1), (x-1, y), (x+1, y), (x, y+1)]
        for neighbour in neighbours:
            enemy = cave[neighbour]
            if type(enemy) is Unit and enemy.kind != self.kind and not enemy.dead():
                enemies.append(enemy)

        return enemies

    def move(self, enemies):
        if self.dead():
            return

        # Calculate eligible target positions
        targets = []
        enemies = [u for u in units if self.kind != u.kind and not u.dead()]
        for enemy in enemies:
            x, y = enemy.position
            neighbours = [(x, y-1), (x-1, y), (x+1, y), (x, y+1)]
            targets += [n for n in neighbours if cave[n] == '.' or n == self.position]

        # Bail if we are already on a target square
        if self.position in targets:
            return

        # Find shortest path to the targets with BFS
        seen, paths = {self.position}, []
        frontier = deque([(self.position, [])])
        while frontier:
            current, path = frontier.popleft()
            seen.add(current)

            x, y = current
            neighbours = [(x, y-1), (x-1, y), (x+1, y), (x, y+1)]
            for neighbour in neighbours:
                if neighbour in seen or cave[neighbour] != '.':
                    continue

                if neighbour in targets:
                    paths.append((neighbour, path + [current, neighbour]))

                frontier.append((neighbour, path + [current]))
                seen.add(neighbour)

        # Bail if no paths are found
        if not len(paths):
            return

        # Sort on length of path and target position
        p = sorted(paths, key=lambda p: (len(p[1]), p[0][::-1]))

        # Return first step of selected target and path
        self.position = p[0][1][1]
        refresh_cave()

    def hit(self, power):
        self.hit_points -= power

        if self.hit_points <= 0:
            self.hit_points = 0
            refresh_cave()

    def attack(self, enemies):
        if self.dead():
            return

        enemy = min(enemies, key=lambda e: (e.hit_points, e.position[::-1]))
        enemy.hit(self.attack_power)


def refresh_cave():
    cave.clear()

    for unit in units:
        if not unit.dead():
            cave[unit.position] = unit

    for wall in walls:
        cave[wall] = WALL


def draw_cave(dimension=32):

    for y in range(dimension):
        for x in range(dimension):
            object = cave[(x, y)]
            if type(object) == Unit:
                object = object.kind
            print(object, end='')
        print()


with open('input') as f:
    lines = [line.rstrip() for line in f]

    for y, line in enumerate(lines):
        for x, object in enumerate(line):
            unit = None
            if object in [ELF, GOBLIN]:
                units.append(Unit(object, x, y))
            elif object == WALL:
                walls.append((x, y))

    refresh_cave()

rounds = 0
done = False
while not done:

    units.sort(key=lambda unit: unit.position[::-1])

    for unit in units:
        if unit.dead():
            continue

        unit.move(units)

        enemies = unit.enemies_in_range()
        if enemies:
            unit.attack(enemies)

        elves = [u for u in units if u.kind == ELF and not u.dead()]
        goblins = [u for u in units if u.kind == GOBLIN and not u.dead()]

        if not elves or not goblins:
            done = True

            # Check if last unit wiped out the enemy, in
            # which case we need to count it as a full round.
            if unit == units[-1]:
                rounds += 1
            break

    if not done:
        rounds += 1

total_hit_points = sum([u.hit_points for u in units])

print(rounds, total_hit_points, rounds*total_hit_points)
