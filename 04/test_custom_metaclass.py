import unittest
from custom_metaclass import CustomMeta


class TestCustomClass(metaclass=CustomMeta):
    test_attr = 50

    def __init__(self, val=99):
        self.val = val

    def test_method(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"


class TestCustomMeta(unittest.TestCase):
    def test_custom_meta_class_attrs(self):
        self.assertIsInstance(TestCustomClass, CustomMeta)

        self.assertTrue(hasattr(TestCustomClass, "custom_test_attr"))
        self.assertFalse(hasattr(TestCustomClass, "test_attr"))
        self.assertEqual(50, TestCustomClass.custom_test_attr)

        self.assertTrue(hasattr(TestCustomClass, "custom_test_method"))
        self.assertFalse(hasattr(TestCustomClass, "test_method"))

        self.assertTrue(hasattr(TestCustomClass, "__init__"))
        self.assertFalse(hasattr(TestCustomClass, "custom___init__"))

        self.assertTrue(hasattr(TestCustomClass, "__str__"))
        self.assertFalse(hasattr(TestCustomClass, "custom___str__"))

    def test_custom_meta_instance_attrs(self):
        inst_1 = TestCustomClass()
        inst_2 = TestCustomClass(-20)

        self.assertTrue(hasattr(inst_1, "custom_val"))
        self.assertFalse(hasattr(inst_1, "val"))
        self.assertEqual(99, inst_1.custom_val)
        self.assertTrue(hasattr(inst_2, "custom_val"))
        self.assertFalse(hasattr(inst_2, "val"))
        self.assertEqual(-20, inst_2.custom_val)

        self.assertTrue(hasattr(inst_1, "custom_test_method"))
        self.assertFalse(hasattr(inst_1, "test_method"))
        self.assertEqual(100, inst_1.custom_test_method())
        self.assertTrue(hasattr(inst_2, "custom_test_method"))
        self.assertFalse(hasattr(inst_2, "test_method"))
        self.assertEqual(100, inst_2.custom_test_method())

        self.assertTrue(hasattr(inst_1, "custom_test_attr"))
        self.assertFalse(hasattr(inst_1, "test_attr"))
        self.assertEqual(50, inst_1.custom_test_attr)
        self.assertTrue(hasattr(inst_2, "custom_test_attr"))
        self.assertFalse(hasattr(inst_2, "test_attr"))
        self.assertEqual(50, inst_2.custom_test_attr)

        self.assertTrue(hasattr(inst_1, "__str__"))
        self.assertFalse(hasattr(inst_1, "custom___str__"))
        self.assertEqual("Custom_by_metaclass", str(inst_1))
        self.assertTrue(hasattr(inst_2, "__str__"))
        self.assertFalse(hasattr(inst_2, "custom___str__"))
        self.assertEqual("Custom_by_metaclass", str(inst_2))

    def test_custom_meta_additional_attrs(self):
        inst = TestCustomClass()

        inst.dynamic = "added instance attr"
        self.assertTrue(hasattr(inst, "custom_dynamic"))
        self.assertFalse(hasattr(inst, "dynamic"))
        self.assertEqual("added instance attr", inst.custom_dynamic)

        TestCustomClass.class_dynamic = "added class attr"
        self.assertTrue(hasattr(TestCustomClass, "custom_class_dynamic"))
        self.assertFalse(hasattr(TestCustomClass, "class_dynamic"))
        self.assertEqual("added class attr", TestCustomClass.custom_class_dynamic)
