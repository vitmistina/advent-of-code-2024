from typing import List, Dict

def find_similarities(list_left: List[str], list_right: List[str], memo: Dict[str, int] = None) -> int:
    if memo is None:
        memo = {}
    products = []
    for left_value in list_left:
        if left_value in memo:
            products.append(int(left_value) * memo[left_value])
        else:
            count = list_right.count(left_value)
            memo[left_value] = count
            products.append(int(left_value) * count)
    return sum(products)

def main(input_file_path: str) -> Dict[str, int]:
    with open(input_file_path) as f:
        data = [line.strip() for line in f]

    list_left, list_right = zip(*(line.split('   ') for line in data))
    list_left, list_right = sorted(list_left), sorted(list_right)

    differences = [abs(int(left) - int(right)) for left, right in zip(list_left, list_right)]

    return {
        "part_1": sum(differences),
        "part_2": find_similarities(list_left, list_right)
    }

if __name__ == "__main__":
    result = main('./2024_01/2024_01_input.txt')
    print(result)