import unittest

from .aoc_2024_04 import extract_diagonal_slices, main


class Test202404(unittest.TestCase):
    def test_day_2024_04(self):
        result = main("./2024_04/2024_04_test.txt")
        self.assertEqual(result["part_1"], 18)
        self.assertEqual(result["part_2"], 9)

    def test_diagonal_slice_extraction(self):
        data = ["ABC", "DEF", "GHI"]
        # expected coordinates:
        # (0,0)
        # (1,0), (0,1)
        # (2,0), (1,1), (0,2)
        # (2,1), (1,2)
        # (2,2)
        result = extract_diagonal_slices(data)
        expected = ["A", "BD", "CEG", "FH", "I"]
        self.assertEqual(result, expected)

        reverse_result = extract_diagonal_slices(list(reversed(data)))
        reverse_expected = ["G", "HD", "IEA", "FB", "C"]
        self.assertEqual(reverse_result, reverse_expected)


if __name__ == "__main__":
    unittest.main()
