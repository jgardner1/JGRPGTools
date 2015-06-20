from PyQt5.QtWidgets import QDoubleSpinBox

class ModifierSpinBox(QDoubleSpinBox):

    def __init__(self, parent):
        super(ModifierSpinBox, self).__init__(parent)

    def textFromValue(self, value):
        decimals = self.decimals()

        return ("{:+0."+str(decimals)+"f}").format(value)
