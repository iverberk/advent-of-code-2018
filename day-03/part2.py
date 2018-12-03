import re
import numpy as np

fabric = np.zeros((1000, 1000))
mask = np.zeros((1000, 1000))
claims = {}

with open('input') as f:
    for claim in f:
        m = re.match(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", claim)

        id = int(m.group(1))
        left = int(m.group(2))
        top = int(m.group(3))
        width = int(m.group(4))
        height = int(m.group(5))

        claims[id] = width*height

        mask[left:left+width, top:top+height] += 1
        fabric[left:left+width, top:top+height] = id

fabric = fabric[(mask == 1)]
for id, area in claims.items():
    if (fabric == id).sum() == area:
        print(id)
