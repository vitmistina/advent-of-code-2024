from typing import List, Optional, Tuple
from functools import lru_cache


@lru_cache(None)
def dfs(line: str, options: Tuple[str]) -> Optional[int]:
    if not line:
        return 1
    option_count = 0
    for opt in options:
        if len(opt) > len(line):
            continue
        rest, candidate = line[: len(line) - len(opt)], line[len(line) - len(opt) :]
        if candidate != opt:
            continue
        option_count += dfs(rest, tuple(options))
    else:
        return option_count


def main(input_file_path: str):
    with open(input_file_path) as f:
        data = [line.strip() for line in f.readlines()]
        options = tuple(data[0].split(", "))
        designs = data[2:]
        results = [dfs(line, options) for line in designs]
        return {
            "part_1": sum([1 if res > 0 else 0 for res in results]),
            "part_2": sum(results),
        }


if __name__ == "__main__":
    result = main("./2024_19/2024_19_input.txt")
    print(result)
