import re
from typing import Dict, List, Tuple


class Robot:
    # sample input: p=0,4 v=3,-3
    def __init__(self, input_str: str):
        self.position: Tuple[int, int] = self._parse_position(input_str)
        self.velocity: Tuple[int, int] = self._parse_velocity(input_str)

    def __repr__(self):
        return f"(p={self.position}, v={self.velocity})"

    @staticmethod
    def _parse_position(input_str: str) -> Tuple[int, int]:
        position_regex = r"p=(-?\d+),(-?\d+)"
        return tuple(map(int, re.search(position_regex, input_str).groups()))

    @staticmethod
    def _parse_velocity(input_str: str) -> Tuple[int, int]:
        velocity_regex = r"v=(-?\d+),(-?\d+)"
        return tuple(map(int, re.search(velocity_regex, input_str).groups()))

    def move_with_wrapping(self, time: int, bounds: Tuple[int, int]) -> Tuple[int, int]:
        x, y = self.position
        vx, vy = self.velocity
        return (x + vx * time) % bounds[0], (y + vy * time) % bounds[1]


def count_robots_in_quadrants(
    robots: List[Robot], width: int, height: int
) -> Dict[str, int]:
    quadrants = {"TopRight": 0, "TopLeft": 0, "BottomLeft": 0, "BottomRight": 0}
    for robot in robots:
        x, y = robot.move_with_wrapping(100, (width, height))
        if x == width // 2 or y == height // 2:
            continue
        if x < width / 2 and y < height / 2:
            quadrants["TopLeft"] += 1
        elif x < width / 2 and y > height / 2:
            quadrants["BottomLeft"] += 1
        elif x > width / 2 and y < height / 2:
            quadrants["TopRight"] += 1
        elif x > width / 2 and y > height / 2:
            quadrants["BottomRight"] += 1
    return quadrants


def print_on_grid(robots: List[Robot], width: int, height: int) -> None:
    pos_count = {}
    for robot in robots:
        x, y = robot.move_with_wrapping(100, (width, height))
        pos_count[(x, y)] = pos_count.get((x, y), 0) + 1
    for y in range(height):
        for x in range(width):
            print(pos_count.get((x, y), "."), end="")
        print()


def main(input_file_path: str, width: int, height: int) -> Dict[str, int]:
    with open(input_file_path) as f:
        data = [Robot(line.strip()) for line in f.readlines()]
        print_on_grid(data, width, height)
        quadrants = count_robots_in_quadrants(data, width, height)
        print(quadrants)
        # product (multiplied) of all values in quadrants
        product = 1
        for value in quadrants.values():
            product *= value

        return {"part_1": product, "part_2": None}


if __name__ == "__main__":
    result = main("./2024_14/2024_14_input.txt", 101, 103)
    print(result)
