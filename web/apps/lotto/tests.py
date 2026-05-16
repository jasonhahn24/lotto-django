from django.test import TestCase
from .utils import generate_auto_numbers, check_prize_rank


class UtilsTest(TestCase):

    def test_auto_numbers_length(self):
        nums = generate_auto_numbers()
        self.assertEqual(len(nums), 6)

    def test_auto_numbers_range(self):
        nums = generate_auto_numbers()
        self.assertTrue(all(1 <= n <= 45 for n in nums))

    def test_auto_numbers_unique(self):
        nums = generate_auto_numbers()
        self.assertEqual(len(nums), len(set(nums)))

    def test_auto_numbers_sorted(self):
        nums = generate_auto_numbers()
        self.assertEqual(nums, sorted(nums))

    def test_prize_rank_1st(self):
        draw = [1, 2, 3, 4, 5, 6]
        rank, _ = check_prize_rank([1, 2, 3, 4, 5, 6], draw, 7)
        self.assertEqual(rank, 1)

    def test_prize_rank_2nd(self):
        draw = [1, 2, 3, 4, 5, 6]
        rank, _ = check_prize_rank([1, 2, 3, 4, 5, 7], draw, 7)
        self.assertEqual(rank, 2)

    def test_prize_rank_3rd(self):
        draw = [1, 2, 3, 4, 5, 6]
        rank, _ = check_prize_rank([1, 2, 3, 4, 5, 8], draw, 7)
        self.assertEqual(rank, 3)

    def test_prize_rank_no_prize(self):
        draw = [1, 2, 3, 4, 5, 6]
        rank, _ = check_prize_rank([10, 11, 12, 13, 14, 15], draw, 7)
        self.assertEqual(rank, 0)