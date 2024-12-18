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
        self.guard_path: List[Step] = [Step(self.x, self.y, self.direction)]

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
                return self.guard.guard_path
            elif self.grid[new_y][new_x].is_obstacle or self.extra_obstacle == (
                new_x,
                new_y,
            ):
                new_dir = self.guard.rotate()
                self.guard.guard_path.append(Step(x, y, new_dir))
            else:
                self.guard.move(new_x, new_y)
                next_step = Step(new_x, new_y, self.guard.direction)
                self.guard.guard_path.append(next_step)
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
            print()
        print()

    def find_loops_efficiently(self, steps: List[Step]) -> int:
        count = 0
        for i, step in enumerate(steps[1:], 1):
            x, y = step.x, step.y
            # Get the guard's state before reaching the blocked position
            prev_step = self.guard.guard_path[i - 1]
            # Recreate the guard's state at that moment
            guard = Guard(prev_step.x, prev_step.y, prev_step.direction)
            # Since the next cell is now blocked, the guard will rotate
            guard.rotate()

            visited_states = set()
            loop_detected = False
            for _ in range(MAX_STEPS):  # Limit the simulation steps
                state = (guard.x, guard.y, guard.direction)
                if state in visited_states:
                    loop_detected = True
                    # print(f"Loop detected at {step}")
                    break  # Loop detected
                visited_states.add(state)

                dx, dy = DIRECTION_COORDS[guard.direction]
                new_x, new_y = guard.x + dx, guard.y + dy

                # If the next position is the one we blocked, the guard rotates
                if (new_x, new_y) == (x, y):
                    guard.rotate()
                    continue
                # If the guard exits the map, simulation ends
                if (
                    new_x < 0
                    or new_x >= len(self.grid[0])
                    or new_y < 0
                    or new_y >= len(self.grid)
                ):
                    # print(f"Non-loop (exit) detected at {step}")
                    break
                # If the guard encounters an obstacle, it rotates
                if self.grid[new_y][new_x].is_obstacle or self.extra_obstacle == (
                    new_x,
                    new_y,
                ):
                    guard.rotate()
                else:
                    guard.move(new_x, new_y)
            if loop_detected:
                count += 1
        return count


def main(input_file_path: str):
    map = Map(input_file_path)
    steps = map.evaluate_guard_path()
    part_1 = len(set([(step.x, step.y) for step in steps]))
    # print()
    # map.print(steps)
    # 1586 right answer
    # part_2 = None
    part_2 = map.find_loops_efficiently(steps)
    return {"part_1": part_1, "part_2": part_2}


if __name__ == "__main__":
    result = main("./2024_06/2024_06_input.txt")
    print(result)
