# -*- coding: utf-8 -*-
"""
.. autoclass:: InchesLabel
    :members:
    :undoc-members:
    :special-members:
    :private-members:

"""
from PyQt5.QtWidgets import QLabel

class InchesLabel(QLabel):
    """
    A QLabel that presents lengths in feet and inches.
    """

    def __init__(self, parent=None):
        super(InchesLabel, self).__init__(parent)

    def setText(self, inches):
        """Sets the text of the QLabel to either the text (if inches is a
        str) or a length in feet and inches."""
        if isinstance(inches, str):
            text = inches
        elif inches > 12.0:
            text = "{}' {:0.2f}\"".format(
                inches // 12,
                inches % 12.0)
        else:
            text = "{:0.2f}\"".format(inches)

        super(InchesLabel, self).setText(text)
