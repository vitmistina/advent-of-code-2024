from enum import Enum
from typing import List


DIR_DELTAS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class PartType(Enum):
    PART_1 = 1
    PART_2 = 2


class Coord:
    def __init__(self, col, row, z):
        self.col = col
        self.row = row
        self.z = z

    def __repr__(self):
        return f"({self.col}, {self.row}, {self.z})"

    def is_inclined_from(self, other: "Coord"):
        return self.z == other.z + 1


class Map:
    def __init__(self, data: List[str]):
        self.map = []
        for row, line in enumerate(data):
            self.map.append([None] * len(line))
            for col, char in enumerate(line):
                if char.isdigit():
                    self.map[row][col] = Coord(col, row, int(char))

    def find_paths_to_nines(self, history: List[Coord]):
        current = history[-1]
        if current.z == 9:
            return [history]
        paths = []
        for delta in DIR_DELTAS:
            new_col = current.col + delta[0]
            new_row = current.row + delta[1]
            if (
                new_col < 0
                or new_col >= len(self.map[0])
                or new_row < 0
                or new_row >= len(self.map)
            ):
                continue
            new_coord: Coord = self.map[new_row][new_col]
            if new_coord is None or new_coord in history:
                continue
            if new_coord.is_inclined_from(current):
                paths.extend(self.find_paths_to_nines(history + [new_coord]))
        return paths


def main(input_file_path: str):
    with open(input_file_path) as f:
        data = [line.strip() for line in f.readlines()]
        map = Map(data)

        part_1 = 0
        part_2 = 0
        for row in map.map:
            for cell in row:
                if cell.z == 0:
                    paths = map.find_paths_to_nines([cell])
                    part_1 += len(set([path[-1] for path in paths]))
                    part_2 += len(paths)

        return {"part_1": part_1, "part_2": part_2}


if __name__ == "__main__":
    result = main("./2024_10/2024_10_input.txt")
    print(result)
