from enum import Enum
import re
from typing import Dict, Tuple, List


class PartType(Enum):
    PART_1 = 1
    PART_2 = 2


BUTTON_COSTS = {
    "A": 3,
    "B": 1,
}


class ClawMachine:
    def __init__(self, machine_str: str):
        self.buttons = self._parse_buttons(machine_str)
        self.prize = self._parse_prize(machine_str)

    @staticmethod
    def _parse_buttons(machine_str: str) -> Dict[str, Tuple[int, int]]:
        button_regex = r"Button ([A-Z]): X\+(\d+), Y\+(\d+)"
        return {
            button_name: (int(x), int(y))
            for button_name, x, y in re.findall(button_regex, machine_str)
        }

    @staticmethod
    def _parse_prize(machine_str: str) -> Tuple[int, int]:
        prize_regex = r"Prize: X=(\d+), Y=(\d+)"
        return tuple(map(int, re.search(prize_regex, machine_str).groups()))

    def __repr__(self):
        return f"ClawMachine(buttons={self.buttons}, prize={self.prize})"

    def find_minimum_mathematically(self, part_type: PartType) -> int:
        prize_x, prize_y = self.prize
        if part_type == PartType.PART_2:
            prize_x += 10000000000000
            prize_y += 10000000000000

        ax, ay = self.buttons["A"]
        bx, by = self.buttons["B"]

        b = (prize_y * ax - prize_x * ay) / (by * ax - bx * ay)
        a = (prize_x - b * bx) / ax

        if (
            a % 1 != 0
            or b % 1 != 0
            or a < 0
            or b < 0
            or (part_type == PartType.PART_1 and (a > 100 or b > 100))
        ):
            return 0

        return int(a * BUTTON_COSTS["A"] + b * BUTTON_COSTS["B"])


def calculate_total_cost(data: List[ClawMachine], part_type: PartType) -> int:
    return


def read_input_file(input_file_path: str) -> List[ClawMachine]:
    with open(input_file_path) as f:
        return [ClawMachine(part) for part in f.read().split("\n\n")]


def main(input_file_path: str) -> Dict[str, int]:
    data = read_input_file(input_file_path)
    part_1 = sum(
        machine.find_minimum_mathematically(PartType.PART_1) for machine in data
    )
    part_2 = sum(
        machine.find_minimum_mathematically(PartType.PART_2) for machine in data
    )
    return {"part_1": part_1, "part_2": part_2}


if __name__ == "__main__":
    result = main("./2024_13/2024_13_input.txt")
    print(result)
