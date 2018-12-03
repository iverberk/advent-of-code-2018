import re
import numpy as np

fabric = np.zeros((1000, 1000))

with open('input') as f:
    for claim in f:
        m = re.match(r"#\d+ @ (\d+),(\d+): (\d+)x(\d+)", claim)

        left = int(m.group(1))
        top = int(m.group(2))
        width = int(m.group(3))
        height = int(m.group(4))

        fabric[left:left+width, top:top+height] += 1

print((fabric > 1).sum())
