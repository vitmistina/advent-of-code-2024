from dataclasses import dataclass, field
from enum import Enum
from queue import PriorityQueue
from typing import Dict, List, Set, Tuple

Coord = Tuple[int, int]
Direction = Tuple[int, int]
VisitedKey = Tuple[Coord, Direction]
QueueItem = Tuple[List[Coord], List[Direction], int]


class PartType(Enum):
    PART_1 = 1
    PART_2 = 2


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: QueueItem = field(compare=False)


DIRECTIONS: List[Direction] = [(0, -1), (1, 0), (0, 1), (-1, 0)]


class Map:
    def __init__(self, data: List[List[str]], part: PartType):
        self.map = data
        self.start = (1, len(data) - 2)
        self.end = (len(data[0]) - 2, 1)
        self.part = part

    def a_star(self) -> int:
        minimums: Dict[VisitedKey, Tuple[int, Set[Coord], int]] = {}
        queue: PriorityQueue[QueueItem] = PriorityQueue()
        queue.put(PrioritizedItem(0, ([self.start], [(1, 0)], 0)))

        ends: Dict[Direction, int] = {}
        if self.map[self.end[1]][self.end[0] - 1] != "#":
            ends[(1, 0)] = None
        if self.map[self.end[1] + 1][self.end[0]] != "#":
            ends[(0, -1)] = None
        while queue.qsize() > 0:
            prioritized_item: PrioritizedItem = queue.get()
            history, directions, distance = prioritized_item.item
            current_pos = history[-1]
            current_dir = directions[-1]
            candidates = [
                ((current_pos[0] + d[0], current_pos[1] + d[1]), d) for d in DIRECTIONS
            ]
            end_is_near = None
            for candidate, new_dir in candidates:
                x, y = candidate
                if self.map[y][x] == "#":
                    continue
                prev_min, prev_min_history, ways_to_get_there = minimums.get(
                    (candidate, new_dir), (float("inf"), set(), 0)
                )
                rotation_cost = 0 if current_dir == new_dir else 1000
                new_distance = distance + 1 + rotation_cost
                if end_is_near and new_distance != end_is_near:
                    continue
                new_history = list(history) + [candidate]

                if new_distance < prev_min or (
                    self.part == PartType.PART_2
                    and new_distance == prev_min
                    and set(new_history) - prev_min_history != set()
                ):
                    minimums[(candidate, new_dir)] = (
                        new_distance,
                        set(new_history) | prev_min_history,
                        ways_to_get_there + 1,
                    )
                    new_directions = list(directions) + [new_dir]
                    if candidate == self.end:
                        ends[new_dir] = new_distance
                        if all(ends.values()):
                            if self.part == PartType.PART_1:
                                return min(ends.values())
                            else:
                                end_is_near = new_distance
                    else:
                        heuristic = abs(candidate[0] - self.end[0]) + abs(
                            candidate[1] - self.end[1]
                        )
                        queue.put(
                            PrioritizedItem(
                                new_distance + heuristic,
                                (new_history, new_directions, new_distance),
                            )
                        )
        if self.part == PartType.PART_2:
            optimal_path_distance = min(ends.values())
            for direction, distance in ends.items():
                if distance == optimal_path_distance:
                    return len(minimums[(self.end, direction)][1])
        raise ValueError("No path found")

    def print_with_history(self, history: List[Coord]):
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if (x, y) in history:
                    print("X", end="")
                else:
                    print(cell, end="")
            print()
        print()


def main(input_file_path: str):
    with open(input_file_path) as f:
        data = [list(line.strip()) for line in f.readlines()]
        map = Map(data, PartType.PART_1)
        part_1 = map.a_star()
        map = Map(data, PartType.PART_2)
        part_2 = map.a_star()
        return {"part_1": part_1, "part_2": part_2}


if __name__ == "__main__":
    result = main("./2024_16/2024_16_input.txt")
    print(result)
