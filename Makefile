PYTHON=/usr/bin/env python3
PYUIC=PyQt5.uic.pyuic

ui/%_auto.py: ui/%.ui
	$(PYTHON) -m $(PYUIC) $< -o $@

all: ui/MainWindow_auto.py ui/Character_auto.py

