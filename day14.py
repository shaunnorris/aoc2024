from aoclib import read_file_lines, tuple_add

def test_get_robots():
    testdata = read_file_lines('day14-test.txt')
    assert get_robots(testdata) == [
        {"p": (0, 4), "v": (3, -3)},
        {"p": (6, 3), "v": (-1, -3)},
        {"p": (10, 3), "v": (-1, 2)},
        {"p": (2, 0), "v": (2, -1)},
        {"p": (0, 0), "v": (1, 3)},
        {"p": (3, 0), "v": (-2, -2)},
        {"p": (7, 6), "v": (-1, -3)},
        {"p": (3, 0), "v": (-1, -2)},
        {"p": (9, 3), "v": (2, 3)},
        {"p": (7, 3), "v": (-1, 2)},
        {"p": (2, 4), "v": (2, -3)},
        {"p": (9, 5), "v": (-3, -3)},
    ]


def get_robots(data):
    robots = []
    for line in data:
        p,v = line.split(' ')
        p = p.split('=')[1]
        x, y = p.split(',')
        v = v.split('=')[1]
        vx, vy = v.split(',')
        robots.append({'p':(int(x), int(y)), 'v':(int(vx),int(vy))})
    return robots

def test_check_pos():
    testrobots = get_robots(read_file_lines('day14-test.txt'))
    testpos = {
        (0, 6): 2,
        (0, 9): 1,
        (2, 0): 1,
        (3, 1): 1,
        (3, 2): 1,
        (4, 5): 1,
        (5, 3): 1,
        (5, 4): 2,
        (6, 1): 1,
        (6, 6): 1,
    }
    assert check_pos(testrobots,(11,7),100) == testpos
    
def check_pos(robots,size,seconds):
    newpos = {}
    for robot in robots:
        p, v = robot['p'], robot['v']
        dx, dy = v[0] * seconds, v[1] * seconds
        grossp = tuple_add(p, (dx, dy))
        actualpx = (grossp[0] % size[0] + size[0]) % size[0]
        actualpy = (grossp[1] % size[1] + size[1]) % size[1]
        if (actualpy,actualpx) in newpos:
            newpos[(actualpy,actualpx)] += 1
        else:
            newpos[(actualpy,actualpx)] = 1
    return(newpos)

def test_calc_safety():
    testpos = {
        (0, 6): 2,
        (0, 9): 1,
        (2, 0): 1,
        (3, 1): 1,
        (3, 2): 1,
        (4, 5): 1,
        (5, 3): 1,
        (5, 4): 2,
        (6, 1): 1,
        (6, 6): 1,
    }
    assert calc_safety(testpos,(7,11)) == 12

def calc_safety(pos,size):
    qcount = {'q0':0,'q1':0,'q2':0,'q3':0}
    q0 = ((0,0),(size[0] //2-1,size[1] //2-1 ))
    q1 =  ((0,size[1] // 2 +1),(size[0] //2-1,size[1]  ))
    q2 =  (size[0]//2+1,0),(size[0] ,size[1] //2-1 )
    q3 =  ((size[0] //2 + 1,size[1] //2 +1),(size[0] ,size[1]  ))
    for coord,spotcount in pos.items():
        if coord[0] in range(q0[0][0],q0[1][0]+1) and coord[1] in range(q0[0][1],q0[1][1]+1):
            qcount['q0'] += spotcount
        elif coord[0] in range(q1[0][0],q1[1][0]+1) and coord[1] in range(q1[0][1],q1[1][1]+1):
            qcount['q1'] += spotcount
        elif coord[0] in range(q2[0][0],q2[1][0]+1) and coord[1] in range(q2[0][1],q2[1][1]+1):
            qcount['q2'] += spotcount
        elif coord[0] in range(q3[0][0],q3[1][0]+1) and coord[1] in range(q3[0][1],q3[1][1]+1):
            qcount['q3'] += spotcount
    return qcount['q0'] * qcount['q1'] * qcount['q2'] * qcount['q3']



def print_tree(pos,size):
    for y in range(size[1]):
        line = ''
        for x in range(size[0]):
            if (y,x) in pos:
                line = line + str(pos[(y,x)])
            else:
                line = line + '.'
        print(line)

def test_count_blobs():
    testpos = {
        (0, 6): 2,
        (0, 7): 1,
        (1, 5): 1,
        (1, 6): 1,
    }
    testpos2 = {
        (0, 6): 2,
        (0, 9): 1,
        (2, 0): 1,
        (3, 1): 1,
        (3, 2): 1,
        (4, 5): 1,
        (5, 3): 1,
        (5, 4): 2,
        (6, 1): 1,
        (6, 6): 1,
    }
    assert count_blobs(testpos) == (1,4)
    assert count_blobs(testpos2) == (8,2)
    
def count_blobs(pos):
    # Create a set of coordinates for efficient lookups
    coordinates = pos.keys()
    coords_set = set(coordinates)

    # Initialize count of contiguous regions
    count = 0

    # Initialize size of largest region
    largest_region_size = 0

    # Iterate over all coordinates
    for x, y in coordinates:
        # If this coordinate is not yet visited (i.e., not in a region)
        if (x, y) in coords_set:
            # Perform flood fill from this coordinate and get the size of the region
            region_size = flood_fill(coords_set, x, y)
            # Update the size of the largest region if necessary
            largest_region_size = max(largest_region_size, region_size)
            # Increment count of contiguous regions
            count += 1

    return count, largest_region_size

def flood_fill(coords_set, x, y):
    # Directions to explore (up, down, left, right)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Create a stack for DFS
    stack = [(x, y)]

    # Initialize size of the region
    region_size = 0

    while stack:
        x, y = stack.pop()
        # If this coordinate is still in the set (i.e., not yet visited)
        if (x, y) in coords_set:
            # Mark it as visited by removing it from the set
            coords_set.remove((x, y))
            # Increment the size of the region
            region_size += 1
            # Explore neighbors
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                # If neighbor is in the set (i.e., contiguous)
                if (nx, ny) in coords_set:
                    # Add it to the stack for further exploration
                    stack.append((nx, ny))

    return region_size


robots = get_robots(read_file_lines('day14-input.txt'))
size = (103,101)
rsize = (101,103)
part1 = calc_safety(check_pos(robots,rsize,100),size)
print('part1:',part1)

def find_tree():
  
    for s in range(10000):
        pos = check_pos(robots,rsize,s)
        total_robots = sum(pos.values())
        threshold = 0.3 * total_robots
        if count_blobs(pos)[1] > threshold:
            print('part2:',s)
            print_tree(pos,rsize)
            break
find_tree()