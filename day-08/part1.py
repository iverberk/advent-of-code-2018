def input():
    for c in open('input').read().split():
        yield int(c)


input = input()


def meta_sum():
    children, metadata = next(input), next(input)

    s = 0
    for _ in range(children):
        s += meta_sum()

    for _ in range(metadata):
        s += next(input)

    return s


print(meta_sum())
