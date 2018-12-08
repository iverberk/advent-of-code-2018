import networkx as nx

G = nx.DiGraph()
with open('input') as f:
    for line in f:
        instruction = line.strip().split()
        G.add_edge(instruction[1], instruction[7])

print("".join(list(nx.lexicographical_topological_sort(G))))
