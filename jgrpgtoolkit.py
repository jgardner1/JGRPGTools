#!/usr/bin/env python3

import sys

from PyQt5.Qt import Qt

from PyQt5.QtWidgets import (
        QApplication,
        QWidget,
        QMainWindow,
        QMdiArea,
        QMdiSubWindow,
        QTextEdit,
        QVBoxLayout,
        QHBoxLayout,
        QPushButton,
        QLineEdit,
)
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtCore import QUrl

# TODO:
# - Change the card to a QStackLayout, showing either the view or the edit or
# the attributes.
# - Figure out how to handle attributes. What possible types are there? Where
# do you specify the form for a certain type of card? Or do I just allow raw
# JSON?
# - Save / Load cards. File format: JSON of course! Or maybe we need SQLite,
# especially if there are a lot of cards.
# - Menu items for the cards. Load deck, save deck, new card, delete card,
# copy card, etc...
# - Allow cards to be handled over HTTP. This would include monitoring the
# cards for changes?!?
# - Start implementing the card template language. I'll need a full-blown
# parser.

class Card(object):

    def __init__(self, name, content):
        self.name = name
        self.content = content

class CardWebView(QWebView):

    def __init__(self, card, *args, **kwargs):
        QWebView.__init__(self, *args, **kwargs)

        self.card = card

        self.setHtml(card.content)

class CardEditView(QWidget):

    def __init__(self, card, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.card = card

        layout = QVBoxLayout()
        self.setLayout(layout)

        name_edit = self.name_edit = QLineEdit(self)
        name_edit.setText(card.name)
        layout.addWidget(name_edit)


        text_edit = self.text_edit = QTextEdit(self)
        text_edit.setHtml(card.content)
        layout.addWidget(text_edit)

        layout2 = QHBoxLayout()
        save_button = self.save_button = QPushButton("&Save", self)
        layout2.addWidget(save_button)

        cancel_button = self.save_button = QPushButton("&Cancel", self)
        layout2.addWidget(cancel_button)

        layout.addLayout(layout2)



class CardSubWindow(QMdiSubWindow):
    
    def __init__(self, card, *args, **kwargs):
        QMdiSubWindow.__init__(self, *args, **kwargs)

        self.card = card

        card_widget = self.card_widget = CardEditView(card)

        self.setWidget(card_widget)
        self.setWindowTitle(card.name)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)

        cards = self.cards = [
            Card("First Card", "This is the first card."),
            Card("Second Card", "This is the second card."),
            Card("Third Card", "This is the third card."),
            Card("Fourth Card", "This is the fourth card."),
        ]

        self.mdi_area = mdi_area = QMdiArea()
        mdi_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.setCentralWidget(mdi_area)

        for card in cards:
            mdi_area.addSubWindow(CardSubWindow(card))
    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.setWindowTitle("PyQt5 Hypercard")

    main_window.show()


    #w = QWebView()
    #w.setWindowTitle("PyQt5 Hypercard")
    #w.load(QUrl('http://google.com/'))
    #w.show()

    app.exec()
