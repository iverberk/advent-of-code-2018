pots, notes = [], {}
with open('input') as f:
    pots = f.readline().split(':')[1].strip()
    for line in f:
        if not line.strip():
            continue

        note, result = line.strip().split(' => ')
        notes[note] = result


def total(pots):
    total = 0
    for index, pot in enumerate(pots):
        if pot == '#':
            total += index+offset

    return total


offset = 0
previous_pots = [pots]
previous_pots_total = total(pots)
generations = 50000000000
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
            # Check if a new plant grew on the left side
            if not first_plant and result == '#':
                offset -= 1
                first_plant = current_index

        # Check if the first plant disappeared
        if first_plant == current_index and result == '.':
            offset += 1

        new_pots += result

    pots = new_pots.strip('.')

    if pots in previous_pots:
        latest_total = total(pots)

        # Calculate the steady increase
        difference = latest_total - previous_pots_total

        # Calculate the remaining generations fast
        print(latest_total + ((generations-generation-1) * difference))
        break

    previous_pots.append(pots)
    previous_pots_total = total(pots)
    generation += 1
