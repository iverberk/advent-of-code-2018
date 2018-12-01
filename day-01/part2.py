changes = []
with open('input') as f:
    for change in f:
        changes.append(int(change))

frequency = 0
frequencies = set()
while True:
    for change in changes:
        frequencies.add(frequency)
        frequency += change
        if frequency in frequencies:
            print(frequency)
            quit()
