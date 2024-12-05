from enum import Enum
from typing import List, Dict, Tuple

class PartType(Enum):
    PART_1 = 1
    PART_2 = 2

class Printer:
    def __init__(self, input_file_path: str):
        self.rules, self.updates = self.load_data(input_file_path)
    

    def load_data(self, input_file_path: str) -> Tuple[Dict[int,List[int]], List[List[int]]]:
        with open(input_file_path) as f:
            parts = f.read().strip().split("\n\n")
            rules = {}
            for rule in parts[0].split("\n"):
                rule = rule.split("|")
                current_rule = rules.get(int(rule[0]), [])
                current_rule.append(int(rule[1].strip()))
                rules[int(rule[0])] = current_rule
            
            updates = []
            for update in parts[1].split("\n"):
                updates.append(list(map(int, update.split(","))))
            
            return rules, updates
        
    def process_updates(self, part: PartType) -> int:
        if part == None:
            return 0
        middle_values = []
        for update in self.updates:
            evaluated_value = self.evaluate_update(update, PartType.PART_1)
            if part == PartType.PART_1:
                middle_values.append(evaluated_value)
            elif part == PartType.PART_2 and evaluated_value == 0:
                middle_values.append(self.evaluate_update(update, part))
        return sum(middle_values)

    def evaluate_update(self, update, part: PartType) -> int:
        for i, page_number in enumerate(update):
            for next_idx, next_page in enumerate(update[i+1:]):
                next_page_rules = self.rules.get(next_page, [])
                next_page_actual_index = next_idx + i + 1
                if page_number in next_page_rules and part == PartType.PART_1:
                    return 0
                elif page_number in next_page_rules and part == PartType.PART_2:
                    swapped_positions = update[:i] + [next_page] + [page_number] + update[i+1:next_page_actual_index] + update[next_page_actual_index+1:]
                    assert(len(swapped_positions) == len(update))
                    return self.evaluate_update(swapped_positions, part)
        else:
            return update[len(update) // 2]
                        

def main(input_file_path: str):
    printer = Printer(input_file_path)
    return {"part_1": printer.process_updates(PartType.PART_1), "part_2": printer.process_updates(PartType.PART_2)}

if __name__ == "__main__":
    result = main('./2024_05/2024_05_input.txt')
    print(result)