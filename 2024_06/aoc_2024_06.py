from enum import Enum
from typing import List, Set, Tuple
from copy import deepcopy


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


DIRECTION_CHANGES = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}
DIRECTION_COORDS = {
    Direction.UP: (0, -1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
}

MAX_STEPS = 10000


class Position:
    def __init__(
        self,
        x: int,
        y: int,
        is_visited: bool = False,
        visited_directions: Set[Direction] = None,
        is_obstacle: bool = False,
    ):
        self.x = x
        self.y = y
        self.is_visited = is_visited
        self.visited_directions = (
            visited_directions if visited_directions is not None else set()
        )
        self.is_obstacle = is_obstacle

    def __repr__(self) -> str:
        if self.is_visited:
            return "X"
        elif self.is_obstacle:
            return "#"
        else:
            return "."


class Guard:
    def __init__(self, x: int, y: int, start_direction: Direction = Direction.UP):
        self.x = x
        self.y = y
        self.direction = start_direction

    def __repr__(self) -> str:
        return f"Guard at ({self.x}, {self.y}) facing {self.direction}"

    def move(self, direction: Direction, dx: int = 0, dy: int = 0):
        self.x += dx
        self.y += dy
        self.direction = direction


class Map:
    def __init__(self, input_file_path: str = None):
        if input_file_path:
            self.grid, self.guard = self.load_data(input_file_path)
            self.non_loop_steps: Set[Set[Tuple[int, int]]] = set()

    def copy_with_clear_visits(self) -> "Map":
        copy = Map().load_data_from_grid(self.grid, self.guard)
        for row in copy.grid:
            for cell in row:
                cell.is_visited = False
                cell.visited_directions = set()
        return copy

    def load_data_from_grid(self, grid: List[List[Position]], guard: Guard) -> "Map":
        self.grid = deepcopy(grid)
        self.guard = deepcopy(guard)
        return self

    def load_data(self, input_file_path: str) -> Tuple[List[List[Position]], Guard]:
        with open(input_file_path) as f:
            grid = [list(line.strip()) for line in f.readlines()]
            output: List[List[Position]] = []
            for y, row in enumerate(grid):
                output_row: List[Position] = []
                for x, cell in enumerate(row):
                    if cell == "^":
                        guard = Guard(x, y)
                        output_row.append(
                            Position(
                                x,
                                y,
                                is_visited=True,
                                visited_directions=set([Direction.UP]),
                            )
                        )
                    elif cell == "#":
                        output_row.append(Position(x, y, is_obstacle=True))
                    else:
                        output_row.append(Position(x, y))
                output.append(output_row)
            return output, guard

    def step_set_based(self) -> Set[Tuple[int, int]]:
        visited_cells: Set[Tuple[int, int]] = set()
        for _ in range(MAX_STEPS):
            x, y = self.guard.x, self.guard.y
            dx, dy = DIRECTION_COORDS[self.guard.direction]
            new_x, new_y = x + dx, y + dy
            if (
                new_x < 0
                or new_x >= len(self.grid[0])
                or new_y < 0
                or new_y >= len(self.grid)
            ):
                return visited_cells
            elif self.grid[new_y][new_x].is_obstacle:
                new_direction = DIRECTION_CHANGES[self.guard.direction]
                self.guard.move(new_direction)
            else:
                self.guard.move(self.guard.direction, dx, dy)
                visited_cells.add((new_x, new_y))
        return visited_cells

    def find_steps_without_loops(self) -> Set[Tuple[int, int]]:
        taken_steps = set()
        for _ in range(10000):
            x, y = self.guard.x, self.guard.y
            dx, dy = DIRECTION_COORDS[self.guard.direction]
            new_x, new_y = x + dx, y + dy
            if (
                new_x < 0
                or new_x >= len(self.grid[0])
                or new_y < 0
                or new_y >= len(self.grid)
            ):
                return taken_steps
            elif (
                self.grid[new_y][new_x].is_visited
                and self.guard.direction in self.grid[new_y][new_x].visited_directions
            ):
                return set()
            elif self.grid[new_y][new_x].is_obstacle:
                new_direction = DIRECTION_CHANGES[self.guard.direction]
                self.guard.move(new_direction)
                self.grid[new_y][new_x].visited_directions.add(new_direction)
            else:
                self.guard.move(self.guard.direction, dx, dy)
                self.grid[new_y][new_x].is_visited = True
                self.grid[new_y][new_x].visited_directions.add(self.guard.direction)
                taken_steps.add((new_x, new_y))
        return taken_steps

    def find_loops(self):
        copy = self.copy_with_clear_visits()
        potential_boulders = copy.step_set_based()
        potential_boulders.remove((self.guard.x, self.guard.y))
        count = 0
        for checked, (x, y) in enumerate(potential_boulders, 1):
            copy = self.copy_with_clear_visits()
            copy.grid[y][x].is_obstacle = True
            steps_without_loops = copy.find_steps_without_loops()
            if len(steps_without_loops) == 0:
                count += 1

            print(f"Found {count} obstacles in {checked}/{len(potential_boulders)}")
        return count


def main(input_file_path: str):
    map = Map(input_file_path)
    part_1 = len(map.step_set_based())
    # 1586 right answer
    map = Map(input_file_path)
    part_2 = map.find_loops()
    return {"part_1": part_1, "part_2": part_2}


if __name__ == "__main__":
    result = main("./2024_06/2024_06_input.txt")
    print(result)
