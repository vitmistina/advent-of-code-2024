from typing import Dict, Tuple

SequenceDict = Dict[Tuple[int, int, int, int], int]


def generate_nth_value(num: int, n: int, global_sequences: SequenceDict) -> int:
    sequences: SequenceDict = {}
    prev_price = num % 10
    diffs = []
    for _ in range(n):
        mul = num * 64
        num = (num ^ mul) % 16777216
        div = num // 32
        num = (num ^ div) % 16777216
        mul = num * 2048
        num = (num ^ mul) % 16777216
        price = num % 10
        diffs.append(price - prev_price)
        if len(diffs) >= 4 and tuple(diffs[-4:]) not in sequences:
            sequences[tuple(diffs[-4:])] = price
            aggregate_price = global_sequences.get(tuple(diffs[-4:]), 0) + price
            global_sequences[tuple(diffs[-4:])] = aggregate_price

        prev_price = price
    return num


def main(input_file_path: str):
    with open(input_file_path) as f:
        data = [int(line.strip()) for line in f.readlines()]
        global_sequences = {}
        results = [generate_nth_value(num, 2000, global_sequences) for num in data]
        return {
            "part_1": sum(results),
            "part_2": max(global_sequences.values()),
        }


if __name__ == "__main__":
    result = main("./2024_22/2024_22_input.txt")
    print(result)
