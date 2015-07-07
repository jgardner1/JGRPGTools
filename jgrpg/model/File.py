import json

from PyQt5.QtCore import pyqtSignal, QObject

from .Race import Races
from .Character import Characters
from .Item import ItemPrototypes
from .Group import Groups
from .Area import Areas

class File(QObject):

    def __init__(self):
        super(File, self).__init__()
        self.filename = None

        self.new()

    def new(self):
        self.load_from_json('default.jgu')
        
        self.filename = None

    def open(self, filename):
        self.load_from_json(filename)

        if filename != self.filename:
            self.filename = filename
            self.filename_changed.emit(self.filename)

    def load_from_json(self, f):
        data = json.load(open(f, 'r', encoding='utf8'))
        self.init_from_data(**data)

    def init_from_data(self, *,
            races=[],
            characters=[],
            item_prototypes=[],
            groups=[],
            areas=[]
    ):
        Races.load(races)
        Characters.load(characters)
        ItemPrototypes.load(item_prototypes)
        Groups.load(groups)
        Areas.load(areas)


    def save(self, filename=None):
        filename = filename or self.filename
        self.save_to_json(filename)
        if filename != self.filename:
            self.filename = filename
            self.filename_changed.emit(self.filename)

    def save_to_json(self, f):
        data = json.dump({
            'characters':Characters.save(),
            'races':[_.json() for _ in self.races],
            'skills':[_.json() for _ in self.skills],
            'personalities':[_.json() for _ in self.personalities],
            'item_prototypes':ItemPrototypes.save(),
            'groups':Groups.save(),
            'areas':Areas.save(),
        }, open(f, 'w', encoding='utf8'), indent=2)

