#! /usr/bin/python3

import threading
import unittest
import unittest.mock


class Collector(object):
    def __init__(self, local_clock):
        self.collected = []
        self.local_clock = local_clock

    def collect(self, char):
        self.collected.append((char, self.local_clock.timestamp()))


class CollectorTest(unittest.TestCase):
    def setUp(self):
        self.local_clock = unittest.mock.MagicMock()
        self.local_clock.timestamp.return_value = 0
        self.sut = Collector(self.local_clock)

    def test_collector_can_collect_characters(self):
        self.sut.collect('c')
        self.assertIn(('c', 0), self.sut.collected)

    def test_collector_adds_timestamp_during_collection(self):
        self.local_clock.timestamp.return_value = 10
        self.sut.collect('c')
        self.assertIn(('c', 10), self.sut.collected)


class Hackertyper(object):
    def __init__(self, buffer, collector, inactivity_timer):
        self.buffer = buffer
        self.collector = collector
        self.inactivity_timer = inactivity_timer

    def receive(self, char):
        self.inactivity_timer.reset()
        if self.buffer.check_character(char):
            self.collector.collect(char)


class HackertyperTest(unittest.TestCase):
    def setUp(self):
        self.buffer = unittest.mock.MagicMock()
        self.buffer.check_character.return_value(True)

        self.collector = unittest.mock.MagicMock()

        self.inactivity_timer = unittest.mock.MagicMock()

        self.sut = Hackertyper(self.buffer, self.collector, self.inactivity_timer)

    def test_hackertyper_collect_only_if_valid_input(self):
        self.sut.receive('c')
        self.buffer.check_character.assert_called_with('c')
        self.collector.collect.assert_called_with('c')

    def test_hackertyper_discard_if_invalid_input(self):
        self.buffer.check_character.return_value = False
        self.sut.receive('c')
        self.buffer.check_character.assert_called_with('c')

    def test_hackertyper_received_input_resets_inactivity_timer(self):
        self.sut.receive('c')
        self.inactivity_timer.reset.assert_called_once_with()


class InactivityTimer(object):
    def __init__(self, interval, timeout_handler):
        self.function = timeout_handler
        self.interval = interval
        self._timer = None
        self._is_running = False

    def start(self):
        self._is_running = True
        self._timer = threading.Timer(self.interval, self.function)
        self._timer.start()

    def stop(self):
        if self._is_running:
            self._timer.cancel()
            self._is_running = False

    def reset(self):
        self.stop()
        self.start()


class InactivityTimerTest(unittest.TestCase):
    def setUp(self):
        pass

    @unittest.skip('Time costly')
    def test_can_be_restarted(self):
        obj = unittest.mock.MagicMock()
        sut = InactivityTimer(interval=1, timeout_handler=obj.timeout_handler)
        sut.reset()
        sut.reset()
        from time import sleep
        sleep(1)
        obj.timeout_handler.assert_called_once_with()


class LocalClock(object):
    def __init__(self):
        self._paused = True

    def pause(self):
        pass

    def timestamp(self):
        return 0


class LocalClockTest(unittest.TestCase):
    def setUp(self):
        self.sut = LocalClock()

    def test_local_clock_can_be_paused_on_request(self):
        self.sut.pause()

    def test_local_clock_first_timestamp_is_always_zero(self):
        self.assertEqual(self.sut.timestamp(), 0)

if __name__ == '__main__':
    pass
    # buffer = Buffer()
    # local_clock = LocalClock()
    # inactivity_timer = InactivityTimer(5, local_clock.pause)
    # collector = Collector(local_clock)
    # hackertyper = Hackertyper(buffer, collector, inactivity_timer)