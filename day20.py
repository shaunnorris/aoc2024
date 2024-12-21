from aoclib import read_file_lines
import networkx as nx
import time
import scipy.spatial
import numpy as np
from collections import deque


def test_load_map():
    testdata = read_file_lines("day20-test.txt")
    assert load_map(testdata) == {'.': [(1, 1), (1, 2), (1, 3), (1, 5), (1, 6), (1, 7), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (2, 1), (2, 3), (2, 5), (2, 7), (2, 9), (2, 13), (3, 1), (3, 3), (3, 4), (3, 5), (3, 7), (3, 9), (3, 11), (3, 12), (3, 13), (4, 7), (4, 9), (4, 11), (5, 7), (5, 9), (5, 11), (5, 12), (5, 13), (6, 7), (6, 9), (6, 13), (7, 3), (7, 4), (7, 5), (7, 7), (7, 8), (7, 9), (7, 11), (7, 12), (7, 13), (8, 3), (8, 11), (9, 1), (9, 2), (9, 3), (9, 7), (9, 8), (9, 9), (9, 11), (9, 12), (9, 13), (10, 1), (10, 7), (10, 9), (10, 13), (11, 1), (11, 3), (11, 4), (11, 5), (11, 7), (11, 9), (11, 11), (11, 12), (11, 13), (12, 1), (12, 3), (12, 5), (12, 7), (12, 9), (12, 11), (13, 1), (13, 2), (13, 3), (13, 5), (13, 6), (13, 7), (13, 9), (13, 10), (13, 11)], '#': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (1, 0), (1, 4), (1, 8), (1, 14), (2, 0), (2, 2), (2, 4), (2, 6), (2, 8), (2, 10), (2, 11), (2, 12), (2, 14), (3, 0), (3, 2), (3, 6), (3, 8), (3, 10), (3, 14), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 8), (4, 10), (4, 12), (4, 13), (4, 14), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 8), (5, 10), (5, 14), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 8), (6, 10), (6, 11), (6, 12), (6, 14), (7, 0), (7, 1), (7, 2), (7, 6), (7, 10), (7, 14), (8, 0), (8, 1), (8, 2), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 12), (8, 13), (8, 14), (9, 0), (9, 4), (9, 5), (9, 6), (9, 10), (9, 14), (10, 0), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 8), (10, 10), (10, 11), (10, 12), (10, 14), (11, 0), (11, 2), (11, 6), (11, 8), (11, 10), (11, 14), (12, 0), (12, 2), (12, 4), (12, 6), (12, 8), (12, 10), (12, 12), (12, 13), (12, 14), (13, 0), (13, 4), (13, 8), (13, 12), (13, 13), (13, 14), (14, 0), (14, 1), (14, 2), (14, 3), (14, 4), (14, 5), (14, 6), (14, 7), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13), (14, 14)], 'S': (3, 1), 'E': (7, 5)}
    
def load_map(lines):
    mapdata = {'.':[],'#':[],'S':'','E':''}
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            if lines[r][c] == '#':
                mapdata['#'].append((r,c))
            elif lines[r][c] == '.':
                mapdata['.'].append((r,c))
            elif lines[r][c] == 'S':
                mapdata['S'] = (r,c)
                mapdata['.'].append((r,c))
            elif lines[r][c] == 'E':
                mapdata['E'] = (r,c)
                mapdata['.'].append((r,c))
    return mapdata

def test_build_lookup_table():
    mapdata = load_map(read_file_lines("day20-test.txt"))
    assert build_lookup_table(mapdata) == {(7, 5): 0, (7, 4): 1, (7, 3): 2, (8, 3): 3, (9, 3): 4, (9, 2): 5, (9, 1): 6, (10, 1): 7, (11, 1): 8, (12, 1): 9, (13, 1): 10, (13, 2): 11, (13, 3): 12, (12, 3): 13, (11, 3): 14, (11, 4): 15, (11, 5): 16, (12, 5): 17, (13, 5): 18, (13, 6): 19, (13, 7): 20, (12, 7): 21, (11, 7): 22, (10, 7): 23, (9, 7): 24, (9, 8): 25, (9, 9): 26, (10, 9): 27, (11, 9): 28, (12, 9): 29, (13, 9): 30, (13, 10): 31, (13, 11): 32, (12, 11): 33, (11, 11): 34, (11, 12): 35, (11, 13): 36, (10, 13): 37, (9, 13): 38, (9, 12): 39, (9, 11): 40, (8, 11): 41, (7, 11): 42, (7, 12): 43, (7, 13): 44, (6, 13): 45, (5, 13): 46, (5, 12): 47, (5, 11): 48, (4, 11): 49, (3, 11): 50, (3, 12): 51, (3, 13): 52, (2, 13): 53, (1, 13): 54, (1, 12): 55, (1, 11): 56, (1, 10): 57, (1, 9): 58, (2, 9): 59, (3, 9): 60, (4, 9): 61, (5, 9): 62, (6, 9): 63, (7, 9): 64, (7, 8): 65, (7, 7): 66, (6, 7): 67, (5, 7): 68, (4, 7): 69, (3, 7): 70, (2, 7): 71, (1, 7): 72, (1, 6): 73, (1, 5): 74, (2, 5): 75, (3, 5): 76, (3, 4): 77, (3, 3): 78, (2, 3): 79, (1, 3): 80, (1, 2): 81, (1, 1): 82, (2, 1): 83, (3, 1): 84}


