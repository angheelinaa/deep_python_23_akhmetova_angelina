import unittest
from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    def test_custom_list_add(self):
        cust_lst_1 = CustomList([5, 1, 3, 7])
        cust_lst_2 = CustomList([1, 2, 7])

        result_lst_1 = cust_lst_1 + cust_lst_2

        self.assertEqual([5, 1, 3, 7], cust_lst_1)
        self.assertEqual([1, 2, 7], cust_lst_2)
        self.assertIsInstance(result_lst_1, CustomList)
        for i, elem in enumerate(result_lst_1):
            self.assertEqual(elem, cust_lst_1[i] + (cust_lst_2[i] if i < len(cust_lst_2) else 0))

        result_lst_2 = cust_lst_2 + cust_lst_1

        self.assertEqual([5, 1, 3, 7], cust_lst_1)
        self.assertEqual([1, 2, 7], cust_lst_2)
        self.assertIsInstance(result_lst_2, CustomList)
        for i, elem in enumerate(result_lst_2):
            self.assertEqual(elem, (cust_lst_2[i] if i < len(cust_lst_2) else 0) + cust_lst_1[i])

    def test_custom_list_add_with_list(self):
        cust_lst_1 = CustomList([1])
        cust_lst_2 = CustomList([5, 1, 3, 7])
        lst = [2, 5]

        result_lst_1 = cust_lst_1 + lst

        self.assertEqual([1], cust_lst_1)
        self.assertEqual([2, 5], lst)
        self.assertIsInstance(result_lst_1, CustomList)
        for i, elem in enumerate(result_lst_1):
            self.assertEqual(elem, (cust_lst_1[i] if i < len(cust_lst_1) else 0) + lst[i])

        result_lst_2 = cust_lst_2 + lst

        self.assertEqual([5, 1, 3, 7], cust_lst_2)
        self.assertEqual([2, 5], lst)
        self.assertIsInstance(result_lst_2, CustomList)
        for i, elem in enumerate(result_lst_2):
            self.assertEqual(elem, cust_lst_2[i] + (lst[i] if i < len(lst) else 0))

    def test_custom_list_radd(self):
        cust_lst_1 = CustomList([1])
        cust_lst_2 = CustomList([5, 1, 3, 7])
        lst = [2, 5]

        result_lst_1 = lst + cust_lst_1
        self.assertEqual([1], cust_lst_1)
        self.assertEqual([2, 5], lst)
        self.assertIsInstance(result_lst_1, CustomList)
        for i, elem in enumerate(result_lst_1):
            self.assertEqual(elem, lst[i] + (cust_lst_1[i] if i < len(cust_lst_1) else 0))

        result_lst_2 = lst + cust_lst_2
        self.assertEqual([5, 1, 3, 7], cust_lst_2)
        self.assertEqual([2, 5], lst)
        self.assertIsInstance(result_lst_2, CustomList)
        for i, elem in enumerate(result_lst_2):
            self.assertEqual(elem, (lst[i] if i < len(lst) else 0) + cust_lst_2[i])

    def test_custom_list_sub(self):
        cust_lst_1 = CustomList([5, 1, 3, 7])
        cust_lst_2 = CustomList([1, 2, 7])

        result_lst_1 = cust_lst_1 - cust_lst_2
        self.assertEqual([5, 1, 3, 7], cust_lst_1)
        self.assertEqual([1, 2, 7], cust_lst_2)
        self.assertIsInstance(result_lst_1, CustomList)
        for i, elem in enumerate(result_lst_1):
            self.assertEqual(elem, cust_lst_1[i] - (cust_lst_2[i] if i < len(cust_lst_2) else 0))

        result_lst_2 = cust_lst_2 - cust_lst_1
        self.assertEqual([5, 1, 3, 7], cust_lst_1)
        self.assertEqual([1, 2, 7], cust_lst_2)
        self.assertIsInstance(result_lst_2, CustomList)
        for i, elem in enumerate(result_lst_2):
            self.assertEqual(elem, (cust_lst_2[i] if i < len(cust_lst_2) else 0) - cust_lst_1[i])

    def test_custom_list_sub_with_list(self):
        cust_lst_1 = CustomList([1])
        cust_lst_2 = CustomList([5, 1, 3, 7])
        lst = [2, 5]

        result_lst_1 = cust_lst_1 - lst
        self.assertEqual([1], cust_lst_1)
        self.assertEqual([2, 5], lst)
        self.assertIsInstance(result_lst_1, CustomList)
        for i, elem in enumerate(result_lst_1):
            self.assertEqual(elem, (cust_lst_1[i] if i < len(cust_lst_1) else 0) - lst[i])

        result_lst_2 = cust_lst_2 - lst
        self.assertEqual([5, 1, 3, 7], cust_lst_2)
        self.assertEqual([2, 5], lst)
        self.assertIsInstance(result_lst_2, CustomList)
        for i, elem in enumerate(result_lst_2):
            self.assertEqual(elem, cust_lst_2[i] - (lst[i] if i < len(lst) else 0))

    def test_custom_list_rsub(self):
        cust_lst_1 = CustomList([1])
        cust_lst_2 = CustomList([5, 1, 3, 7])
        lst = [2, 5]

        result_lst_1 = lst - cust_lst_1
        self.assertEqual([1], cust_lst_1)
        self.assertEqual([2, 5], lst)
        self.assertIsInstance(result_lst_1, CustomList)
        for i, elem in enumerate(result_lst_1):
            self.assertEqual(elem, lst[i] - (cust_lst_1[i] if i < len(cust_lst_1) else 0))

        result_lst_2 = lst - cust_lst_2
        self.assertEqual([5, 1, 3, 7], cust_lst_2)
        self.assertEqual([2, 5], lst)
        self.assertIsInstance(result_lst_2, CustomList)
        for i, elem in enumerate(result_lst_2):
            self.assertEqual(elem, (lst[i] if i < len(lst) else 0) - cust_lst_2[i])

    def test_custom_list_str(self):
        cust_lst = CustomList([5, 1, 3, 7])

        self.assertEqual("elements = [5, 1, 3, 7], sum = 16", str(cust_lst))

    def test_custom_list_eq_and_ne(self):
        cust_lst_1 = CustomList([5, 1, 3, 7])
        cust_lst_2 = CustomList([1, 2, 7])
        cust_lst_3 = CustomList([9, -2, 8, 0, 1])

        self.assertFalse(cust_lst_1 == cust_lst_2)
        self.assertTrue(cust_lst_1 == cust_lst_3)

        self.assertTrue(cust_lst_1 != cust_lst_2)
        self.assertFalse(cust_lst_1 != cust_lst_3)

    def test_custom_list_lt_and_le(self):
        cust_lst_1 = CustomList([5, 1, 3, 7])
        cust_lst_2 = CustomList([1, 2, 7])
        cust_lst_3 = CustomList([9, -2, 8, 0, 1])

        self.assertTrue(cust_lst_2 < cust_lst_1)
        self.assertFalse(cust_lst_1 < cust_lst_3)

        self.assertTrue(cust_lst_2 <= cust_lst_1)
        self.assertTrue(cust_lst_1 <= cust_lst_3)
        self.assertFalse(cust_lst_3 <= cust_lst_2)

    def test_custom_list_gt_and_ge(self):
        cust_lst_1 = CustomList([5, 1, 3, 7])
        cust_lst_2 = CustomList([1, 2, 7])
        cust_lst_3 = CustomList([9, -2, 8, 0, 1])

        self.assertTrue(cust_lst_1 > cust_lst_2)
        self.assertFalse(cust_lst_1 > cust_lst_3)

        self.assertTrue(cust_lst_1 >= cust_lst_2)
        self.assertTrue(cust_lst_1 >= cust_lst_3)
        self.assertFalse(cust_lst_2 >= cust_lst_3)
