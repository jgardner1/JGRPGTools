from PyQt5.QtWidgets import QTreeView

from jgrpg.model import GlobalData

class UniverseTreeView(QTreeView):

    def __init__(self, parent=None):
        super(UniverseTreeView, self).__init__(parent)

        self.setModel(GlobalData.universe)
