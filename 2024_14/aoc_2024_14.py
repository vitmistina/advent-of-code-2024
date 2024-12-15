import re
from typing import Dict, List, Set, Tuple
from math import gcd, lcm
import pygame
import sys


class Robot:
    def __init__(self, input_str: str):
        self.position: Tuple[int, int] = self._parse_position(input_str)
        self.velocity: Tuple[int, int] = self._parse_velocity(input_str)

    def __repr__(self):
        return f"(p={self.position}, v={self.velocity})"

    @staticmethod
    def _parse_position(input_str: str) -> Tuple[int, int]:
        position_regex = r"p=(-?\d+),(-?\d+)"
        return tuple(map(int, re.search(position_regex, input_str).groups()))

    @staticmethod
    def _parse_velocity(input_str: str) -> Tuple[int, int]:
        velocity_regex = r"v=(-?\d+),(-?\d+)"
        return tuple(map(int, re.search(velocity_regex, input_str).groups()))

    def move_with_wrapping(self, time: int, bounds: Tuple[int, int]) -> Tuple[int, int]:
        x, y = self.position
        vx, vy = self.velocity
        return (x + vx * time) % bounds[0], (y + vy * time) % bounds[1]


def count_robots_in_quadrants(
    robots: List[Robot], width: int, height: int, time_point: int = 0
) -> Dict[str, int]:
    quadrants = {"TopRight": 0, "TopLeft": 0, "BottomLeft": 0, "BottomRight": 0}
    for robot in robots:
        x, y = robot.move_with_wrapping(time_point, (width, height))
        if x == width // 2 or y == height // 2:
            continue
        if x < width / 2 and y < height / 2:
            quadrants["TopLeft"] += 1
        elif x < width / 2 and y > height / 2:
            quadrants["BottomLeft"] += 1
        elif x > width / 2 and y < height / 2:
            quadrants["TopRight"] += 1
        elif x > width / 2 and y > height / 2:
            quadrants["BottomRight"] += 1
    return quadrants


def print_on_grid(
    robots: List[Robot], width: int, height: int, time: int, copies: int = 1
) -> None:
    pos_count = {}
    for robot in robots:
        x, y = robot.move_with_wrapping(time, (width, height))
        pos_count[(x, y)] = pos_count.get((x, y), 0) + 1
    for y in range(height * copies):
        for x in range(width * copies):
            print(pos_count.get((x % width, y % height), "."), end="")
        print()


def get_treeshape_positions(width: int, height: int) -> Set[Tuple[int, int]]:
    middle = width // 2
    output = set([(middle, 0)])

    for y in range(1, height):
        output.add((middle + y, y))
        output.add((middle - y, y))
    return output


def find_tree_shapes(robots: List[Robot], width: int, height: int) -> int:
    vx, vy = robots[0].velocity
    x_period = width // gcd(width, abs(vx))
    y_period = height // gcd(height, abs(vy))
    period = lcm(x_period, y_period)

    for time in range(period):
        quadrants = count_robots_in_quadrants(robots, width, height, time)
        percent = [q * 100 / len(robots) for q in quadrants.values()]
        if any(p > 50 for p in percent):
            print_on_grid(robots, width, height, time)
            return time


def render_grid(
    robots: List[Robot], width: int, height: int, time: int, time_factor: int
) -> None:
    pygame.init()
    screen = pygame.display.set_mode((width * 4 + 200, height * 4 + 200))
    pygame.display.set_caption("Robot Grid")

    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    running = True
    paused = False

    tick_speed = 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_UP:
                    tick_speed += 1
                elif event.key == pygame.K_DOWN:
                    if tick_speed > 1:
                        tick_speed -= 1
                elif event.key == pygame.K_LEFT:
                    time_factor -= 1
                elif event.key == pygame.K_RIGHT:
                    time_factor += 1
                elif event.key == pygame.K_r:
                    time = 0
                    time_factor = 1

        if not paused:
            time += time_factor

        screen.fill((0, 0, 0))
        pos_count = {}
        for robot in robots:
            x, y = robot.move_with_wrapping(time, (width, height))
            pos_count[(x, y)] = pos_count.get((x, y), 0) + 1

        for (x, y), count in pos_count.items():
            pygame.draw.rect(screen, (255, 255, 255), (x * 4, y * 4, 4, 4))

        time_text = font.render(f"Time: {time}", True, (255, 255, 255))
        screen.blit(time_text, (10, height * 4 + 10))

        tick_factor_text = font.render(
            f"Tick Speed: {tick_speed}", True, (255, 255, 255)
        )
        screen.blit(tick_factor_text, (10, height * 4 + 50))

        time_factor_text = font.render(
            f"Time Factor: {time_factor}", True, (255, 255, 255)
        )
        screen.blit(time_factor_text, (10, height * 4 + 90))

        pygame.display.flip()
        clock.tick(tick_speed)

    pygame.quit()
    sys.exit()


def main(input_file_path: str, width: int, height: int) -> Dict[str, int]:
    with open(input_file_path) as f:
        data = [Robot(line.strip()) for line in f.readlines()]
        quadrants = count_robots_in_quadrants(data, width, height, 100)

        product = 1
        for value in quadrants.values():
            product *= value

        part_2 = find_tree_shapes(data, width, height)

        return {"part_1": product, "part_2": part_2}


if __name__ == "__main__":
    result = main("./2024_14/2024_14_input.txt", 101, 103)
    print(result)
