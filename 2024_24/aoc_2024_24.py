from collections import defaultdict, deque

from enum import Enum, auto
from typing import Dict, List, Tuple


class Operand(Enum):
    AND = auto()
    OR = auto()
    XOR = auto()


Node = Tuple[str, int]
Instruction = Tuple[
    str, Operand, str, str, bool
]  # (input_1, operand, input_2, output, is_solved)


def perform_diagnostics(
    instructions: List[Instruction], max_bit_position: int
) -> Tuple[List[str], Dict[int, List[str]]]:
    r"""Perform diagnostics on the given list of instructions trying to perform binary adding of two numbers.

    This function processes a list of instructions and returns diagnostic
    information. For each bit position the return dictionary contains a list of results.
    OK when the result was as expected and ERR when the result was not as expected.
    The ERR results are also provided in the return tuple on first position.
    Args:
        instructions (List[Instruction]): A list of instructions to be processed.
            Each instruction is a tuple containing:
            - input_1 (str): The first input node identifier.
            - operand (Operand): The operation to be performed (AND, OR, XOR).
            - input_2 (str): The second input node identifier.
            - output (str): The output node identifier.
            - is_solved (bool): A flag indicating whether the instruction is solved.
        max_bit_position (int): The maximum bit position to be considered.
    Returns:
        Tuple[List[str], Dict[int, List[str]]]: A tuple containing:
            - A list of ERR results.
            - A dictionary For each bit position the return dictionary contains a list of results. OK when the result was as expected and ERR when the result was not as expected
    """
    errors = []
    results = defaultdict(list)
    for pos in range(max_bit_position):
        scenarios = [
            ("0b00", "0b00"),
            ("0b01", "0b01"),
            ("0b00", "0b10"),
            ("0b01", "0b11"),
            ("0b10", "0b00"),
            ("0b11", "0b01"),
            ("0b10", "0b10"),
            ("0b11", "0b11"),
        ]
        # scenarios = [
        #     ("0b00", "0b10"),
        #     ("0b10", "0b00"),
        # ]

        # for x_int, y_int in scenarios:
        is_simple = False
        if is_simple:
            x_int = 1 << pos
            y_int = 0
            calculate_expected_vs_real(
                x_int, y_int, instructions, max_bit_position, errors, results, pos
            )
        else:
            if pos == 0:
                scenarios = [(int(x, 2) >> 1, int(y, 2) >> 1) for x, y in scenarios]
            else:
                scenarios = [
                    (int(x, 2) << pos - 1, int(y, 2) << pos - 1) for x, y in scenarios
                ]
            for sc in scenarios:
                x_int, y_int = sc
                calculate_expected_vs_real(
                    x_int,
                    y_int,
                    instructions,
                    max_bit_position,
                    errors,
                    results,
                    pos,
                )

    return errors, results


def calculate_expected_vs_real(
    x_int, y_int, instructions, max_bit_position, errors, results, pos
):
    x_bin = bin(x_int)[2:].zfill(max_bit_position)
    y_bin = bin(y_int)[2:].zfill(max_bit_position)
    # print(f"Performing diagnostics for x{x_bin} and y{y_bin}")
    nodes: Dict[str, int] = {}
    for idx, bit in enumerate(reversed(x_bin)):
        nodes[f"x{str(idx).zfill(2)}"] = int(bit)
    for idx, bit in enumerate(reversed(y_bin)):
        nodes[f"y{str(idx).zfill(2)}"] = int(bit)

    expected_result = x_int + y_int
    real_result = compute_node_values_hopefully_faster(nodes, list(instructions))

    if expected_result != real_result:
        errors.append(
            f"x{x_bin},\ny{y_bin} Expected: {expected_result}, Real: {real_result}\ne{bin(expected_result)[2:].zfill(max_bit_position)}\nr{bin(real_result)[2:].zfill(max_bit_position)}"
        )
        results[pos].append("ERR")
        lineage_x = find_lineage(
            f"x{str(pos).zfill(2)}", f"z{str(pos).zfill(2)}", instructions
        )
        lineage_y = find_lineage(
            f"y{str(pos).zfill(2)}", f"z{str(pos).zfill(2)}", instructions
        )
        print(f"Lineage x{str(pos).zfill(2)}: {lineage_x}")
        print(f"Lineage y{str(pos).zfill(2)}: {lineage_y}")


