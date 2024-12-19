from aoclib import read_file_lines, get_mapsize, in_bounds, tuple_add
import heapq

def test_load_map():
    test1 = read_file_lines("day16-test1.txt")
    assert len(load_map(test1)["."]) == 104
    assert len(load_map(test1)["#"]) == 121


def load_map(maplines):
    mapdata = {"S": "", "E": "", ".": [], "#": []}

    for i in range(len(maplines)):
        for j in range(len(maplines[0])):
            if maplines[i][j] == "S":
                mapdata["S"] = (i, j)
                mapdata["."].append((i, j))
            elif maplines[i][j] == "E":
                mapdata["E"] = (i, j)
                mapdata["."].append((i, j))
            elif maplines[i][j] == ".":
                mapdata["."].append((i, j))
            elif maplines[i][j] == "#":
                mapdata["#"].append((i, j))
    return mapdata


def test_bfs_lowest_score_path():
    testmap1 = load_map(read_file_lines("day16-test1.txt"))
    assert bfs_lowest_score_paths(testmap1) == (7036, 45)

def bfs_lowest_score_paths(mapdata):
    start = mapdata['S']
    end = mapdata['E']
    coords = mapdata['.']
    # Directions and their vector equivalents
    directions = {
        "N": (0, -1),
        "S": (0, 1),
        "E": (1, 0),
        "W": (-1, 0)
    }
    
    # Priority queue (min-heap): (current_score, current_node, current_direction, path_so_far)
    pq = [(0, start, "E", [start])]  # Start facing East
    
    # Dictionary to store the lowest score for each node with a given direction
    min_scores = {(coord, direction): float('inf') for coord in coords for direction in directions}
    min_scores[(start, "E")] = 0

    # Store all optimal paths
    best_paths = []
    best_score = float('inf')

    while pq:
        # Get the coordinate with the lowest score
        current_score, current_node, current_direction, path = heapq.heappop(pq)

        # If we exceed the best score, skip processing
        if current_score > best_score:
            continue

        # If we reach the end node
        if current_node == end:
            if current_score < best_score:
                best_score = current_score
                best_paths = [path]  # Reset with the new best path
            elif current_score == best_score:
                best_paths.append(path)
            continue

        # Explore all possible moves
        for new_direction, vector in directions.items():
            # Calculate the new position
            new_node = (current_node[0] + vector[0], current_node[1] + vector[1])
            
            if new_node not in coords:
                continue  # Skip if the new position is not valid
            
            # Calculate the score for this move
            move_cost = 1  # Forward movement cost
            turn_cost = 1000 if new_direction != current_direction else 0
            total_cost = current_score + move_cost + turn_cost

            # If a lower score path to the new node with the new direction is found
            if total_cost < min_scores[(new_node, new_direction)]:
                min_scores[(new_node, new_direction)] = total_cost
                heapq.heappush(pq, (total_cost, new_node, new_direction, path + [new_node]))
            elif total_cost == min_scores[(new_node, new_direction)]:
                # If the score is the same, add it to the queue for exploration
                heapq.heappush(pq, (total_cost, new_node, new_direction, path + [new_node]))

    # Return all best paths and the best score
    unique_points = []
    for path in best_paths:
        for point in path:
            if point not in unique_points:
                unique_points.append(point)
    return best_score, len(unique_points)

mapdata = load_map(read_file_lines("day16-input.txt"))
part1,part2 = bfs_lowest_score_paths(mapdata)
print('part1:',part1)
print('part2:',part2)

