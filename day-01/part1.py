frequency = 0
with open('input') as f:
    for change in f:
        frequency += int(change)

print(frequency)
