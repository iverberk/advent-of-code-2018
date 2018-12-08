def input():
    for c in open('input').read().split():
        yield int(c)


input = input()


def value():
    children, metadata = next(input), next(input)

    s = 0
    child_values = [0]
    for _ in range(children):
        child_values.append(value())

    for _ in range(metadata):
        meta = next(input)
        if not children:
            s += meta
        else:
            if meta > 0 and meta < len(child_values):
                s += child_values[meta]

    return s


print(value())
