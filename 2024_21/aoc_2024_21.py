from collections import defaultdict, deque
from typing import Dict, List, Tuple, Optional

Coord = Tuple[int, int]
PathDict = Dict[Tuple[str, str], List[List[str]]]

NUM_KEYPAD: List[List[Optional[str]]] = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"],
]
DIR_KEYPAD: List[List[Optional[str]]] = [[None, "^", "A"], ["<", "v", ">"]]
DIRECTIONS: List[Coord] = [(1, 0), (-1, 0), (0, -1), (0, 1)]
DIR_MAP = {(1, 0): ">", (-1, 0): "<", (0, -1): "^", (0, 1): "v"}

PART_1_LEVELS = 3
PART_2_LEVELS = 26


def find_keypad_position(keypad: List[List[Optional[str]]], key: str) -> Coord:
    for y, row in enumerate(keypad):
        for x, value in enumerate(row):
            if value == key:
                return (x, y)
    raise ValueError(f"Key {key} not found in keypad")


def find_all_paths(start: str, target: str, is_numerical: bool) -> List[List[str]]:
    keypad = NUM_KEYPAD if is_numerical else DIR_KEYPAD
    start_pos = find_keypad_position(keypad, start)
    end_pos = find_keypad_position(keypad, target)

    q = deque([(start_pos, [])])
    paths = []
    keep_going = True
    while q:
        (x, y), path = q.popleft()
        if (x, y) == end_pos:
            paths.append(path + ["A"])
            keep_going = False
            continue
        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(keypad[0]) and 0 <= new_y < len(keypad):
                new_pos = keypad[new_y][new_x]
                if keep_going and new_pos is not None:
                    q.append(((new_x, new_y), path + [DIR_MAP[(dx, dy)]]))
    return paths


def path_all_combinations(is_numerical: bool) -> PathDict:
    keypad = NUM_KEYPAD if is_numerical else DIR_KEYPAD
    # output = {}
    # for row in keypad:
    #     for start in row:
    #         if start is not None:
    #             for row2 in keypad:
    #                 for end in row2:
    #                     if end is not None:
    #                         output[(start, end)] = find_all_paths(
    #                             start, end, is_numerical
    #                         )
    # return output
    return {
        (start, end): find_all_paths(start, end, is_numerical)
        for row in keypad
        for start in row
        if start is not None
        for row2 in keypad
        for end in row2
        if end is not None
    }


NUM_PATHS = path_all_combinations(True)
PAD_PATHS = path_all_combinations(False)


def find_optimal_expansion(instruction: str, is_num: bool) -> List[str]:
    pad = NUM_PATHS if is_num else PAD_PATHS
    output = []
    for i in range(len(instruction)):
        start = "A" if i == 0 else instruction[i - 1]
        end = instruction[i]
        paths = pad[(start, end)]
        if len(paths) == 1:
            output.extend(paths[0])
        else:
            len_map = {find_path_len("".join(p), 2): p for p in paths}
            output.extend(len_map[min(len_map.keys())])
    return [instr + "A" for instr in "".join(output).split("A")[:-1]]


def find_path_len(instruction: str, levels: int) -> int:
    if levels == 0:
        return len(instruction)
    return sum(
        min(find_path_len("".join(p), levels - 1) for p in PAD_PATHS[(start, end)])
        for i, (start, end) in enumerate(zip("A" + instruction, instruction))
    )


def find_efficiently(instruction: str, levels: int) -> int:
    memo = {}
    current_map = defaultdict(int)
    numerical_level = find_optimal_expansion(instruction, True)
    for inst in numerical_level:
        current_map[inst] += 1
    for _ in range(levels - 1):
        next_map = defaultdict(int)
        for key, value in current_map.items():
            next_level = memo.get(key, find_optimal_expansion(key, False))
            memo[key] = next_level
            for inst in next_level:
                next_map[inst] += value
        current_map = next_map
    return sum(value * len(key) for key, value in current_map.items())


def calculate_complexity(data: List[List[str]], is_part_2: bool) -> List[int]:
    levels = PART_2_LEVELS if is_part_2 else PART_1_LEVELS
    return [
        int("".join(line[:-1])) * find_efficiently("".join(line), levels)
        for line in data
    ]


def main(input_file_path: str) -> Dict[str, int]:
    with open(input_file_path) as f:
        data: List[List[str]] = [list(line.strip()) for line in f.readlines()]
    part_1_complexity = calculate_complexity(data, False)
    part_2_complexity = calculate_complexity(data, True)
    return {"part_1": sum(part_1_complexity), "part_2": sum(part_2_complexity)}


if __name__ == "__main__":
    result = main("./2024_21/2024_21_input.txt")
    print(result)
