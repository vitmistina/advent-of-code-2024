import unittest

from .aoc_2024_21 import find_optimal_expansion, main


class Test202421(unittest.TestCase):
    def test_day_2024_21(self):
        result = main("./2024_21/2024_21_test.txt")
        self.assertEqual(result["part_1"], 126384)
        self.assertGreater(result["part_2"], 126384)

    def test_day_2024_21_expansion(self):
        self.assertEqual(find_optimal_expansion("<A", False), ["v<<A", ">>^A"])
        self.assertEqual(
            find_optimal_expansion("029A", True), ["<A", "^A", "^^>A", "vvvA"]
        )


if __name__ == "__main__":
    unittest.main()
