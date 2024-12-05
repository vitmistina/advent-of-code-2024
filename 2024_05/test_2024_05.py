import unittest

from aoc_2024_05 import main

class Test202405(unittest.TestCase):
    def test_day_2024_05(self):
        result = main('./2024_05/2024_05_test.txt')
        self.assertEqual(result["part_1"], 143)
        self.assertEqual(result["part_2"], 123)

if __name__ == "__main__":
    unittest.main()