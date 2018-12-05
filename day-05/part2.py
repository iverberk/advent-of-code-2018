input = open('input').readline().strip()

units = set(input.lower())
lengths = []

for unit in units:
    polymer = input.replace(unit, '').replace(unit.swapcase(), '')
    index = 0
    while index < len(polymer)-1:
        if polymer[index] == polymer[index+1].swapcase():
            polymer = polymer[:index] + polymer[index+2:]
            if index > 0:
                index -= 1
        else:
            index += 1
    lengths.append(len(polymer))

print(min(lengths))
