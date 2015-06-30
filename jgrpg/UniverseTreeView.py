from PyQt5.QtWidgets import QTreeView, QMessageBox, QMdiSubWindow, QMenu
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

from jgrpg.model import (
        GlobalData, Character, Race, Skill, Personality, ItemPrototypes, Groups,
        ObjectStore,
)

import __main__

class UniverseTreeView(QTreeView):

    def __init__(self, parent=None):
        super(UniverseTreeView, self).__init__(parent)

        model = QStandardItemModel()
        self.setModel(model)

        root_item = model.invisibleRootItem()
        self.characters_item = QStandardItem("Characters")
        self.characters_item.setEditable(False)
        root_item.appendRow(self.characters_item)

        GlobalData.character_added.connect(self.init_characters)
        GlobalData.character_removed.connect(self.init_characters)
        GlobalData.characters_reset.connect(self.init_characters)


        self.races_item = QStandardItem("Races")
        self.races_item.setEditable(False)
        root_item.appendRow(self.races_item)

        GlobalData.race_added.connect(self.init_races)
        GlobalData.race_removed.connect(self.init_races)
        GlobalData.races_reset.connect(self.init_races)


        self.skills_item = QStandardItem("Skills")
        self.skills_item.setEditable(False)
        root_item.appendRow(self.skills_item)

        GlobalData.skill_added.connect(self.init_skills)
        GlobalData.skill_removed.connect(self.init_skills)
        GlobalData.skills_reset.connect(self.init_skills)


        self.personalities_item = QStandardItem("Personalities")
        self.personalities_item.setEditable(False)
        root_item.appendRow(self.personalities_item)

        GlobalData.personality_added.connect(self.init_personalities)
        GlobalData.personality_removed.connect(self.init_personalities)
        GlobalData.personalities_reset.connect(self.init_personalities)


        self.backgrounds_item = QStandardItem("Backgrounds")
        self.backgrounds_item.setEditable(False)
        root_item.appendRow(self.backgrounds_item)

        GlobalData.background_added.connect(self.init_backgrounds)
        GlobalData.background_removed.connect(self.init_backgrounds)
        GlobalData.backgrounds_reset.connect(self.init_backgrounds)


        self.item_prototypes_item = QStandardItem("Item Prototypes")
        self.item_prototypes_item.setData(ItemPrototypes, Qt.UserRole)
        self.item_prototypes_item.setEditable(False)
        root_item.appendRow(self.item_prototypes_item)

        ItemPrototypes.added.connect(self.init_item_prototypes)
        ItemPrototypes.removed.connect(self.init_item_prototypes)
        ItemPrototypes.reset.connect(self.init_item_prototypes)

        self.groups_item = QStandardItem("Groups")
        self.groups_item.setData(Groups, Qt.UserRole)
        self.groups_item.setEditable(False)
        root_item.appendRow(self.groups_item)

        Groups.added.connect(self.init_groups)
        Groups.removed.connect(self.init_groups)
        Groups.reset.connect(self.init_groups)

        self.init_all()

        self.activated.connect(self.item_activated)


    def init_all(self):
        self.init_characters()
        self.init_races()
        self.init_skills()
        self.init_personalities()
        self.init_backgrounds()
        self.init_item_prototypes()
        self.init_groups()

    def _set_items(self, item, data):
        item.setRowCount(0)
        subitems = []
        for d in sorted(data, key=lambda r: r.name.lower()):
            subitems.append(Item(d))

        item.appendRows(subitems)


    def init_characters(self):
        self._set_items(self.characters_item, GlobalData.characters)

    def init_races(self):
        self._set_items(self.races_item, GlobalData.races)

    def init_skills(self):
        self._set_items(self.skills_item, GlobalData.skills)

    def init_personalities(self):
        self._set_items(self.personalities_item, GlobalData.personalities)

    def init_backgrounds(self):
        self._set_items(self.backgrounds_item, GlobalData.backgrounds)

    def init_item_prototypes(self):
        self._set_items(self.item_prototypes_item, ItemPrototypes)

    def init_groups(self):
        self._set_items(self.groups_item, Groups)

    def item_activated(self, index):
        item = index.data(Qt.UserRole)

        if not item:
            return

        mw = __main__.main_window

        if isinstance(item, ObjectStore):
            mw.create(item.cls)
        else:
            mw.viewObject(item)


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

        __main__.main_window.deleteObject(item)

    def contextMenuEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid():
            target = index.data(Qt.UserRole)
            if target:
                if isinstance(target, ObjectStore):
                    menu = ObjectStoreContextMenu(target)
                else:
                    menu = ContextMenu(target)
                menu.exec(event.globalPos())


class Item(QStandardItem):

        def __init__(self, item):
            super(Item, self).__init__()
            self.item = item

            self.setEditable(False)
            self.setData(item, Qt.UserRole)

            self.item.changed.connect(self.update)
            self.update()

        def update(self):
            self.setData(self.item.name, Qt.DisplayRole)

class ObjectStoreContextMenu(QMenu):

    def __init__(self, target):
        self.target = target
        super(ObjectStoreContextMenu, self).__init__()

        self.createAction = self.addAction("Create")
        self.createAction.triggered.connect(self.create)

    def create(self):
        __main__.main_window.create(self.target.cls)

class ContextMenu(QMenu):

    def __init__(self, target):
        self.target = target
        super(ContextMenu, self).__init__()

        self.viewAction = self.addAction("View")
        self.viewAction.triggered.connect(self.view)

        self.addAction("Copy")

        self.deleteAction = self.addAction("Delete")
        self.deleteAction.triggered.connect(self.delete)

        self.editAction = self.addAction("Edit")
        self.editAction.triggered.connect(self.edit)

        if isinstance(target, Race):
            self.createAction = self.addAction("Create Character from This Race")
            self.createAction.triggered.connect(self.create_character_from_race)

    def view(self):
        __main__.main_window.viewObject(self.target)

    def edit(self):
        __main__.main_window.editObject(self.target)

    def delete(self):
        __main__.main_window.deleteObject(self.target)

    def create_character_from_race(self):
        mw = __main__.main_window
        mw.createCharacter(self.target)

