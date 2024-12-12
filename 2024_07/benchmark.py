from time import time
from .aoc_2024_07 import Calibrator, PartType

if __name__ == "__main__":
    with open("./2024_07/2024_07_input.txt") as f:
        data = [line.strip().split(":") for line in f.readlines()]
        lines = [(int(line[0]), list(map(int, line[1].split()))) for line in data]

        algo_times = {}
        results = {}
        pt_2_calibrator = Calibrator(PartType.PART_2)

        time_pre_run = time()
        part_2_results_bfs = [
            (pt_2_calibrator.breadth_first_search(expected, nums), expected, nums)
            for expected, nums in lines
        ]
        results["bfs"] = sum(
            expected
            for operator, expected, nums in part_2_results_bfs
            if operator is not None
        )
        algo_times["bfs"] = time() - time_pre_run

        time_pre_run = time()
        part_2_results = [
            (pt_2_calibrator.roll_up_with_expressions(expected, nums), expected, nums)
            for expected, nums in lines
        ]
        results["recursion"] = sum(
            expected
            for operator, expected, nums in part_2_results
            if operator is not None
        )
        algo_times["recursion"] = time() - time_pre_run

        time_pre_run = time()
        part_2_results_dfs = [
            (pt_2_calibrator.depth_first_search(expected, nums), expected, nums)
            for expected, nums in lines
        ]
        results["dfs"] = sum(
            expected
            for operator, expected, nums in part_2_results_dfs
            if operator is not None
        )
        algo_times["dfs"] = time() - time_pre_run

        time_pre_run = time()
        part_2_results_backtrace = [
            (pt_2_calibrator.backtrace(expected, nums), expected, nums)
            for operator, expected, nums in part_2_results
        ]
        results["backtrace"] = sum(
            expected
            for operator, expected, nums in part_2_results_backtrace
            if operator is not None
        )
        algo_times["backtrace"] = time() - time_pre_run

        print(algo_times)
        print(results)
