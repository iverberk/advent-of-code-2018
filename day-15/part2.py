from collections import defaultdict, deque

WALL, ELF, GOBLIN = '#', 'E', 'G'

cave = defaultdict(lambda: '.')
units = []


class Unit:

    def __init__(self, kind, x, y, attack_power=3):
        self.kind = kind
        self.original = (x, y)
        self.position = (x, y)

        self.hit_points = 200
        self.attack_power = attack_power

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
        cave[self.position] = '.'
        self.position = p[0][1][1]
        cave[self.position] = self

    def hit(self, power):
        self.hit_points -= power

        if self.hit_points <= 0:
            self.hit_points = 0
            cave[self.position] = '.'

    def attack(self, enemies):
        if self.dead():
            return

        enemy = min(enemies, key=lambda e: (e.hit_points, e.position[::-1]))
        enemy.hit(self.attack_power)


def draw_cave(dimension=32):

    for y in range(dimension):
        for x in range(dimension):
            object = cave[(x, y)]
            if type(object) == Unit:
                object = object.kind
            print(object, end='')
        print()


lines = []
with open('input') as f:
    lines = [line.rstrip() for line in f]

    for y, line in enumerate(lines):
        for x, object in enumerate(line):
            unit = None
            if object in [ELF, GOBLIN]:
                unit = Unit(object, x, y)
                units.append(unit)
                cave[(x, y)] = unit
            elif object == WALL:
                cave[(x, y)] = WALL

rounds = 0
done = False
elf_attack_power = 4
num_elves = len([u for u in units if u.kind == ELF])
increase_power = False
while not done:

    if increase_power:
        rounds = 0
        elf_attack_power += 1
        increase_power = False

        units = []
        cave.clear()
        for y, line in enumerate(lines):
            for x, object in enumerate(line):
                unit = None
                if object == ELF:
                    unit = Unit(object, x, y, elf_attack_power)
                    units.append(unit)
                    cave[(x, y)] = unit
                elif object == GOBLIN:
                    unit = Unit(object, x, y)
                    units.append(unit)
                    cave[(x, y)] = unit
                elif object == WALL:
                    cave[(x, y)] = WALL

    units.sort(key=lambda unit: unit.position[::-1])

    for unit in units:
        if unit.dead():
            continue

        unit.move(units)

        enemies = unit.enemies_in_range()
        if enemies:
            unit.attack(enemies)

        goblins = [u for u in units if u.kind == GOBLIN and not u.dead()]
        elves = [u for u in units if u.kind == ELF and not u.dead()]
        if len(elves) < num_elves:
            increase_power = True
            break

        if not goblins:
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
