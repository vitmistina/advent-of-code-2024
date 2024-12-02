from typing import List, Dict

def main(input_file_path: str) -> Dict[str, int]:
    data = read_input(input_file_path)
    return {
        "part_1": count_safe_sequences(data),
        "part_2": count_safe_sequences_with_damper(data)
    }

def read_input(input_file_path: str) -> List[str]:
    with open(input_file_path) as f:
        return [line.strip() for line in f]

def count_safe_sequences(data: List[str]) -> int:
    return sum(1 for line in data if is_safe_sequence(parse_line(line)))

def count_safe_sequences_with_damper(data: List[str]) -> int:
    return sum(1 for line in data if is_safe_with_damper(parse_line(line)))

def parse_line(line: str) -> List[int]:
    return list(map(int, line.split()))

def is_safe_sequence(sequence: List[int]) -> bool:
    diffs = [y - x for x, y in zip(sequence, sequence[1:])]
    return all_same_sign(diffs) and all_in_acceptable_range(diffs)

def is_safe_with_damper(sequence: List[int]) -> bool:
    if is_safe_sequence(sequence):
        return True
    return any(is_safe_sequence(sequence[:i] + sequence[i+1:]) for i in range(len(sequence)))

def all_same_sign(diffs: List[int]) -> bool:
    return all(x > 0 for x in diffs) or all(x < 0 for x in diffs)

def all_in_acceptable_range(diffs: List[int]) -> bool:
    acceptable_range = {1, 2, 3}
    return all(abs(x) in acceptable_range for x in diffs)

if __name__ == "__main__":
    result = main('./2024_02/2024_02_input.txt')
    print(result)