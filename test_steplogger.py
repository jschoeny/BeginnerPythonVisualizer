import unittest
import logging

from steplogger import StepLoggerThread


class StepLoggerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.step_logger = StepLoggerThread(None)
        logging.basicConfig(level=logging.DEBUG)

    def test_test1(self):
        _expected = [
            (1, "def my_function():"),
            (8, "def my_function_2():"),
            (14, "my_function()"),
            (2, "x = 20 + 4"),
            (2, "x = \u200A24\u200A"),
            (3, "y = \u200A24\u200A * 2"),
            (3, "y = \u200A48\u200A"),
            (4, "z = \u200A48\u200A / 3"),
            (4, "z = \u200A16.0\u200A"),
            (5, "print(\u200A16.0\u200A)"),
            (15, "my_function_2()"),
            (9, "a = \"Hello\""),
            (9, "a = \u200A'Hello'\u200A"),
            (10, "b = \u200A'Hello'\u200A + \" World\""),
            (10, "b = \u200A'Hello World'\u200A"),
            (11, "print(\u200A'Hello World'\u200A)"),
        ]
        self.step_logger.set_test_file('test_programs/test1.py')
        self.step_logger.start()
        _expected_index = 0
        while self.step_logger.isRunning():
            lineno, line = self.step_logger.next_step()
            if lineno is None:
                continue
            with self.subTest(index=_expected_index):
                self.assertEqual(_expected[_expected_index], (lineno + 1, line.strip("\n\t ")))
            _expected_index += 1
            if _expected_index == len(_expected):
                break
        self.step_logger.next_step()
        self.step_logger.stop()

    def test_test2(self):
        _expected = [
            (1, "def my_loop(repeat):"),
            (8, "my_loop(4)"),
            (2, "for i in range(\u200A4\u200A):"),
            (2, "for \u200A0\u200A in range(\u200A4\u200A):"),
            (3, "x = 2"),
            (3, "x = \u200A2\u200A"),
            (4, "total = \u200A0\u200A + \u200A2\u200A + 1"),
            (4, "total = \u200A3\u200A"),
            (5, "print(\u200A3\u200A)"),
            (2, "for \u200A0\u200A in range(\u200A4\u200A):"),
            (2, "for \u200A1\u200A in range(\u200A4\u200A):"),
            (3, "x = 2"),
            (3, "x = \u200A2\u200A"),
            (4, "total = \u200A1\u200A + \u200A2\u200A + 1"),
            (4, "total = \u200A4\u200A"),
            (5, "print(\u200A4\u200A)"),
            (2, "for \u200A1\u200A in range(\u200A4\u200A):"),
            (2, "for \u200A2\u200A in range(\u200A4\u200A):"),
            (3, "x = 2"),
            (3, "x = \u200A2\u200A"),
            (4, "total = \u200A2\u200A + \u200A2\u200A + 1"),
            (4, "total = \u200A5\u200A"),
            (5, "print(\u200A5\u200A)"),
            (2, "for \u200A2\u200A in range(\u200A4\u200A):"),
            (2, "for \u200A3\u200A in range(\u200A4\u200A):"),
            (3, "x = 2"),
            (3, "x = \u200A2\u200A"),
            (4, "total = \u200A3\u200A + \u200A2\u200A + 1"),
            (4, "total = \u200A6\u200A"),
            (5, "print(\u200A6\u200A)"),
        ]
        self.step_logger.set_test_file('test_programs/test2.py')
        self.step_logger.start()
        _expected_index = 0
        while self.step_logger.isRunning():
            lineno, line = self.step_logger.next_step()
            if lineno is None:
                continue
            with self.subTest(index=_expected_index):
                self.assertEqual(_expected[_expected_index], (lineno + 1, line.strip("\n\t ")))
            _expected_index += 1
            if _expected_index == len(_expected):
                break
        print("\ttest2.py")
        self.step_logger.next_step()
        self.step_logger.stop()


if __name__ == '__main__':
    unittest.main()
