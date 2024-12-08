import unittest

from aoc_2024_08 import main


class Test202408(unittest.TestCase):
    def test_day_2024_08(self):
        result = main("./2024_08/2024_08_test.txt")
        self.assertEqual(result["part_1"], 14)
        self.assertEqual(result["part_2"], 34)


if __name__ == "__main__":
    unittest.main()
