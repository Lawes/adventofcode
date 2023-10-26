from collections import defaultdict, Counter


def load_input(filename):
    graph = defaultdict(set)
    with open(filename, 'r') as f:
        for line in f:
            n1, n2 = line.strip().split('-')

            graph[n1].add(n2)
            graph[n2].add(n1)
    return graph


def isSmallCave(name):
    return name.lower() == name


final_path = []

def path_to_end(s, graph, path):
    if s == 'end':
        newp = path.copy()
        newp.append(s)
        final_path.append(newp)
    else:
        newp = path.copy()
        newp.append(s)
        for n in graph[s]:
            if isSmallCave(n) and n in path:
                continue
            path_to_end(n, graph, newp)


def path_to_end2(s, graph, path):
    if s == 'end':
        newp = path.copy()
        newp.append(s)
        final_path.append(newp)
    else:
        newp = path.copy()
        newp.append(s)
        count_small = Counter((ns for ns in newp if isSmallCave(ns)))
        for n in graph[s]:
            if n == 'start' and n in path:
                continue

            if n in count_small:
                if max(count_small.values()) == 2 and count_small[n] >= 1:
                    continue
            path_to_end2(n, graph, newp)



if __name__ == '__main__':
    g = load_input('input')

    print(g)

    node = 'start'

    path_to_end2(node, g, [])

    print(len(final_path))




