from typing import Dict, List, Tuple


def parse_input(input_file_path: str) -> Tuple[List[List[int]], List[List[int]]]:
    with open(input_file_path) as f:
        data = [part.strip().splitlines() for part in f.read().split("\n\n")]

    locks, keys = [], []
    for part in data:
        column_count_of_hash = [col.count("#") - 1 for col in zip(*part)]
        if part[0] == "#####":
            locks.append(column_count_of_hash)
        elif part[0] == ".....":
            keys.append(column_count_of_hash)
        else:
            raise ValueError("Invalid input")

    return locks, keys


def build_lock_dict(locks: List[List[int]]) -> Dict[int, Dict]:
    lock_dict = {}
    for lock in locks:
        current_level = lock_dict
        for idx, col in enumerate(lock):
            if idx == len(lock) - 1:
                current_level[col] = current_level.get(col, 0) + 1
            else:
                current_level = current_level.setdefault(col, {})
    return lock_dict


def find_non_overlapping_keys(
    keys: List[List[int]], lock_dict: Dict[int, Dict]
) -> List[int]:
    non_overlapping_keys = []
    for key in keys:
        relevant_dicts = [lock_dict]
        for idx, col in enumerate(key):
            if idx == len(key) - 1:
                for rel_dict in relevant_dicts:
                    for k in rel_dict.keys():
                        if col + k < 6:
                            non_overlapping_keys.append(rel_dict[k])
            else:
                new_relevant_dicts = []
                for rel_dict in relevant_dicts:
                    for k in rel_dict.keys():
                        if col + k < 6:
                            new_relevant_dicts.append(rel_dict[k])
                relevant_dicts = new_relevant_dicts
    return non_overlapping_keys


def main(input_file_path: str) -> Dict[str, int]:
    locks, keys = parse_input(input_file_path)
    lock_dict = build_lock_dict(locks)
    non_overlapping_keys = find_non_overlapping_keys(keys, lock_dict)

    return {"part_1": sum(non_overlapping_keys), "part_2": None}


if __name__ == "__main__":
    result = main("./2024_25/2024_25_input.txt")
    print(result)
