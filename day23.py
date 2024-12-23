from aoclib import read_file_lines
from itertools import combinations
from collections import defaultdict


def test_load_pairs():
    testdata = read_file_lines('day23-test.txt')
    assert len(load_pairs(testdata)) == 32
    
def load_pairs(lines):
    pairs = []
    for line in lines:
        left, right = line.split('-')
        pairs.append((left.strip(), right.strip()))
    return pairs

def test_count_tgroups():
    testdata = read_file_lines('day23-test.txt')
    pairs = load_pairs(testdata)
    assert count_tgroups(pairs) == 7
    
def count_tgroups_old(pairs):
    
    groups = []
    tgroups = []
    for pair in pairs:
        l1,r1 = pair
        for pair2 in pairs:
            if pair != pair2:
                l2,r2 = pair2
                for pair3 in pairs:
                    if pair3 != pair and pair3 != pair2:
                        l3,r3 = pair3
                        pointlist = [l1,r1,l2,r2,l3,r3]
                        unique = sorted(list(set(pointlist)))
                        if len(unique) == 3:
                            if unique not in groups:
                                groups.append(unique)
                                for item in unique:
                                    if item[0] == 't':
                                        if unique not in tgroups:
                                            tgroups.append(unique)
    print(tgroups)
    return len(tgroups)

def count_tgroups(edges):
    # Build adjacency list
    adjacency = defaultdict(set)
    for edge in edges:
        a, b = edge
        adjacency[a].add(b)
        adjacency[b].add(a)
    
    # Find triangles
    triangles = set()
    for a, b in edges:
        # Check common neighbors between a and b
        common_neighbors = adjacency[a].intersection(adjacency[b])
        for c in common_neighbors:
            # Sort to ensure uniqueness (e.g., {A, B, C} == {C, B, A})
            triangle = tuple(sorted([a, b, c]))
            if "t" in [a[0], b[0], c[0]]:
                triangles.add(triangle)
    
    return len(triangles)

def test_largest_connected_group():
    testdata = read_file_lines('day23-test.txt')
    pairs = load_pairs(testdata)
    assert largest_clique(pairs) == 'co,de,ka,ta'


def largest_clique(edges):
    # Build adjacency list
    adjacency = defaultdict(set)
    for edge in edges:
        a, b = edge
        adjacency[a].add(b)
        adjacency[b].add(a)

    # Function to find cliques using Bron-Kerbosch algorithm
    def bron_kerbosch(r, p, x):
        if not p and not x:
            cliques.append(r)
            return
        for node in list(p):
            bron_kerbosch(r | {node}, p & adjacency[node], x & adjacency[node])
            p.remove(node)
            x.add(node)

    # Initialize variables
    cliques = []
    nodes = set(adjacency.keys())

    # Execute Bron-Kerbosch algorithm
    bron_kerbosch(set(), nodes, set())

    # Find the largest clique
    largest_clique = max(cliques, key=len, default=set())
    output_str = ','.join(sorted(list(largest_clique)))
    return output_str



pairdata = read_file_lines('day23-input.txt')
part1 = count_tgroups(load_pairs(pairdata))
print('part1:',part1)
part2 = largest_clique(load_pairs(pairdata))
print('part2:',part2)