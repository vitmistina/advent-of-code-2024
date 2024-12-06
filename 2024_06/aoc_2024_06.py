from enum import Enum
from typing import List, Set, Tuple
from copy import copy, deepcopy


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


class Step:
    def __init__(self, x: int, y: int, direction: Direction):
        self.x = x
        self.y = y
        self.direction = direction

    def __repr__(self) -> str:
        return f"Step at ({self.x}, {self.y}) facing {self.direction}"

    def __eq__(self, other):
        if isinstance(other, Step):
            return (
                self.x == other.x
                and self.y == other.y
                and self.direction == other.direction
            )
        return False

    def __hash__(self):
        return hash((self.x, self.y, self.direction))


class Guard:
    def __init__(self, x: int, y: int, start_direction: Direction = Direction.UP):
        self.x = x
        self.y = y
        self.direction = start_direction

    def __repr__(self) -> str:
        return f"Guard at ({self.x}, {self.y}) facing {self.direction}"

    def move(self, new_x: int, new_y: int):
        self.x = new_x
        self.y = new_y

    def rotate(self) -> Direction:
        self.direction = DIRECTION_CHANGES[self.direction]
        return self.direction


class Map:
    def __init__(self, input_file_path: str = None):
        if input_file_path:
            self.grid, self.guard = self.load_data(input_file_path)
            self.original_guard = copy(self.guard)
            self.non_loop_steps: Set[Set[Tuple[int, int]]] = set()
        self.extra_obstacle: Tuple[int, int] = None

    def reset_guard(self):
        self.guard = copy(self.original_guard)

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

    def evaluate_guard_path(self) -> Set[Step]:
        visited_cells: Set[Step] = set(
            [Step(self.guard.x, self.guard.y, self.guard.direction)]
        )
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
                return set([(step.x, step.y) for step in visited_cells])
            elif self.grid[new_y][new_x].is_obstacle or self.extra_obstacle == (
                new_x,
                new_y,
            ):
                new_dir = self.guard.rotate()
                visited_cells.add(Step(x, y, new_dir))
            else:
                self.guard.move(new_x, new_y)
                next_step = Step(new_x, new_y, self.guard.direction)
                if next_step in visited_cells:
                    return set()
                visited_cells.add(next_step)
        print("Guard reached max steps")
        return None

    def print(self, steps: Set[Step] = None):
        coords = set([(step.x, step.y) for step in steps]) if steps else set()
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if (x, y) in coords:
                    print("X", end="")
                elif (x, y) == self.extra_obstacle:
                    print("O", end="")
                else:
                    print(cell, end="")

    def find_loops(self, steps: Set[Tuple[int, int]] = None) -> int:
        steps.remove((self.guard.x, self.guard.y))
        count = 0
        for checked, (x, y) in enumerate(steps, 1):
            self.reset_guard()
            self.extra_obstacle = (x, y)
            steps_without_loops = self.evaluate_guard_path()
            if len(steps_without_loops) == 0:
                count += 1
            if checked % 100 == 0:
                print(f"Found {count} obstacles in {checked}/{len(steps)}")
        return count


def main(input_file_path: str):
    map = Map(input_file_path)
    steps = map.evaluate_guard_path()
    part_1 = len(steps)
    # 1586 right answer
    map = Map(input_file_path)
    part_2 = map.find_loops(steps)
    return {"part_1": part_1, "part_2": part_2}


if __name__ == "__main__":
    result = main("./2024_06/2024_06_input.txt")
    print(result)
