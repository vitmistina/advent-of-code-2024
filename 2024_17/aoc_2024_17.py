from typing import List, Tuple


class Machine:
    def __init__(self, input_str):
        registries, instructions = input_str.split("\n\n")
        self.a, self.b, self.c = [
            int(line.strip().split()[2]) for line in registries.split("\n")
        ]
        self.instructions: List[int] = list(
            map(int, instructions.split()[1].split(","))
        )
        self.inst_pointer = 0

    def process_from_start_with_a(self, a: int) -> str:
        self.a = a
        self.inst_pointer = 0
        return self.process_instructions()

    def process_instructions(self) -> str:
        output: List[int] = []
        while self.inst_pointer < len(self.instructions):
            current_opcode = self.instructions[self.inst_pointer]
            operand = self.instructions[self.inst_pointer + 1]
            # switch from 0 to 7 for current_opcode
            match current_opcode:
                case 0:
                    self._adv(operand)
                case 1:
                    self._bxl(operand)
                case 2:
                    self._bst(operand)
                case 3:
                    self._jnz(operand)
                case 4:
                    self._bxc(operand)
                case 5:
                    output.append(self._out(operand))
                case 6:
                    self._bdv(operand)
                case 7:
                    self._cdv(operand)
            self.inst_pointer += 2
        return ",".join(map(str, output))

    def _combo_operand(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case 7:
                raise ValueError("Invalid operand")

    def _adv(self, operand: int):
        self.a //= 2 ** self._combo_operand(operand)

    def _bxl(self, operand: int):
        self.b ^= operand

    def _bst(self, operand: int):
        self.b = self._combo_operand(operand) % 8

    def _jnz(self, operand: int):
        if self.a != 0:
            self.inst_pointer = operand - 2

    def _bxc(self, _: int):
        self.b ^= self.c

    def _out(self, operand: int) -> int:
        return self._combo_operand(operand) % 8

    def _bdv(self, operand: int):
        self.b = self.a // (2 ** self._combo_operand(operand))

    def _cdv(self, operand: int):
        self.c = self.a // (2 ** self._combo_operand(operand))


def convert_to_octal(num: int) -> str:
    return oct(num)[2:]


def convert_to_decimal(octal: str) -> int:
    return int(octal, 8)


def main(input_file_path: str, has_part_2=False):
    with open(input_file_path) as f:
        input_str = f.read()
        m = Machine(input_str)
        part_1 = m.process_instructions()

        part_2 = None
        # m = Machine(input_str)
        # instr = ",".join(map(str, m.instructions))
        # instr_rev_num = int(instr[::-1].replace(",", ""))
        # iterations = 0

        # m.a = 281474976710656 + 15375
        # m.inst_pointer = 0
        # new_instructions = m.process_instructions()
        # new_instr_rev_num = int(new_instructions[::-1].replace(",", ""))
        if has_part_2:
            m = Machine(input_str)
            # candidates are octal strings with 16 digits, in the tuple they have the current reached point
            # working back from the end of the instructions
            instr_len = len(m.instructions)
            candidates: List[Tuple[str, int, int]] = [("0" * instr_len, 0, 0)]
            while candidates:
                octal, integer, reached = candidates.pop()
                if reached == instr_len:
                    part_2 = integer
                    break
                for j in list(reversed(range(0, 8))):
                    new_octal = octal[:reached] + str(j) + octal[reached + 1 :]
                    prelim_res = m.process_from_start_with_a(
                        convert_to_decimal(new_octal)
                    ).split(",")

                    if len(prelim_res) > -reached + 1 and prelim_res[
                        -(reached + 1)
                    ] == str(m.instructions[-(reached + 1)]):
                        candidates.append(
                            (new_octal, convert_to_decimal(new_octal), reached + 1)
                        )

        return {"part_1": part_1, "part_2": part_2}


if __name__ == "__main__":
    result = main("./2024_17/2024_17_input.txt", has_part_2=True)
    print(result)