def order_points(mapdata):
    S = mapdata['S']
    E = mapdata['E']
    points = set(mapdata['.'])

    # Initialize the queue with the starting point S
    queue = deque([S])

    # Initialize the ordered points list
    ordered_points = []

    # Perform BFS
    while queue:
        point = queue.popleft()
        ordered_points.append(point)

        # Add neighbors to the queue
        for neighbor in get_neighbors(point, points):
            if neighbor not in ordered_points:
                queue.append(neighbor)

    return ordered_points

def get_neighbors(point, points):
    x, y = point
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if (nx, ny) in points:
            neighbors.append((nx, ny))
    return neighbors

def calculate_distances(ordered_points, E):
    distances = {}
    for i, point in enumerate(ordered_points):
        distances[point] = len(ordered_points) - i - 1
    return distances

def build_lookup_table(mapdata):
    start_time = time.time()

    ordered_points = order_points(mapdata)
    distances = calculate_distances(ordered_points, mapdata['E'])
    finish_time = time.time()
    print(f"Lookup table built in {finish_time - start_time:.2f} seconds")
    return distances

def build_lookup_table_old(mapdata):
    lookup = {}
    points = mapdata['.']
    start_time = time.time()

    G = nx.Graph()
    G.add_nodes_from(points)

    for point in points:
        for neighbor in points:
            if point != neighbor and abs(point[0] - neighbor[0]) + abs(point[1] - neighbor[1]) == 1:
                G.add_edge(point, neighbor)

    path = nx.shortest_path(G, source=mapdata['S'], target=mapdata['E'], weight=None)
    path.reverse()
    for x in path:
        lookup[x] = path.index(x)
    lookup_time = time.time() - start_time
    print(f"Lookup table built in {lookup_time:.2f} seconds")
    return lookup
    


def test_find_pairs():
    testdata = load_map(read_file_lines("day20-test.txt"))
    assert len(find_pairs(testdata,2)) == 127
    
def find_pairs_old(mapdata, n=2):
    start_time = time.time()

    points = mapdata['.']
    pairs = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            if 2 <= distance <= n:
                if (points[i], points[j]) not in pairs and (points[j], points[i]) not in pairs:
                    pairs.append((points[i], points[j]))
    print(len(pairs))
    pair_time = time.time() - start_time
    print(f"Pair set built in {pair_time:.2f} seconds")
    return pairs

def find_pairs(mapdata, n=2):
    start_time = time.time()
    points = mapdata['.']
    pairs = set()

    # Use a k-d tree to quickly find nearby points
    kdtree = scipy.spatial.KDTree(points)

    for i, point in enumerate(points):
        # Find all points within a distance of n
        nearby_points = kdtree.query_ball_point(point, n)
        for nearby_index in nearby_points:
            if nearby_index != i:  # skip the point itself
                nearby_point = points[nearby_index]
                distance = abs(point[0] - nearby_point[0]) + abs(point[1] - nearby_point[1])
                if 2 <= distance <= n:
                    pairs.add(tuple(sorted((point, nearby_point))))
    end_time = time.time()
    print(f"Pair set built in {end_time - start_time:.2f} seconds")
    return pairs

def test_calc_cheat():
    testdata = load_map(read_file_lines("day20-test.txt"))
    assert calc_cheat(testdata,2,1) == 44
    assert calc_cheat(testdata,20,50) == 285
    
def calc_cheat_old(mapdata,n,threshold):
    start_time = time.time()
    lookup = build_lookup_table(mapdata)
    pairs = find_pairs(mapdata, n)
    cheats = []
    for pair in pairs:
        manhattan =  abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])
        cheat_distance = abs(lookup[pair[0]] - lookup[pair[1]]) - manhattan
        if cheat_distance >= threshold:
            cheats.append(cheat_distance)
    finish_time = time.time()
    print(f"Cheats calculated in {finish_time - start_time:.2f} seconds")
    return len(cheats)

def calc_cheat(mapdata,n,threshold):
    start_time = time.time()
    lookup = build_lookup_table(mapdata)
    pairs = find_pairs(mapdata, n)

    pair0 = np.array([pair[0] for pair in pairs])
    pair1 = np.array([pair[1] for pair in pairs])

    manhattan = np.abs(pair0[:, 0] - pair1[:, 0]) + np.abs(pair0[:, 1] - pair1[:, 1])
    lookup0 = np.array([lookup[tuple(x)] for x in pair0])
    lookup1 = np.array([lookup[tuple(x)] for x in pair1])
    cheat_distance = np.abs(lookup0 - lookup1) - manhattan

    cheats = np.where(cheat_distance >= threshold, cheat_distance, 0)

    finish_time = time.time()
    print(f"Cheats calculated in {finish_time - start_time:.2f} seconds")
    return np.count_nonzero(cheats)

mapdata = load_map(read_file_lines("day20-input.txt"))
part1 = calc_cheat(mapdata,2,100)
print('part1:',part1)
part2 = calc_cheat(mapdata,20,100)
print('part2:',part2)