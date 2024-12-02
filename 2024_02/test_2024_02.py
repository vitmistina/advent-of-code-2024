import unittest

from aoc_2024_02 import main

class Test202402(unittest.TestCase):
    def test_day_2024_02(self):
        result = main('./2024_02/2024_02_test.txt')
        self.assertEqual(result["part_1"], 2)
        self.assertEqual(result["part_2"], 4)
        # Add test cases here

if __name__ == "__main__":
    unittest.main()