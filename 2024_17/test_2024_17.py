import unittest

from .aoc_2024_17 import main, convert_to_octal


class Test202417(unittest.TestCase):
    def test_day_2024_17(self):
        result = main("./2024_17/2024_17_test.txt", has_part_2=False)
        self.assertEqual(result["part_1"], "4,6,3,5,6,3,5,2,1,0")
        result = main("./2024_17/2024_17_test_2.txt", has_part_2=True)
        self.assertEqual(result["part_2"], 117440)

    def test_day_2024_17_octal(self):
        self.assertEqual(convert_to_octal(0), "0")
        self.assertEqual(convert_to_octal(7), "7")
        self.assertEqual(convert_to_octal(8), "10")
        self.assertEqual(convert_to_octal(64), "100")
        self.assertEqual(convert_to_octal(64 + 8 + 5), "115")


if __name__ == "__main__":
    unittest.main()
