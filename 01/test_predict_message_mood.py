import unittest
from unittest import mock
from predict_message_mood import SomeModel, predict_message_mood


class TestPredictMessageMood(unittest.TestCase):
    def setUp(self):
        self.model = SomeModel()

    def test_predict(self):
        for _ in range(10):
            prediction = self.model.predict("text")
            self.assertLessEqual(prediction, 1)
            self.assertGreaterEqual(prediction, 0)

    def test_predict_message_mood_simple(self):
        message = "text"

        with mock.patch("predict_message_mood.SomeModel.predict") as mock_somemodel_predict:
            mock_somemodel_predict.side_effect = [0.2, 0.5, 0.9]

            self.assertEqual("неуд", predict_message_mood(message, self.model))
            self.assertEqual("норм", predict_message_mood(message, self.model))
            self.assertEqual("отл", predict_message_mood(message, self.model))

            expected_calls = [
                mock.call("text"),
                mock.call("text"),
                mock.call("text"),
            ]
            self.assertEqual(expected_calls, mock_somemodel_predict.mock_calls)

    def test_predict_message_mood_empty(self):
        message = ""

        with mock.patch("predict_message_mood.SomeModel.predict") as mock_somemodel_predict:
            mock_somemodel_predict.side_effect = [0.2, 0.5, 0.9]

            self.assertEqual("неуд", predict_message_mood(message, self.model))
            self.assertEqual("норм", predict_message_mood(message, self.model))
            self.assertEqual("отл", predict_message_mood(message, self.model))

            expected_calls = [
                mock.call(""),
                mock.call(""),
                mock.call(""),
            ]
            self.assertEqual(expected_calls, mock_somemodel_predict.mock_calls)

    def test_predict_message_mood_expected_values(self):
        expected_values = ["неуд", "отл", "норм"]

        for _ in range(10):
            self.assertIn(predict_message_mood("text", self.model), expected_values)

    def test_predict_message_mood_boundary_conditions(self):
        message = "text"

        with mock.patch("predict_message_mood.SomeModel.predict") as mock_somemodel_predict:
            mock_somemodel_predict.side_effect = [0.3, 0.8]

            self.assertEqual("норм", predict_message_mood(message, self.model))
            self.assertEqual("норм", predict_message_mood(message, self.model))

            expected_calls = [
                mock.call("text"),
                mock.call("text"),
            ]
            self.assertEqual(expected_calls, mock_somemodel_predict.mock_calls)

            mock_somemodel_predict.side_effect = [0.0, 1.0]

            self.assertEqual("неуд", predict_message_mood(message, self.model))
            self.assertEqual("отл", predict_message_mood(message, self.model))

            expected_calls = [
                mock.call("text"),
                mock.call("text"),
                mock.call("text"),
                mock.call("text"),
            ]
            self.assertEqual(expected_calls, mock_somemodel_predict.mock_calls)

    def test_predict_message_mood_set_thresholds(self):
        message = "text"

        with mock.patch("predict_message_mood.SomeModel.predict") as mock_somemodel_predict:
            mock_somemodel_predict.return_value = 0.5

            self.assertEqual("неуд", predict_message_mood(message, self.model, bad_thresholds=0.6))
            self.assertEqual("отл", predict_message_mood(message, self.model, good_thresholds=0.4))
            self.assertEqual("отл", predict_message_mood(message, self.model, bad_thresholds=0.1,
                                                         good_thresholds=0.4))

            expected_calls = [
                mock.call("text"),
                mock.call("text"),
                mock.call("text"),
            ]
            self.assertEqual(expected_calls, mock_somemodel_predict.mock_calls)

    def test_predict_message_mood_incorrect_thresholds(self):
        message = "text"

        with self.assertRaises(ValueError) as err:
            predict_message_mood(message, self.model, bad_thresholds=0.8, good_thresholds=0.3)

        self.assertEqual("good_thresholds should be greater than bad_thresholds",
                         str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            predict_message_mood(message, self.model, bad_thresholds="0.3", good_thresholds=0.8)

        self.assertEqual("bad_thresholds and good_thresholds expected as"
                         " instance of float", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            predict_message_mood(message, self.model, bad_thresholds=0.3, good_thresholds="0.8")

        self.assertEqual("bad_thresholds and good_thresholds expected as"
                         " instance of float", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            predict_message_mood(message, self.model, bad_thresholds="0.3", good_thresholds="0.8")

        self.assertEqual("bad_thresholds and good_thresholds expected as "
                         "instance of float", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

    def test_predict_message_mood_error_type_msg_model(self):
        with self.assertRaises(TypeError) as err:
            predict_message_mood(123, self.model)

        self.assertEqual("message expected as instance of str and model expected as "
                         "instance of SomeModel", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            predict_message_mood("123", "model")

        self.assertEqual("message expected as instance of str and model expected as"
                         " instance of SomeModel", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            predict_message_mood(123, "model")

        self.assertEqual("message expected as instance of str and model expected as "
                         "instance of SomeModel", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))
