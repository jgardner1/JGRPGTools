from PyQt5.QtWidgets import QLabel

class InchesLabel(QLabel):

    def __init__(self, parent=None):
        super(InchesLabel, self).__init__(parent)

    def setText(self, inches):
        if isinstance(inches, str):
            text = inches
        elif inches > 12.0:
            text = "{}' {:0.2f}\"".format(
                inches // 12,
                inches % 12.0)
        else:
            text = "{:0.2f}\"".format(inches)

        super(InchesLabel, self).setText(text)
