from collections import defaultdict


class Marbles:

    class Marble:

        def __init__(self, number):
            self.number = number
            self.next = self
            self.prev = self

    def __init__(self):
        marble = self.Marble(0)

        self.start = marble
        self.current = marble

    def move(self, amount, clockwise=True):
        for _ in range(amount):
            if clockwise:
                self.current = self.current.next
            else:
                self.current = self.current.prev

    def insert(self, number):
        marble = self.Marble(number)

        marble.prev = self.current
        marble.next = self.current.next

        self.current.next.prev = marble
        self.current.next = marble

        self.current = marble

        if self.current.prev == self.start:
            self.start.next = self.current

        if self.current.next == self.start:
            self.start.prev = self.current

    def remove(self):
        score = self.current.number

        if self.start == self.current:
            self.start = self.current.next

        self.current.prev.next = self.current.next
        self.current.next.prev = self.current.prev

        self.current = self.current.next

        return score


players = defaultdict(int)
marbles = Marbles()
num_players = 405
for number in range(1, 70953*100):

    player = number % num_players

    if not number % 23 == 0:
        marbles.move(1)
        marbles.insert(number)
    else:
        players[player] += number
        marbles.move(7, False)
        players[player] += marbles.remove()

print(players[max(players, key=players.get)])
