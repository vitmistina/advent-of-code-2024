from typing import Deque, List, Tuple, Dict, Optional, Set
from collections import deque


class Coord:
    def __init__(self, col: int, row: int):
        self.col = col
        self.row = row

    def __repr__(self):
        return f"C({self.col}, {self.row})"

    @classmethod
    def from_tuple(cls, input: Tuple[int, int]) -> "Coord":
        return cls(input[0], input[1])


def main(
    input_file_path: str, dim: Tuple[int, int], rounds: int
) -> Dict[str, Optional[int]]:
    data = read_input(input_file_path)
    grid = get_grid_at_round(dim, rounds, data)

    part_1 = bfs_pathfind(dim, grid)

    part_2 = binary_search_for_part_2(dim, rounds, data)

    return {"part_1": part_1, "part_2": part_2}


def read_input(input_file_path: str) -> List[Coord]:
    with open(input_file_path) as f:
        return [
            Coord.from_tuple(tuple(map(int, line.strip().split(","))))
            for line in f.readlines()
        ]


def get_grid_at_round(
    dim: Tuple[int, int], rounds: int, data: List[Coord]
) -> List[List[str]]:
    grid: List[List[str]] = [
        ["." for _ in range(dim[0] + 1)] for _ in range(dim[1] + 1)
    ]
    for coord in data[:rounds]:
        grid[coord.row][coord.col] = "#"
    return grid


def bfs_pathfind(dim: Tuple[int, int], grid: List[List[str]]) -> Optional[int]:
    queue: Deque[Tuple[int, int, int]] = deque([(0, 0, 0)])  # (row, col, path_length)
    seen: Set[Tuple[int, int]] = {(0, 0)}
    while queue:
        row, col, path_length = queue.popleft()
        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_row, new_col = row + dr, col + dc
            if (
                0 <= new_row <= dim[1]
                and 0 <= new_col <= dim[0]
                and (new_row, new_col) not in seen
            ):
                seen.add((new_row, new_col))
                if new_col == dim[0] and new_row == dim[1]:
                    return path_length + 1
                if grid[new_row][new_col] != "#":
                    queue.append((new_row, new_col, path_length + 1))
    return None


def binary_search_for_part_2(
    dim: Tuple[int, int], rounds: int, data: List[Coord]
) -> Optional[str]:
    left, right = rounds, len(data)
    while left < right:
        mid = (left + right) // 2
        grid = get_grid_at_round(dim, mid, data)
        if bfs_pathfind(dim, grid) is None:
            right = mid
        else:
            if bfs_pathfind(dim, get_grid_at_round(dim, mid + 1, data)) is None:
                return f"{data[mid].col},{data[mid].row}"
            left = mid + 1
    return None


if __name__ == "__main__":
    result = main("./2024_18/2024_18_input.txt", (70, 70), 1024)
    print(result)
