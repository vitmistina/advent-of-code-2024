import unittest

from .aoc_2024_23 import main


class Test202423(unittest.TestCase):
    def test_day_2024_23(self):
        result = main("./2024_23/2024_23_test.txt", False)
        self.assertEqual(result["part_1"], 7)
        result = main("./2024_23/2024_23_test_2.txt", True)
        self.assertEqual(result["part_2"], "co,de,ka,ta")


if __name__ == "__main__":
    unittest.main()