def find_lineage(start: str, end_id: str, instructions: List[Instruction]) -> List[str]:
    q = [(start, [start])]
    while q:
        node_id, lineage = q.pop(0)
        if node_id == end_id:
            return lineage
        for i in instructions:
            i_1, _, i_2, out, _ = i
            if i_1 == node_id or i_2 == node_id:
                q.append((out, lineage + [out]))


def swap_outputs(
    instructions: List[Instruction], swap_list: List[Tuple[str, str]]
) -> List[Instruction]:
    new_instructions = list(instructions)
    for swap in swap_list:
        out_1, out_2 = swap
        for idx, i in enumerate(instructions):
            i_1, operand, i_2, out, is_solved = i
            if out == out_1:
                new_instructions[idx] = (i_1, operand, i_2, out_2, is_solved)
            elif out == out_2:
                new_instructions[idx] = (i_1, operand, i_2, out_1, is_solved)
    return new_instructions


def compute_node_values(nodes: Dict[str, int], instructions):
    max_iterations = 1000
    while not all(i[-1] for i in instructions):
        max_iterations -= 1
        if max_iterations == 0:
            raise Exception("Max iterations reached")
        for idx, i in enumerate(instructions):
            if i[-1]:
                continue
            i_1, operand, i_2, out, is_solved = i
            if i_1 in nodes and i_2 in nodes:
                a = nodes[i_1]
                b = nodes[i_2]
                if operand == Operand.AND:
                    nodes[out] = a & b
                elif operand == Operand.OR:
                    nodes[out] = a | b
                elif operand == Operand.XOR:
                    nodes[out] = a ^ b

                instructions[idx] = (i_1, operand, i_2, out, True)

    sorted_key_values = reversed(
        sorted([(key, value) for key, value in nodes.items() if key.startswith("z")])
    )
    result = "".join(str(value) for _, value in sorted_key_values)
    return int(result, 2)


def compute_node_values_hopefully_faster(nodes: Dict[str, int], instructions):
    instructions = deque(instructions)
    while instructions:
        i = instructions.popleft()
        i_1, operand, i_2, out, is_solved = i
        if i_1 in nodes and i_2 in nodes:
            a = nodes[i_1]
            b = nodes[i_2]
            if operand == Operand.AND:
                nodes[out] = a & b
            elif operand == Operand.OR:
                nodes[out] = a | b
            elif operand == Operand.XOR:
                nodes[out] = a ^ b
        else:
            instructions.append((i_1, operand, i_2, out, False))

    sorted_key_values = reversed(
        sorted([(key, value) for key, value in nodes.items() if key.startswith("z")])
    )
    result = "".join(str(value) for _, value in sorted_key_values)
    return int(result, 2)


def main(input_file_path: str):
    with open(input_file_path) as f:
        initial, connections = [part.strip() for part in f.read().split("\n\n")]
        nodes: Dict[str, int] = {}

        max_bit_position: int = None
        for line in initial.split("\n"):
            id, value = line.split(": ")
            nodes[id] = int(value)
            max_bit_position = int(id[1:]) + 1

        instructions: List[Instruction] = [
            (
                i_1,
                Operand[op],
                i_2,
                out,
                False,
            )
            for con in connections.split("\n")
            for i_1, op, i_2, _, out in [con.split(" ")]
        ]

        swap_tuples = [("z14", "vss"), ("hjf", "kdh"), ("kpp", "z31"), ("z35", "sgj")]
        flattened_swaps = [item for sublist in swap_tuples for item in sublist]
        swapped = swap_outputs(
            instructions,
            swap_tuples,
        )

        diag = perform_diagnostics(list(swapped), max_bit_position)
        for d in diag[0]:
            print(d)
            print()

        part_1_int = compute_node_values(nodes, instructions)
        return {"part_1": part_1_int, "part_2": ",".join(sorted(flattened_swaps))}


if __name__ == "__main__":
    result = main("./2024_24/2024_24_input.txt")
    print(result)
