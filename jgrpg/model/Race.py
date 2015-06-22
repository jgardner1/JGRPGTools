from PyQt5.QtCore import QObject, pyqtSignal

class Race(QObject):
    """A race is a type of creature."""
    removed  = pyqtSignal()
    changed = pyqtSignal()
    
    def __init__(self, **data):
        super(Race, self).__init__()
        self._update(**data)

    def update(self, **data):
        self._update(**data)
        self.changed.emit()

    def _update(self, *,
            name="",
            male_names=[],
            female_names=[],
            family_names=[],
            attribute_modifiers={},
            #         Avg   95%
            height=[ 65.0,  9.5], # inched
            weight=[160.0, 85.0], # lbs
            m_f_ratio=1.0
    ):
        self.name = name
        self.male_names = male_names
        self.female_names = female_names
        self.family_names = family_names
        self.attribute_modifiers = attribute_modifiers
        self.height = height
        self.weight = weight
        self.m_f_ratio = m_f_ratio

    def json(self):
        return {
            'name':self.name,
            "male_names": self.male_names,
            "female_names": self.female_names,
            "family_names": self.family_names,
            "attribute_modifiers": self.attribute_modifiers,
            "height": self.height,
            "weight": self.weight,
            "m_f_ratio": self.m_f_ratio
        }

    def generate_name(self, *, male=False, female=False):
        first_names = None
        if male:
            first_names = self.male_names
        elif female:
            first_names = self.female_names
        else:
            first_names = self.male_names + self.female_names

        name = "{} {}".format(
                self.choose_name(first_names),
                self.choose_name(self.family_names))

        return name.title()

    @staticmethod
    def choose_name(names):
        if not names:
            return "Fred"

        # Sort the names
        prefixes = []
        suffixes = []
        whole_names = []
        for name in names:
            if name.startswith('-'):
                suffixes.append(name[1:])
            elif name.endswith('-'):
                prefixes.append(name[:-1])
            else:
                whole_names.append(name)

        # How many of each?
        combos = len(prefixes) * len(suffixes)
        print("prefixes={}, suffixes={}, combos={}".format(
            prefixes, suffixes, combos))

        # Whole or composed names?
        which = uniform(0, combos+len(whole_names))
        print("which={}, combos={}, which > combos={}".format(
            which,
            combos,
            which > combos))
        if which > combos:
            print("Whole")
            return choice(whole_names)
        else:
            print("composed")
            return choice(prefixes)+choice(suffixes)

    def generate_height_weight(self,
            gender='M',
            attrs={},
            height=0.5,
            weight=0.5,
    ):
        size_mod = pow(
                sqrt(4.0/3.0),
                attrs.get('strength') \
                - attrs.get('dexterity'))

        height = normal(self.height[0], self.height[1]/2.0)*size_mod

        height_variance = height - self.height[0]

        weight = normal(self.weight[0], self.weight[1]/2.0) \
                * height_variance \
                * height_variance

        if gender.lower() in ('f', 'female'):
            height = height/self.m_f_ratio
            weight = weight/self.m_f_ratio

        return (height, weight)
