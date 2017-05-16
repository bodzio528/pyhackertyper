#! /usr/bin/python3


def current_timestamp_ms():
    import time
    return int(round(time.time() * 1000))


def collect(char, buffer):
    buffer.append((char, current_timestamp_ms()))


def validate(char, input_buffer, expected_buffer):
    return char == expected_buffer[len(input_buffer)]


def format_summary(summary):
    errors = summary['errors']
    collected_len = len(summary['collected'])
    error_rate = round(100.0 * errors / collected_len, 1)
    end_time = summary['collected'][-1][1]
    start_time = summary['collected'][0][1]
    duration = round((end_time - start_time) / 1000.0, 4)
    if duration != 0:
        avg_speed = round(60.0 * (collected_len - errors) / duration)
    else:
        avg_speed = '(infinity)'

    return '\nErrors {0}({1}%) Avg. Speed {2} CPM'.format(errors, error_rate, avg_speed)


class Hackertyper(object):
    OK = 0
    ERR = 1

    def __init__(self, challenge_text, user_output):
        self.challenge_text = challenge_text
        self.user_output = user_output
        self.errors = 0
        self.input_buffer = []

    def key(self, user_input):
        if len(self.input_buffer) < len(self.challenge_text):
            if not validate(user_input, self.input_buffer, self.challenge_text):
                self.errors += 1
                self.user_output(Hackertyper.ERR, user_input)
            else:
                self.user_output(Hackertyper.OK, user_input)
        collect(user_input, self.input_buffer)

    def summary(self):
        return {'errors': self.errors, 'total': len(self.challenge_text), 'collected': self.input_buffer}


if __name__ == '__main__':
    # if --gui then start PyQt5 gui
    import sys
    import gui
    sys.exit(gui.app.exec_())
