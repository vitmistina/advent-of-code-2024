from enum import Enum
from typing import List, Set, Tuple


class Sides(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


class PartType(Enum):
    PART_1 = 1
    PART_2 = 2


DIRECTIONS = [
    (Sides.BOTTOM, 0, 1),
    (Sides.RIGHT, 1, 0),
    (Sides.TOP, 0, -1),
    (Sides.LEFT, -1, 0),
]

SeenSet = Set[Tuple[int, int]]
WallPiece = Set[Tuple[Sides, int, int]]


def is_out_of_bounds(col: int, row: int, width: int, height: int) -> bool:
    return col < 0 or row < 0 or col >= width or row >= height


def process_area(
    map: List[List[str]], initial: Tuple[int, int], seen: SeenSet, part_type: PartType
) -> int:
    width, height = len(map[0]), len(map)
    col, row = initial
    char = map[row][col]
    stack = [initial]
    seen.add((col, row))
    area = 0
    walls_pieces: WallPiece = set()

    while stack:
        col, row = stack.pop()
        area += 1
        for side, dx, dy in DIRECTIONS:
            new_col, new_row = col + dx, row + dy
            if (
                is_out_of_bounds(new_col, new_row, width, height)
                or map[new_row][new_col] != char
            ):
                walls_pieces.add((side, col, row))
            elif (new_col, new_row) not in seen:
                stack.append((new_col, new_row))
                seen.add((new_col, new_row))

    if part_type == PartType.PART_1:
        return area * len(walls_pieces)
    else:
        return area * len(merge_wall_pieces(walls_pieces))


def merge_wall_pieces(wall_pieces: List[WallPiece]) -> List[List[WallPiece]]:
    walls: List[List[WallPiece]] = []
    while wall_pieces:
        side, col, row = wall_pieces.pop()
        stack = [(side, col, row)]
        wall = set()
        while stack:
            side, col, row = stack.pop()
            wall.add((side, col, row))
            for _, dx, dy in DIRECTIONS:
                new_col, new_row = col + dx, row + dy
                if (side, new_col, new_row) in wall_pieces:
                    stack.append((side, new_col, new_row))
                    wall_pieces.remove((side, new_col, new_row))
        walls.append(list(wall))
    return walls


def main(input_file_path: str):
    with open(input_file_path) as f:
        map = [list(line.strip()) for line in f.readlines()]

        seen: SeenSet = set()
        part_1 = sum(
            process_area(map, (col, row), seen, PartType.PART_1)
            for row in range(len(map))
            for col in range(len(map[0]))
            if (col, row) not in seen
        )

        seen.clear()
        part_2 = sum(
            process_area(map, (col, row), seen, PartType.PART_2)
            for row in range(len(map))
            for col in range(len(map[0]))
            if (col, row) not in seen
        )

        return {"part_1": part_1, "part_2": part_2}


if __name__ == "__main__":
    result = main("./2024_12/2024_12_input.txt")
    print(result)
