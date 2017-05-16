import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication

from hackertyper import Hackertyper, format_summary


class HackertyperWidget(QWidget):
    STY_REGULAR = 'font-size: 20px; qproperty-alignment: AlignJustify; font-family: Courier New;'
    STY_ERR = STY_REGULAR + 'color: red;'
    STY_OK = STY_REGULAR + 'color: green'

    def __init__(self, expected_text):
        super().__init__()
        self.expected_text = expected_text
        # self.lines = self.split_to_lines(self.expected_text)
        self.idx = 0

        self.hackertyper = Hackertyper(self.expected_text, user_output=self._update)

        self.label_expected = QLabel(self.expected_text)
        self.label_expected.setStyleSheet(HackertyperWidget.STY_REGULAR)
        self.label_input = QLabel()
        self.label_input.setStyleSheet(HackertyperWidget.STY_REGULAR)
        self.label_status = QLabel()

        lo = QVBoxLayout()
        lo.addWidget(self.label_expected, stretch=0)
        lo.addWidget(self.label_input, stretch=0)
        lo.addWidget(self.label_status, stretch=1)

        self.setLayout(lo)

        self.resize(250, 150)
        self.setWindowTitle('Hackertyper')
        self.show()

        self.modifiers = {Qt.Key_Shift: False, Qt.Key_Alt: False}

    def _update(self, status, ch):
        self.idx += 1
        if self.idx > 1:
            self.label_status.setText(format_summary(self.hackertyper.summary()))
        if status == Hackertyper.ERR:
            self.label_input.setText(self.label_input.text() + '<font color=red>{}</font>'.format(ch))
        else:
            self.label_input.setText(self.label_input.text() + ch)

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return

        if event.key() == Qt.Key_Escape:
            print('ESKEJP')
        elif event.key() == Qt.Key_Return:
            print('new line feed')
        elif event.key() in [Qt.Key_Shift, Qt.Key_Alt]:
            self.modifiers[event.key()] = True
        else:
            if not self.idx < len(self.expected_text):
                return

            ch = '%c' % (event.key())
            ch = ch.upper() if self.modifiers[Qt.Key_Shift] else ch.lower()

            self.hackertyper.key(ch)

    def keyReleaseEvent(self, event):
        if event.key() in [Qt.Key_Shift, Qt.Key_Alt]:
            self.modifiers[event.key()] = False


app = QApplication(sys.argv)
hackertyper = HackertyperWidget('one line of text')