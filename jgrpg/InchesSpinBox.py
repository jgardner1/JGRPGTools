from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtGui import QValidator

import re

height_re = re.compile(r'(\d+)\'\s*(\d+(?:.\d*))"|(\d+(?:.\d*))\'|(\d+(?:.\d*))"|(\d(?:.\d*))')

class InchesSpinBox(QDoubleSpinBox):

    def __init__(self, parent):
        super(InchesSpinBox, self).__init__(parent)

    def textFromValue(self, value):
        decimals = self.decimals()

        return ("{:0.0f}' {:0."+str(decimals)+"f}\"").format(
                value//12,
                value%12)

    def valueFromText(self, text):
        text = text.strip()
        m = height_re.match(text)
        if m:
            feet, inches = m.group(1,2)
            if feet and inches:
                return int(feet)*12.0 + float(inches)
            feet = m.group(3)
            if feet:
                return float(feet)*12.0
            inches = m.group(4) or m.group(5)
            return float(inches)
        else:
            return 0.0

    def validate(self, text, pos):
        if height_re.match(text.strip()):
            return (QValidator.Acceptable, text, pos)
        else:
            return (QValidator.Invalid, text, pos)
