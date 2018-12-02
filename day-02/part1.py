from collections import Counter

twos = 0
threes = 0
ids = open('input').read().split()

for id in ids:
    c = Counter(id)
    two, three = False, False
    for _, value in c.items():

        if value == 2 and not two:
            twos += 1
            two = True

        if value == 3 and not three:
            threes += 1
            three = True

        if two and three:
            break

print(twos * threes)
