import unittest
import hackertyper


class HackertyperTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_check_character_returns_true_for_correct_input(self):
        self.assertTrue(hackertyper.check_character(actual=' ', expected=' '))

if __name__ == '__main__':
    unittest.main()
