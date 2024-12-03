import re
from typing import Dict, List

def main(input_file_path: str) -> Dict[str, int]:
    data = read_input_file(input_file_path)
    string = "".join(data)
    
    part_1_result = extract_and_multiply(string)
    part_2_string = process_string(string)
    part_2_result = extract_and_multiply(part_2_string)
    
    return {"part_1": part_1_result, "part_2": part_2_result}

def read_input_file(file_path: str) -> List[str]:
    with open(file_path) as f:
        return [line.strip() for line in f.readlines()]

def extract_and_multiply(string: str) -> int:
    regex = r"mul\((\d+),(\d+)\)"
    matches = re.findall(regex, string)
    return sum(int(x) * int(y) for x, y in matches)

def process_string(string: str) -> str:
    parts = string.split("don't()")
    processed_string = parts[0]
    for part in parts[1:]:
        processed_string += "".join(part.split("do()")[1:])
    return processed_string

if __name__ == "__main__":
    result = main('./2024_03/2024_03_input.txt')
    print(result)