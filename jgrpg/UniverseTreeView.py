from PyQt5.QtWidgets import QTreeView, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

from jgrpg.model import GlobalData, Character, Race, Skill, Personality

import __main__
from jgrpg.ViewRaceWidget import ViewRaceWidget

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

        self.activated.connect(self.item_activated)


    def init_all(self):
        self.init_characters()
        self.init_races()
        self.init_skills()
        self.init_personalities()

    def _set_items(self, item, data):
        item.setRowCount(0)
        subitems = []
        for d in sorted(data, key=lambda r: r.name.lower()):
            subitem = QStandardItem(d.name)
            subitem.setEditable(False)
            subitem.setData(d, Qt.UserRole)
            subitems.append(subitem)

        item.appendRows(subitems)
            

    def init_characters(self):
        self._set_items(self.characters_item, GlobalData.characters)

    def init_races(self):
        self._set_items(self.races_item, GlobalData.races)

    def init_skills(self):
        self._set_items(self.skills_item, GlobalData.skills)

    def init_personalities(self):
        self._set_items(self.personalities_item, GlobalData.personalities)

    def item_activated(self, index):
        item = index.data(Qt.UserRole)
        mdiArea = __main__.main_window.mdiArea

        if isinstance(item, Race):
            windows = __main__.main_window.mdiArea.subWindowList()
            for window in windows:
                widget = window.widget()
                if isinstance(widget, ViewRaceWidget) and widget.race is item:
                    mdiArea.setActiveSubWindow(window)
                    break
            else:
                widget = ViewRaceWidget(item)
                window = mdiArea.addSubWindow(widget)
                item.removed.connect(window.close)
                window.show()

        elif isinstance(item, Character):
            print("character")
        elif isinstance(item, Skill):
            print("skill")
        elif isinstance(item, Personality):
            print("personality")
        else:
            print("none of the above")

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Delete:
            self.delete_current_item()
        else:
            super(UniverseTreeView, self).keyPressEvent(event)
        
    def delete_current_item(self):
        index = self.currentIndex()
        item = index.data(Qt.UserRole)
        
        if not item:
            return
        
        mbox = QMessageBox(
            QMessageBox.Warning,
            "Confirm Delete",
            "Do you want to delete {} ({})?".format(item.name, item.__class__.__name__),
            QMessageBox.Yes | QMessageBox.Cancel)
        ret = mbox.exec_()
        if ret == QMessageBox.Yes:
            GlobalData.deleteRace(item)
    