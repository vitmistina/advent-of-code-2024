from enum import Enum
from typing import List, Optional
from collections import deque


class Operand(Enum):
    ADD = 1
    MUL = 2
    CONCAT = 3


class PartType(Enum):
    PART_1 = 1
    PART_2 = 2


class Calibrator:
    def __init__(self, part: PartType):
        self.part = part

    def roll_up_with_expressions(
        self,
        expected: int,
        nums: List[int],
        accumulator: Optional[int] = None,
        operands: Optional[List[Operand]] = None,
    ) -> Optional[List[Operand]]:
        if accumulator is None:
            accumulator = nums[0]
            nums = nums[1:]
        if operands is None:
            operands = []

        if not nums:
            return operands if accumulator == expected else None

        if accumulator > expected:
            return None

        for operand in Operand:
            provisional = self._apply_operand(accumulator, nums[0], operand)
            if provisional is not None:
                result = self.roll_up_with_expressions(
                    expected, nums[1:], provisional, operands + [operand]
                )
                if result is not None:
                    return result
        return None

    def _apply_operand(
        self, accumulator: int, num: int, operand: Operand
    ) -> Optional[int]:
        if operand == Operand.ADD:
            return accumulator + num
        elif operand == Operand.MUL:
            return accumulator * num
        elif operand == Operand.CONCAT:
            return int(f"{accumulator}{num}") if self.part == PartType.PART_2 else None
        raise ValueError(f"Invalid operand: {operand}")

    def depth_first_search(
        self, expected: int, nums: List[int]
    ) -> Optional[List[Operand]]:
        stack = [(1, nums[0], [])]
        while stack:
            idx, accumulator, operands = stack.pop()
            if idx == len(nums):
                if accumulator == expected:
                    return operands
                continue
            for operand in Operand:
                provisional = self._apply_operand(accumulator, nums[idx], operand)
                if provisional is not None and provisional <= expected:
                    stack.append((idx + 1, provisional, operands + [operand]))
        return None

    def breadth_first_search(
        self, expected: int, nums: List[int]
    ) -> Optional[List[Operand]]:
        queue = deque([(1, nums[0], [])])
        while queue:
            idx, accumulator, operands = queue.popleft()
            if idx == len(nums):
                if accumulator == expected:
                    return operands
                continue
            for operand in Operand:
                provisional = self._apply_operand(accumulator, nums[idx], operand)
                if provisional is not None and provisional <= expected:
                    queue.append((idx + 1, provisional, operands + [operand]))
        return None


def main(input_file_path: str):
    with open(input_file_path) as f:
        data = [line.strip().split(":") for line in f.readlines()]
        lines = [(int(line[0]), list(map(int, line[1].split()))) for line in data]

    pt_1_calibrator = Calibrator(PartType.PART_1)
    part_1_results = [
        (pt_1_calibrator.roll_up_with_expressions(expected, nums), expected, nums)
        for expected, nums in lines
    ]
    part_1_sum = sum(
        expected for operator, expected, nums in part_1_results if operator is not None
    )

    pt_2_calibrator = Calibrator(PartType.PART_2)
    part_2_results = [
        (pt_2_calibrator.roll_up_with_expressions(expected, nums), expected, nums)
        for operator, expected, nums in part_1_results
        if operator is None
    ]
    part_2_sum = part_1_sum + sum(
        expected for operator, expected, nums in part_2_results if operator is not None
    )

    return {"part_1": part_1_sum, "part_2": part_2_sum}


if __name__ == "__main__":
    result = main("./2024_07/2024_07_input.txt")
    print(result)
