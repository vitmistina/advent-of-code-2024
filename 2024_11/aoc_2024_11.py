from typing import Dict, List, Tuple

Memo = Dict[Tuple[str, int], int]


def evaluate_num_str(num_str: str) -> List[str]:
    if num_str == "0":
        return ["1"]
    if len(num_str) % 2 == 0:
        mid = len(num_str) // 2
        return [str(int(num_str[:mid])), str(int(num_str[mid:]))]
    return [str(int(num_str) * 2024)]


def solve_recursively(data: List[str], rounds: int, memo: Memo) -> int:
    if rounds == 0:
        return len(data)
    total_result = 0
    for num_str in data:
        current = (num_str, rounds)
        if current in memo:
            total_result += memo[current]
            continue
        next_list = evaluate_num_str(num_str)
        result = sum(
            solve_recursively([next_str], rounds - 1, memo) for next_str in next_list
        )
        memo[current] = result
        total_result += result
    return total_result


def main(input_file_path: str) -> Dict[str, int]:
    with open(input_file_path) as f:
        data = f.read().strip().split()
    memo = {}
    return {
        "part_1": solve_recursively(data, 25, memo),
        "part_2": solve_recursively(data, 75, memo),
    }


if __name__ == "__main__":
    result = main("./2024_11/2024_11_input.txt")
    print(result)
