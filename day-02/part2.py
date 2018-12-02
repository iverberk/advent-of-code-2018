from itertools import combinations
ids = open('input').read().split()

for first, second in combinations(ids, 2):
    pos = -1
    for index, letter in enumerate(first):
        if letter != second[index]:
            if pos >= 0:
                pos = -1
                break
            else:
                pos = index

    if pos >= 0:
        print(first[:pos] + first[pos+1:])
        break
