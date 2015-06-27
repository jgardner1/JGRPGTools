from PyQt5.QtWidgets import QLabel

class WeightLabel(QLabel):

    def __init__(self, parent=None):
        super(WeightLabel, self).__init__(parent)

    def setText(self, weight):
        if isinstance(weight, str):
            text = weight
        else:
            text = "{:0.2f} lbs".format(weight)

        super(WeightLabel, self).setText(text)

