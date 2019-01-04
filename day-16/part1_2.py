from collections import defaultdict
import re


def update(registers, index, value):
    registers[index] = value


instructions = {
    'addr': lambda r, A, B, C: update(r, C, r[A]+r[B]),
    'addi': lambda r, A, B, C: update(r, C, r[A]+B),

    'mulr': lambda r, A, B, C: update(r, C, r[A]*r[B]),
    'muli': lambda r, A, B, C: update(r, C, r[A]*B),

    'banr': lambda r, A, B, C: update(r, C, r[A] & r[B]),
    'bani': lambda r, A, B, C: update(r, C, r[A] & B),

    'borr': lambda r, A, B, C: update(r, C, r[A] | r[B]),
    'bori': lambda r, A, B, C: update(r, C, r[A] | B),

    'setr': lambda r, A, B, C: update(r, C, r[A]),
    'seti': lambda r, A, B, C: update(r, C, A),

    'gtir': lambda r, A, B, C: update(r, C, 1 if A > r[B] else 0),
    'gtri': lambda r, A, B, C: update(r, C, 1 if r[A] > B else 0),
    'gtrr': lambda r, A, B, C: update(r, C, 1 if r[A] > r[B] else 0),

    'eqir': lambda r, A, B, C: update(r, C, 1 if A == r[B] else 0),
    'eqri': lambda r, A, B, C: update(r, C, 1 if r[A] == B else 0),
    'eqrr': lambda r, A, B, C: update(r, C, 1 if r[A] == r[B] else 0),
}

samples = defaultdict(list)
program = []
r = r'[^\d ]'
with open('input', 'r') as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        if line.startswith('Before'):
            before = [int(d) for d in re.sub(r, '', line).split()]
            number, A, B, C = [int(d) for d in f.readline().split()]
            after = [int(d) for d in re.sub(r, '', f.readline()).split()]

            samples[(number, A, B, C)].append({'before': before, 'after': after})
        else:
            program.append(map(int, line.split()))

opcodes = {}
while len(opcodes) < 16:
    n = 0
    for instruction, registers in samples.items():

        number, A, B, C = instruction
        matched = []
        for register in registers:

            matches = set()
            num_matches = 0
            for opcode in instructions.keys():
                sample = register['before'].copy()
                instructions[opcode](sample, A, B, C)

                if sample == register['after']:
                    num_matches += 1
                    if opcode not in opcodes.values():
                        matches.add(opcode)

            if num_matches >= 3:
                n += 1

            matched.append(matches)

        # Find the common opcode
        if matched:
            opcode = matched[0].intersection(*matched[1:])

            # We found a unique opcode that belongs to this number
            if len(opcode) == 1:
                opcodes[number] = next(iter(opcode))

registers = [0, 0, 0, 0]
for instruction in program:
    number, A, B, C = instruction
    instructions[opcodes[number]](registers, A, B, C)

print("part 1:", n, "\npart 2:", registers[0])
