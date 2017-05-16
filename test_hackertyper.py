import unittest
import unittest.mock

from hackertyper import collect, validate, format_summary, Hackertyper


class CollectTest(unittest.TestCase):
    def setUp(self):
        self.buffer = []

    @unittest.mock.patch('hackertyper.current_timestamp_ms')
    def test_collect_uses_current_timestamp_ms(self, current_timestamp):
        current_timestamp.return_value = 0xDEAD
        collect('c', self.buffer)
        self.assertIn(('c', 0xDEAD), self.buffer)


class ValidateTest(unittest.TestCase):
    def test_validate_returns_true_if_expected_and_provided_matche(self):
        input_buffer = []
        expected_buffer = ['l', 'o']
        self.assertTrue(validate('l', input_buffer, expected_buffer))

    def test_validate_returns_false_when_expected_and_provided_do_not_match(self):
        input_buffer = []
        expected_buffer = ['l', 'o']
        self.assertFalse(validate('o', input_buffer, expected_buffer))


class FormatSummaryTest(unittest.TestCase):
    def test_format_summary(self):
        summary = {'errors': 1, 'total': 10,
                   'collected': [('c', 0), ('o', 1000), ('l', 2000), ('l', 3000), ('e', 4000), ('c', 5000),
                                 ('t', 6000), ('e', 7000), ('d', 8000), ('0', 9000)]}
        self.assertEqual(format_summary(summary), '\nErrors 1(10.0%) Avg. Speed 60 CPM')

    def test_format_summary_infinity_speed(self):
        summary = {'errors': 0, 'total': 2,
                   'collected': [('c', 1000), ('o', 1000)]}
        self.assertEqual(format_summary(summary), '\nErrors 0(0.0%) Avg. Speed (infinity) CPM')


class HackertyperTest(unittest.TestCase):
    def setUp(self):
        self.expected_text = 'some sequence of characters'
        self.user_text_1 = 'some saquence of characters'
        self.user_text_2 = 'some saquence of cheracters'
        self.user_output_mock = unittest.mock.Mock()
        self.sut = Hackertyper(self.expected_text, self.user_output_mock)

    def test_hackertyper_returns_summary(self):
        self.sut = Hackertyper('', self.user_output_mock)
        summary = self.sut.summary()
        self.assertIn('errors', summary)
        self.assertIn('total', summary)

    def test_hackertyper_returns_total_number_of_characters_expected(self):
        self.sut = Hackertyper('asdf', self.user_output_mock)
        summary = self.sut.summary()
        self.assertEqual(summary['total'], 4)

    def test_no_errors_for_perfectly_matched_input(self):
        for ch in self.expected_text:
            self.sut.key(ch)
        summary = self.sut.summary()
        self.assertEqual(summary['errors'], 0)
        self.assertEqual(self.user_output_mock.call_count, len(self.expected_text))
        self.user_output_mock.assert_called_with(Hackertyper.OK, unittest.mock.ANY)

    def test_one_error_for_input_with_one_typo(self):
        for ch in self.user_text_1:
            self.sut.key(ch)
        summary = self.sut.summary()
        self.assertEqual(summary['errors'], 1)
        self.user_output_mock.assert_any_call(Hackertyper.ERR, 'a')
        self.user_output_mock.assert_called_with(Hackertyper.OK, unittest.mock.ANY)

    def test_one_error_for_input_with_two_typos(self):
        for ch in self.user_text_2:
            self.sut.key(ch)
        summary = self.sut.summary()
        self.assertEqual(summary['errors'], 2)

    @unittest.mock.patch('hackertyper.current_timestamp_ms')
    def test_hackertyper_returns_collected_data(self, patched_current_timestamp):
        patched_current_timestamp.return_value = 0
        for ch in self.user_text_2:
            self.sut.key(ch)
        summary = self.sut.summary()
        self.assertEqual(summary['collected'], list(zip(self.user_text_2, [0] * len(self.user_text_2))))

    @unittest.mock.patch('hackertyper.current_timestamp_ms')
    def test_hackertyper_returns_collected_data_timestamp_progress(self, patched_current_timestamp):
        patched_current_timestamp.side_effect = range(0, 1000, 20)
        for ch in self.user_text_2:
            self.sut.key(ch)
        summary = self.sut.summary()
        self.assertEqual(summary['collected'], list(zip(self.user_text_2, range(0, 1000, 20))))
