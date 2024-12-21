from collections import deque
from typing import Dict, List, Tuple
from collections import defaultdict


Coord = Tuple[int, int]
DistMap = Dict[Coord, int]
FromTo = Tuple[Coord, Coord]

DIRECTIONS: List[Coord] = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class Map:
    def __init__(self, data: List[List[str]]):
        self.map: List[List[str]] = data
        self.start, self.end = self._find_start_and_end()
        self.dist_from_start: DistMap = self._floodfill_from(self.start)
        self.dist_from_end: DistMap = self._floodfill_from(self.end)
        self.shortest_path_len = self.dist_from_start[self.end]

    def _find_start_and_end(self) -> Tuple[Coord, Coord]:
        for row_idx, row in enumerate(self.map):
            for col_idx, cell in enumerate(row):
                if cell == "S":
                    start = (row_idx, col_idx)
                elif cell == "E":
                    end = (row_idx, col_idx)
        return start, end

    def _floodfill_from(self, start: Coord) -> DistMap:
        dq = deque([start])
        dist_map = {start: 0}
        while dq:
            x, y = dq.popleft()
            for dx, dy in DIRECTIONS:
                new_x, new_y = x + dx, y + dy
                if (
                    0 <= new_x < len(self.map)
                    and 0 <= new_y < len(self.map[0])
                    and (new_x, new_y) not in dist_map
                    and self.map[new_x][new_y] != "#"
                ):
                    dist_map[(new_x, new_y)] = dist_map[(x, y)] + 1
                    dq.append((new_x, new_y))
        return dist_map

    def find_shortcuts_over_threshold(self, threshhold: int) -> Dict[int, List[FromTo]]:
        shortcuts = defaultdict(list)
        for shortcut_from, start_distance in self.dist_from_start.items():
            if start_distance > self.shortest_path_len:
                continue
            for direction in DIRECTIONS:
                shortcut_end = (
                    shortcut_from[0] + direction[0] * 2,
                    shortcut_from[1] + direction[1] * 2,
                )
                end_distance = self.dist_from_end.get(shortcut_end, float("inf"))
                time_saved = self.shortest_path_len - (
                    start_distance + end_distance + 2
                )
                if time_saved >= threshhold:
                    shortcuts[time_saved].append((shortcut_from, shortcut_end))

        return shortcuts


def main(input_file_path: str, threshhold: int) -> dict[str, int]:
    with open(input_file_path) as f:
        data = [list(line.strip()) for line in f.readlines()]
        map = Map(data)
        shortcuts = map.find_shortcuts_over_threshold(threshhold)
        for time_saved, locs in shortcuts.items():
            print(f"locations: {len(locs)}, Time saved: {time_saved}")
        return {
            "part_1": sum([len(locs) for locs in shortcuts.values()]),
            "part_2": None,
        }


if __name__ == "__main__":
    # 404 too low for part 1 (it was supposed to be sum, not len :-)
    result = main("./2024_20/2024_20_input.txt", 100)
    print(result)
