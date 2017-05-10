#! /usr/bin/python3

import unittest
import unittest.mock


def current_timestamp_ms():
    import time
    return int(round(time.time() * 1000))


def collect(char, buffer):
    buffer.append((char, current_timestamp_ms()))


class CollectTest(unittest.TestCase):
    def setUp(self):
        self.buffer = []

    @unittest.mock.patch('hackertyper.current_timestamp_ms')
    def test_collect_uses_current_timestamp_ms(self, current_timestamp):
        current_timestamp.return_value = 0xDEAD
        collect('c', self.buffer)
        self.assertIn(('c', 0xDEAD), self.buffer)


def validate(char, input_buffer, expected_buffer):
    return char == expected_buffer[len(input_buffer)]


class ValidateTest(unittest.TestCase):
    def test_validate_check_compares_next_expected_char_with_provided(self):
        input_buffer = []
        expected_buffer = ['l', 'o']
        self.assertTrue(validate('l', input_buffer, expected_buffer))


def user_input():
    return 'a'


def hackertyper(challenge_text):
    errors = 0
    input_buffer = []
    while len(input_buffer) < len(challenge_text):
        ch = user_input()
        if not validate(ch, input_buffer, challenge_text):
            errors += 1
        collect(ch, input_buffer)

    return {'errors': errors, 'total': len(challenge_text), 'collected': input_buffer}


class HackertyperTest(unittest.TestCase):
    def setUp(self):
        self.expected_text = 'some sequence of characters'
        self.user_text_1 = 'some saquence of characters'
        self.user_text_2 = 'some saquence of cheracters'

    def test_hackertyper_returns_summary(self):
        summary = hackertyper('')
        self.assertIn('errors', summary)
        self.assertIn('total', summary)

    def test_hackertyper_returns_total_number_of_characters_expected(self):
        summary = hackertyper('asdf')
        self.assertEqual(summary['total'], 4)

    @unittest.mock.patch('hackertyper.user_input')
    def test_no_errors_for_perfectly_matched_input(self, patched_user_input):
        patched_user_input.side_effect = list(self.expected_text)
        summary = hackertyper(self.expected_text)
        self.assertEqual(summary['errors'], 0)

    @unittest.mock.patch('hackertyper.user_input')
    def test_one_error_for_input_with_one_typo(self, patched_user_input):
        patched_user_input.side_effect = list(self.user_text_1)
        summary = hackertyper(self.expected_text)
        self.assertEqual(summary['errors'], 1)

    @unittest.mock.patch('hackertyper.user_input')
    def test_one_error_for_input_with_two_typos(self, patched_user_input):
        patched_user_input.side_effect = list(self.user_text_2)
        summary = hackertyper(self.expected_text)
        self.assertEqual(summary['errors'], 2)

    @unittest.mock.patch('hackertyper.user_input')
    @unittest.mock.patch('hackertyper.current_timestamp_ms')
    def test_hackertyper_returns_collected_data(self, patched_current_timestamp, patched_user_input):
        patched_user_input.side_effect = list(self.user_text_2)
        patched_current_timestamp.return_value = 0
        summary = hackertyper(self.expected_text)
        self.assertEqual(summary['collected'], list(zip(self.user_text_2, [0] * len(self.user_text_2))))

    @unittest.mock.patch('hackertyper.user_input')
    @unittest.mock.patch('hackertyper.current_timestamp_ms')
    def test_hackertyper_returns_collected_data_timestamp_progress(self, patched_current_timestamp, patched_user_input):
        patched_user_input.side_effect = list(self.user_text_2)
        patched_current_timestamp.side_effect = range(0, 1000, 20)
        summary = hackertyper(self.expected_text)
        self.assertEqual(summary['collected'], list(zip(self.user_text_2, range(0, 1000, 20))))


def format_summary(summary):
    errors = summary['errors']
    total = summary['total']
    error_rate = 100.0 * errors / total
    end_time = summary['collected'][-1][1]
    start_time = summary['collected'][0][1]
    duration = round((end_time - start_time) / 1000.0, 4)
    if duration != 0:
        avg_speed = round(60.0 * (total - errors) / duration)
    else:
        avg_speed = '(infinity)'

    return 'Errors {0}({1}%) Avg. Speed {2} CPM'.format(errors, error_rate, avg_speed)


class FormatSummaryTest(unittest.TestCase):
    def test_format_summary(self):
        summary = {'errors': 1, 'total': 10,
                   'collected': [('c', 0), ('o', 1000), ('l', 2000), ('l', 3000), ('e', 4000), ('c', 5000), ('t', 6000), ('e', 7000),
                                 ('d', 8000), ('0', 9000)]}
        self.assertEqual(format_summary(summary), 'Errors 1(10.0%) Avg. Speed 60 CPM')

    def test_format_summary_infinity_speed(self):
        summary = {'errors': 0, 'total': 2,
                   'collected': [('c', 1000), ('o', 1000)]}
        self.assertEqual(format_summary(summary), 'Errors 0(0.0%) Avg. Speed (infinity) CPM')

if __name__ == '__main__':
    expected_text = 'some text'
    print(expected_text)
    print(format_summary(hackertyper(expected_text)))
