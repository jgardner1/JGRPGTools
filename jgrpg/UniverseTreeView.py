from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from jgrpg.model import GlobalData

class UniverseTreeView(QTreeView):

    def __init__(self, parent=None):
        super(UniverseTreeView, self).__init__(parent)

        model = QStandardItemModel()
        self.setModel(model)

        root_item = model.invisibleRootItem()
        self.characters_item = QStandardItem("Characters")
        self.characters_item.setEditable(False)

        self.races_item = QStandardItem("Races")
        self.races_item.setEditable(False)

        self.skills_item = QStandardItem("Skills")
        self.skills_item.setEditable(False)

        self.personalities_item = QStandardItem("Personalities")
        self.personalities_item.setEditable(False)

        root_item.appendRow(self.characters_item)
        root_item.appendRow(self.races_item)
        root_item.appendRow(self.skills_item)
        root_item.appendRow(self.personalities_item)

        self.init_all()

        GlobalData.character_added.connect(self.init_characters)
        GlobalData.character_removed.connect(self.init_characters)
        GlobalData.characters_reset.connect(self.init_characters)

        GlobalData.race_added.connect(self.init_races)
        GlobalData.race_removed.connect(self.init_races)
        GlobalData.races_reset.connect(self.init_races)

        GlobalData.skill_added.connect(self.init_skills)
        GlobalData.skill_removed.connect(self.init_skills)
        GlobalData.skills_reset.connect(self.init_skills)

        GlobalData.personality_added.connect(self.init_personalities)
        GlobalData.personality_removed.connect(self.init_personalities)
        GlobalData.personalities_reset.connect(self.init_personalities)


    def init_all(self):
        self.init_characters()
        self.init_races()
        self.init_skills()
        self.init_personalities()

    def init_characters(self):
        item = self.characters_item
        # Deletes all the rows
        item.setRowCount(0)

        subitems = [QStandardItem(_.name)
            for _ in GlobalData.characters]
        for subitem in subitems:
            subitem.setEditable(False)

        item.appendRows(subitems)

    def init_races(self):
        item = self.races_item
        # Deletes all the rows
        item.setRowCount(0)

        subitems = [QStandardItem(_.name)
            for _ in GlobalData.races]
        for subitem in subitems:
            subitem.setEditable(False)

        item.appendRows(subitems)

    def init_skills(self):
        item = self.skills_item
        # Deletes all the rows
        item.setRowCount(0)

        subitems = [QStandardItem(_.name)
            for _ in GlobalData.skills]
        for subitem in subitems:
            subitem.setEditable(False)

        item.appendRows(subitems)

    def init_personalities(self):
        item = self.personalities_item
        # Deletes all the rows
        item.setRowCount(0)

        subitems =[QStandardItem(_.name)
            for _ in GlobalData.personalities]
        for subitem in subitems:
            subitem.setEditable(False)

        item.appendRows(subitems)


            
            
