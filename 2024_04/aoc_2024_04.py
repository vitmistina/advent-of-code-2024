from typing import List, Dict


def extract_diagonal_slices(data: List[str]) -> List[str]:
    if not data:
        return []

    rows, cols = len(data), len(data[0])
    diagonals = []

    for d in range(rows + cols - 1):
        diagonal = [data[row][d - row] for row in range(max(0, d - cols + 1), min(rows, d + 1))]
        diagonals.append("".join(diagonal))

    return diagonals

def calculate_part_1(data: List[str]) -> int:
    target = "XMAS"
    counts = sum(line.count(target) + line[::-1].count(target) for line in data)
    columns = ["".join(col) for col in zip(*data)]
    counts += sum(col.count(target) + col[::-1].count(target) for col in columns)
    diagonals = extract_diagonal_slices(data) + extract_diagonal_slices(data[::-1])
    counts += sum(diagonal.count(target) + diagonal[::-1].count(target) for diagonal in diagonals)
    return counts


def calculate_part_2(data: List[str]) -> int:
    comparison_set = {"M", "S"}
    count = 0

    for row_idx in range(1, len(data) - 1):
        for col_idx in range(1, len(data[0]) - 1):
            if data[row_idx][col_idx] == "A":
                increasing_diagonal = {data[row_idx - 1][col_idx - 1], data[row_idx + 1][col_idx + 1]}
                decreasing_diagonal = {data[row_idx + 1][col_idx - 1], data[row_idx - 1][col_idx + 1]}
                if increasing_diagonal == comparison_set and decreasing_diagonal == comparison_set:
                    count += 1

    return count


def main(input_file_path: str) -> Dict[str, int]:
    with open(input_file_path) as f:
        data = [line.strip() for line in f.readlines()]
    return {
        "part_1": calculate_part_1(data),
        "part_2": calculate_part_2(data)
    }


if __name__ == "__main__":
    result = main('./2024_04/2024_04_input.txt')
    print(result)