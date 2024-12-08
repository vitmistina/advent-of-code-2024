from collections import defaultdict
from enum import Enum
from typing import Dict, List, Set


class PartType(Enum):
    PART_1 = 1
    PART_2 = 2


class Coordinate:
    def __init__(self, col: int, row: int):
        self.col = col
        self.row = row

    def is_in_bounds(self, max_col: int, max_row: int) -> bool:
        return 0 <= self.col < max_col and 0 <= self.row < max_row

    def __add__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(self.col + other.col, self.row + other.row)

    def __eq__(self, other: "Coordinate") -> bool:
        return self.col == other.col and self.row == other.row

    def __hash__(self):
        return hash((self.col, self.row))

    def __repr__(self):
        return f"({self.col}, {self.row})"

    def __str__(self):
        return f"({self.col}, {self.row})"


class Vector:
    def __init__(self, col: int, row: int):
        self.col = col
        self.row = row

    @classmethod
    def from_coords(cls, start: Coordinate, end: Coordinate):
        return cls(end.col - start.col, end.row - start.row)

    def __eq__(self, other: "Vector") -> bool:
        return self.col == other.col and self.row == other.row

    def __hash__(self):
        return hash((self.col, self.row))

    def __repr__(self):
        return f"Vector({self.col}, {self.row})"

    def __str__(self):
        return f"Vector({self.col}, {self.row})"

    def __add__(self, other):
        return Vector(self.col + other.col, self.row + other.row)

    def __mul__(self, other):
        return Vector(self.col * other, self.row * other)

    def scalar_mul(self, value: int) -> "Vector":
        return Vector(self.col * value, self.row * value)

    def __sub__(self, other):
        return Vector(self.col - other.col, self.row - other.row)

    def __truediv__(self, other):
        return Vector(self.col / other, self.row / other)

    def __floordiv__(self, other):
        return Vector(self.col // other, self.row // other)


class Map:
    def __init__(self, data: List[str], part: PartType):
        self.antennas: Dict[str, List[Coordinate]] = self.load_antennas(data)
        self.antinodes: Set[Coordinate] = set()
        self.max_col = len(data[0])
        self.max_row = len(data)
        self.part = part

    def load_antennas(self, data: List[str]) -> Dict[str, List[Coordinate]]:
        antennas = defaultdict(list)
        for row, line in enumerate(data):
            for col, char in enumerate(line):
                if char != ".":
                    antennas[char].append(Coordinate(col, row))
        return antennas

    def populate_antinodes(self):
        for frequency in self.antennas.values():
            for i, coord in enumerate(frequency):
                for j, other_coord in enumerate(frequency):
                    if i != j:
                        vector = Vector.from_coords(coord, other_coord)
                        if self.part == PartType.PART_1:
                            antinodes = {
                                antinode
                                for antinode in [
                                    coord + vector.scalar_mul(2),
                                    other_coord + vector.scalar_mul(-2),
                                ]
                                if antinode.is_in_bounds(self.max_col, self.max_row)
                            }
                            self.antinodes.update(antinodes)
                        else:
                            self._populate_antinodes_in_direction(coord, vector, 1)
                            self._populate_antinodes_in_direction(
                                other_coord, vector, -1
                            )

    def _populate_antinodes_in_direction(
        self, coord: Coordinate, vector: Vector, dir: int
    ):
        mul = 1
        for iteration in range(10000):
            antinode: Coordinate = coord + vector.scalar_mul(mul * dir)
            if not antinode.is_in_bounds(self.max_col, self.max_row):
                break
            self.antinodes.add(antinode)
            mul += 1
        else:
            raise ValueError(f"Too many iterations at {coord}")

    def __repr__(self) -> str:
        output = []
        for row in range(self.max_row):
            line = []
            for col in range(self.max_col):
                coord = Coordinate(col, row)
                if coord in self.antinodes:
                    line.append("#")
                else:
                    for frequency, coords in self.antennas.items():
                        if coord in coords:
                            line.append(frequency)
                            break
                    else:
                        line.append(".")
            output.append("".join(line))
        return "\n".join(output)


def main(input_file_path: str):
    with open(input_file_path) as f:
        data = [line.strip() for line in f.readlines()]
        part_1 = Map(data, PartType.PART_1)
        part_1.populate_antinodes()
        part_2 = Map(data, PartType.PART_2)
        part_2.populate_antinodes()

        return {"part_1": len(part_1.antinodes), "part_2": len(part_2.antinodes)}


if __name__ == "__main__":
    result = main("./2024_08/2024_08_input.txt")
    print(result)
