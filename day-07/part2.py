import networkx as nx

G = nx.DiGraph()
with open('test') as f:
    for line in f:
        instruction = line.strip().split()
        G.add_edge(instruction[1], instruction[7])

elves = {}
seconds = 0
while len(G):
    nodes = [v for v, d in G.in_degree() if d == 0]

    removed = False
    for node in nodes:
        if node in elves:
            elves[node] -= 1
            if not elves[node]:
                removed = True
                G.remove_node(node)
                del elves[node]
        elif len(elves) < 2:
            elves[node] = ord(node) - 64

    # Re-evaluate if we removed a node
    # Reset timings for elves
    if removed:
        for node in nodes:
            if node in elves:
                elves[node] += 1
    else:
        seconds += 1

print(seconds)
