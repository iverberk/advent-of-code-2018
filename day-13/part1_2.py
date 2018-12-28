from itertools import cycle
import operator

TRACK_FILE = 'input'

# Check the width of the track to calculate priority
WIDTH = len(max(open(TRACK_FILE, 'r'), key=len))

UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
DELTAS = {UP: (0, -1), RIGHT: (1, 0), DOWN: (0, 1), LEFT: (-1, 0)}

tracks = {}
carts = []


class Cart:

    def __init__(self, id, x, y, direction):
        self.id = id
        self.turn = cycle([-1, 0, 1])
        self.position = (x, y)
        self.direction = direction

    def move(self):

        if tracks[self.position] == '+':
            self.direction = (self.direction + next(self.turn)) % 4

        if tracks[self.position] == '/':
            if self.direction == UP:
                self.direction = RIGHT
            elif self.direction == DOWN:
                self.direction = LEFT
            elif self.direction == LEFT:
                self.direction = DOWN
            elif self.direction == RIGHT:
                self.direction = UP

        if tracks[self.position] == '\\':
            if self.direction == UP:
                self.direction = LEFT
            elif self.direction == DOWN:
                self.direction = RIGHT
            elif self.direction == LEFT:
                self.direction = UP
            elif self.direction == RIGHT:
                self.direction = DOWN

        self.position = tuple(
            map(operator.add, self.position, DELTAS[self.direction]))

        return self.position

    def priority(self):
        x, y = self.position
        return x*WIDTH+y


cart_id = 1
with open(TRACK_FILE) as f:
    for row, line in enumerate(f):
        for column, track in enumerate(line.rstrip()):
            if track == '>':
                carts.append(Cart(cart_id, column, row, RIGHT))
            elif track == '<':
                carts.append(Cart(cart_id, column, row, LEFT))
            elif track == '^':
                carts.append(Cart(cart_id, column, row, UP))
            elif track == 'v':
                carts.append(Cart(cart_id, column, row, DOWN))

            if track in "<>^v":
                cart_id += 1

            tracks[(column, row)] = track

crashed = []
while True:
    carts = [cart for cart in carts if cart.id not in crashed]

    if len(carts) < 2:
        if len(carts) == 1:
            print("Final cart is at:", carts[0].position)
        else:
            print("All carts destroyed!")
        break

    carts.sort(key=lambda cart: cart.priority())

    for cart in carts:
        positions = {cart.position: cart.id for cart in carts}
        position = cart.move()
        if position in positions.keys():
            crashed.extend([cart.id, positions[position]])
            if len(crashed) == 2:
                print("First crash at:", position)
