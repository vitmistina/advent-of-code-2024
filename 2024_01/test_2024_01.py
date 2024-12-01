import unittest

from aoc_2024_01 import main

class Test202401(unittest.TestCase):
    def test_sample(self):
        result = main('./2024_01/2024_01_test.txt')
        self.assertEqual(result["differences"], 11)
        self.assertEqual(result["product"], 31)
        # Add test cases here

if __name__ == "__main__":
    unittest.main()