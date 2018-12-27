pots, notes = [], {}
with open('input') as f:
    pots = f.readline().split(':')[1].strip()
    for line in f:
        if not line.strip():
            continue

        note, result = line.strip().split(' => ')
        notes[note] = result

offset = 0
generations = 20
for generation in range(generations):

    # Make sure there are enough empty pots on either side
    pots = '.....' + pots + '.....'

    new_pots = ""
    first_plant = False
    for index in range(0, len(pots)-2):
        sequence = pots[index:index+5]

        current = sequence[2]
        current_index = index+2

        if current == '#' and not first_plant:
            first_plant = current_index

        result = '.'
        if sequence in notes:
            result = notes[sequence]
            if not first_plant and result == '#':
                offset -= 1
                first_plant = current_index

        if first_plant == current_index and result == '.':
            offset += 1

        new_pots += result

    pots = new_pots.strip('.')

total = 0
for index, pot in enumerate(pots):
    if pot == '#':
        total += index+offset

print(pots, total)
