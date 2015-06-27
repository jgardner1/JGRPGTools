from PyQt5.QtWidgets import QLabel

class MoneyLabel(QLabel):

    def __init__(self, parent=None):
        super(MoneyLabel, self).__init__(parent)

    def setText(self, money):
        if isinstance(money, str):
            text = money
        else:
            text = "{:0.3f} gp".format(money)

        super(MoneyLabel, self).setText(text)
