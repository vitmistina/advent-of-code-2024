from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple

INSTRUCTION_CONVERSION = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}


class Robot:
    def __init__(self, pos: Tuple[int, int], instructions: str):
        self.pos = pos
        self.instructions = instructions
        self.instruction_pointer = 0

    def __repr__(self):
        return f"Robot(at {self.pos}, instr={self.instructions}, intr_pt={self.instruction_pointer})"

    def move(self, map: List[List[str]]):
        x, y = self.pos
        dx, dy = INSTRUCTION_CONVERSION[self.instructions[self.instruction_pointer]]
        new_x, new_y = x + dx, y + dy
        if map[new_y][new_x] == ".":
            self.pos = (new_x, new_y)
        elif map[new_y][new_x] == "O":
            self._move_box(map, new_x, new_y, dx, dy)
        elif map[new_y][new_x] in ["[", "]"]:
            self._move_wider_box(map, new_x, new_y, dx, dy)
        self.instruction_pointer += 1

    def _move_box(self, map: List[List[str]], new_x: int, new_y: int, dx: int, dy: int):
        empty = find_in_direction(map, (new_x, new_y), (dx, dy))
        if empty:
            map[new_y][new_x] = "."
            map[empty[1]][empty[0]] = "O"
            self.pos = (new_x, new_y)

    def _move_wider_box(
        self, map: List[List[str]], new_x: int, new_y: int, dx: int, dy: int
    ):
        if dy == 0:
            self._move_horizontal_box(map, new_x, new_y, dx)
        else:
            self._move_vertical_box(map, new_x, new_y, dx, dy)

    def _move_horizontal_box(
        self, map: List[List[str]], new_x: int, new_y: int, dx: int
    ):
        empty = find_in_direction(map, (new_x, new_y), (dx, 0))
        if empty:
            x_dist = empty[0] - new_x
            if x_dist > 0:
                map[new_y] = (
                    map[new_y][:new_x]
                    + ["."]
                    + map[new_y][new_x : new_x + x_dist]
                    + map[new_y][new_x + x_dist + 1 :]
                )
            else:
                map[new_y] = (
                    map[new_y][: new_x + x_dist]
                    + map[new_y][new_x + x_dist + 1 : new_x + 1]
                    + ["."]
                    + map[new_y][new_x + 1 :]
                )
            self.pos = (new_x, new_y)
            if not check_integrity(map):
                raise ValueError("Box not moved correctly")

    def _move_vertical_box(
        self, map: List[List[str]], new_x: int, new_y: int, dx: int, dy: int
    ):
        is_cone_empty = find_unblocked_cone(
            map, (new_x, new_y), (dx, dy), map[new_y][new_x]
        )
        if is_cone_empty:
            y_to_x = sort_cone_to_list_of_y(is_cone_empty)
            current = max(y_to_x.keys()) if dy > 0 else min(y_to_x.keys())
            while current in y_to_x:
                for x in y_to_x[current]:
                    map[current + dy][x] = map[current][x]
                    map[current][x] = "."
                current -= dy
            self.pos = (new_x, new_y)
            if map[new_y][new_x] in ["[", "]"]:
                raise ValueError("Box not moved correctly")
            if not check_integrity(map):
                raise ValueError("Box not moved correctly")

    def execute_instructions(self, map: List[List[str]]):
        while self.instruction_pointer < len(self.instructions):
            self.move(map)


def check_integrity(map: List[List[str]]) -> bool:
    for row in map:
        row_str = "".join(row)
        if "[[" in row_str or "]]" in row_str:
            return False
    return True


def sort_cone_to_list_of_y(cone: Set[Tuple[int, int]]) -> Dict[int, List[int]]:
    y_to_x = defaultdict(list)
    for x, y in cone:
        y_to_x[y].append(x)
    return y_to_x


def find_unblocked_cone(
    map: List[List[str]],
    pos: Tuple[int, int],
    direction: Tuple[int, int],
    box_part: str,
) -> Optional[Set[Tuple[int, int]]]:
    assert box_part in ["[", "]"]
    dx, dy = direction
    cone: Set[Tuple[int, int]] = {pos}
    if box_part == "[":
        cone.add((pos[0] + 1, pos[1]))
    else:
        cone.add((pos[0] - 1, pos[1]))

    for x, y in list(cone):
        if map[y + dy][x + dx] == "#":
            return None
        elif map[y + dy][x + dx] in ["[", "]"]:
            next_cone = find_unblocked_cone(
                map, (x + dx, y + dy), direction, map[y + dy][x + dx]
            )
            if next_cone:
                cone.update(next_cone)
            else:
                return None
    return cone


def find_in_direction(
    map: List[List[str]], pos: Tuple[int, int], direction: Tuple[int, int]
) -> Optional[Tuple[int, int]]:
    x, y = pos
    dx, dy = direction
    while map[y][x] != "#":
        x, y = x + dx, y + dy
        if map[y][x] == ".":
            return (x, y)
    return None


def score_map(map: List[List[str]]) -> int:
    return sum(
        r_idx * 100 + c_idx
        for r_idx, row in enumerate(map)
        for c_idx, cell in enumerate(row)
        if cell == "O"
    )


def score_box_map(map: List[List[str]]) -> int:
    return sum(
        r_idx * 100 + c_idx
        for r_idx, row in enumerate(map)
        for c_idx, cell in enumerate(row)
        if cell == "["
    )


def main(input_file_path: str) -> Dict[str, int]:
    with open(input_file_path) as f:
        input_string = f.read()
        part_1 = execute_part_1(input_string)

        part_2 = execute_part_2(input_string)

        return {"part_1": score_map(part_1), "part_2": score_box_map(part_2)}


def execute_part_2(input_string):
    map, instructions = [part.strip() for part in input_string.split("\n\n")]
    map = [list(row.strip()) for row in map.split("\n")]
    instructions = instructions.replace("\n", "")

    robot = None
    extended_map = []
    for y, row in enumerate(map):
        extended_row = []
        for x, cell in enumerate(row):
            if cell == "#":
                extended_row.extend("##")
            elif cell == ".":
                extended_row.extend("..")
            elif cell == "O":
                extended_row.extend("[]")
            elif cell == "@":
                robot = Robot((x * 2, y), instructions)
                extended_row.extend("..")
        extended_map.append(extended_row)

    if robot:
        robot.execute_instructions(extended_map)
    return extended_map


def execute_part_1(input_string: str) -> List[List[str]]:
    map, instructions = [part.strip() for part in input_string.split("\n\n")]
    map = [list(row.strip()) for row in map.split("\n")]
    instructions = instructions.replace("\n", "")

    robot = None
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == "@":
                robot = Robot((x, y), instructions)
                map[y][x] = "."

    if robot:
        robot.execute_instructions(map)
    return map


if __name__ == "__main__":
    result = main("./2024_15/2024_15_input.txt")
    print(result)
