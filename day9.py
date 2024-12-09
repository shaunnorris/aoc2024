from aoclib import read_file_lines

def test_unpack_disk():
    assert unpack_disk(read_file_lines("day9-test.txt")) == [
        0,
        0,
        ".",
        ".",
        ".",
        1,
        1,
        1,
        ".",
        ".",
        ".",
        2,
        ".",
        ".",
        ".",
        3,
        3,
        3,
        ".",
        4,
        4,
        ".",
        5,
        5,
        5,
        5,
        ".",
        6,
        6,
        6,
        6,
        ".",
        7,
        7,
        7,
        ".",
        8,
        8,
        8,
        8,
        9,
        9,
    ]


def unpack_disk(data):
    disk = []
    for index,char in enumerate(data[0]):
        for i in range(int(char)):
            if index % 2 == 0:
                disk.append(index // 2)
            else:
                disk.append('.')
    return disk

def test_compact_disk():
    assert compact_disk(
        [
            0,
            0,
            ".",
            ".",
            ".",
            1,
            1,
            1,
            ".",
            ".",
            ".",
            2,
            ".",
            ".",
            ".",
            3,
            3,
            3,
            ".",
            4,
            4,
            ".",
            5,
            5,
            5,
            5,
            ".",
            6,
            6,
            6,
            6,
            ".",
            7,
            7,
            7,
            ".",
            8,
            8,
            8,
            8,
            9,
            9,
        ]
    ) == [
        0,
        0,
        9,
        9,
        8,
        1,
        1,
        1,
        8,
        8,
        8,
        2,
        7,
        7,
        7,
        3,
        3,
        3,
        6,
        4,
        4,
        6,
        5,
        5,
        5,
        5,
        6,
        6,
    ]


def compact_disk(diskdata):
    newdisk = diskdata[:]
    freespace = [i for i, x in enumerate(newdisk) if x == '.']
    while len(freespace) > 0:
        lastblock = newdisk.pop()
        if lastblock != '.':
            newdisk[freespace[0]] = lastblock
        freespace = [i for i, x in enumerate(newdisk) if x == '.']
    return newdisk

def test_get_checksum():
    assert (
        get_checksum(
            [
                0,
                0,
                9,
                9,
                8,
                1,
                1,
                1,
                8,
                8,
                8,
                2,
                7,
                7,
                7,
                3,
                3,
                3,
                6,
                4,
                4,
                6,
                5,
                5,
                5,
                5,
                6,
                6,
            ]
        )
        == 1928
    )

def get_checksum(diskdata):
    checksum = 0
    for index,value in enumerate(diskdata):
        checksum += value * index
    return checksum

disk = unpack_disk(read_file_lines("day9-input.txt"))
part1 = get_checksum(compact_disk(disk))
print ('part1:',part1)

def test_unpack_disk_two():
    assert unpack_disk_two(["12345"]) == {
        "file0": {"block": 0, "size": 1, "id": 0},
        "free101": {"block": 1, "size": 2},
        "file2": {"block": 3, "size": 3, "id": 1},
        "free103": {"block": 6, "size": 4},
        "file4": {"block": 10, "size": 5, "id": 2},
    }
    assert unpack_disk_two(read_file_lines("day9-test.txt")) == {
        "file0": {"block": 0, "size": 2, "id": 0},
        "free101": {"block": 2, "size": 3},
        "file2": {"block": 5, "size": 3, "id": 1},
        "free103": {"block": 8, "size": 3},
        "file4": {"block": 11, "size": 1, "id": 2},
        "free105": {"block": 12, "size": 3},
        "file6": {"block": 15, "size": 3, "id": 3},
        "free107": {"block": 18, "size": 1},
        "file8": {"block": 19, "size": 2, "id": 4},
        "free109": {"block": 21, "size": 1},
        "file10": {"block": 22, "size": 4, "id": 5},
        "free111": {"block": 26, "size": 1},
        "file12": {"block": 27, "size": 4, "id": 6},
        "free113": {"block": 31, "size": 1},
        "file14": {"block": 32, "size": 3, "id": 7},
        "free115": {"block": 35, "size": 1},
        "file16": {"block": 36, "size": 4, "id": 8},
        "file18": {"block": 40, "size": 2, "id": 9},
    }


def unpack_disk_two(data):
    disk = {}
    blockindex = 0
    for index,char in enumerate(data[0]):
        for i in range(int(char)):
            if index % 2 == 0:
                disk['file'+str(index)] = {'block': blockindex, 'size': int(char), 'id': index // 2}
            else:
                disk['free'+str(100 + index )] = {'block': blockindex, 'size': int(char)} 
        blockindex += int(char)
    return disk

def test_compact_disk_two():
    testdisk = unpack_disk_two(read_file_lines("day9-test.txt"))
    #assert compact_disk_two(testdisk) == {}
    
def compact_disk_two(disk):
    sorted_files = (
        key
        for key in sorted(
            (key for key in disk if key.startswith("file")),
            key=lambda x: (-disk[x]["id"], -disk[x]["block"]),
        )
    )
    for highfile in sorted_files:
        lowfree = next(
            (
                key
                for key in disk
                if key.startswith("free")
                and disk[key]["size"] >= disk[highfile]["size"]
                and disk[key]["block"] < disk[highfile]["block"]
            ),
            None,
        )
        if lowfree != None:
            oldblock = disk[highfile]['block']
            newblock = disk[lowfree]['block']
            disk[highfile]['block'] = newblock
            if disk[highfile]['size'] == disk[lowfree]['size']:
                disk[lowfree]['block'] = oldblock
            else:
                disk[lowfree]['block'] = disk[lowfree]['block'] + disk[highfile]['size']
                newsize = disk[lowfree]['size'] - disk[highfile]['size'] 
                disk[lowfree]['size'] = newsize
                max_free_key = max(
                 (key for key in disk if key.startswith('free')),
                 default=None
                )
                if max_free_key is not None:
                    max_free_num = int(max_free_key[4:])
                    new_free_key = f'free{max_free_num + 1}'
                    disk[new_free_key] = {'block': oldblock, 'size': disk[highfile]['size'] }
    return disk

def print_disk(disk):
    sorted_disk = dict(sorted(disk.items(), key=lambda x: disk[x[0]]['block']))
    for key, value in sorted_disk.items():
        size = value['size']
        if key.startswith('file'):
            id = value['id']
            print(str(id) * size, end='')
        else:
            print (str('.') * size, end='')
    print("\r")

def test_checksum_two():
    testdisk = {
        "file0": {"block": 0, "size": 2, "id": 0},
        "free1": {"block": 2, "size": 3},
        "file2": {"block": 5, "size": 3, "id": 1},
        "free3": {"block": 8, "size": 3},
        "file4": {"block": 11, "size": 1, "id": 2},
        "free5": {"block": 12, "size": 3},
        "file6": {"block": 15, "size": 3, "id": 3},
        "free7": {"block": 18, "size": 1},
        "file8": {"block": 19, "size": 2, "id": 4},
        "free9": {"block": 21, "size": 1},
        "file10": {"block": 22, "size": 4, "id": 5},
        "free11": {"block": 26, "size": 1},
        "file12": {"block": 27, "size": 4, "id": 6},
        "free13": {"block": 31, "size": 1},
        "file14": {"block": 32, "size": 3, "id": 7},
        "free15": {"block": 35, "size": 1},
        "file16": {"block": 36, "size": 4, "id": 8},
        "file18": {"block": 40, "size": 2, "id": 9},
    }
    assert checksum_two(compact_disk_two(testdisk)) == 2858
    
def checksum_two(disk):
    result = 0
    for key, value in disk.items():
        if key.startswith('file'):
            for i in range(value['block'], value['block'] + value['size']):
                result += i * value['id']
    return result

disk2 = unpack_disk_two(read_file_lines("day9-input.txt"))
part2 = checksum_two(compact_disk_two(disk2))
print('part2:',part2)