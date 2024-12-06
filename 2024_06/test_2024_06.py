import unittest

from aoc_2024_06 import main

class Test202406(unittest.TestCase):
    def test_day_2024_06(self):
        result = main('./2024_06/2024_06_test.txt')
        self.assertEqual(result["part_1"], 41)
        self.assertEqual(result["part_2"], 6)

if __name__ == "__main__":
    unittest.main()