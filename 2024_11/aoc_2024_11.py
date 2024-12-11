from typing import Dict, List, Tuple


def evaluate_num_str(num_str: str) -> List[str]:
    if num_str == "0":
        return ["1"]
    elif len(num_str) % 2 == 0:
        return [
            str(int(num_str[: len(num_str) // 2])),
            str(int(num_str[len(num_str) // 2 :])),
        ]

    else:
        return [str(int(num_str) * 2024)]


def solve_recursively(
    data: List[str], rounds: int, memo: Dict[Tuple[str, int], int]
) -> int:
    if rounds == 0:
        return len(data)
    total_result = 0
    for num_str in data:
        current = (num_str, rounds)
        if current in memo:
            return memo[current]
        next_list: List[str] = evaluate_num_str(num_str)
        result: int = sum(
            [solve_recursively([next_str], rounds - 1, memo) for next_str in next_list]
        )
        memo[current] = result
        total_result += result
    return total_result


def main(input_file_path: str):
    with open(input_file_path) as f:
        data = f.read().strip()
        data = [num_str for num_str in data.split(" ")]
        recursive_part_1 = solve_recursively(data, 25, {})
        # for _ in range(5):
        #     new_data = []
        #     for num_str in data:
        #         new_data.extend(evaluate_num_str(num_str))
        #     data = new_data
        # numeric_result = len(data)
        recursive_part_2 = solve_recursively(data, 75, {})
        return {
            "part_1": recursive_part_1,
            "part_2": recursive_part_2,
        }


if __name__ == "__main__":
    result = main("./2024_11/2024_11_input.txt")
    print(result)
