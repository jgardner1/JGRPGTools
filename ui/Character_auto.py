# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/Character.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Character(object):
    def setupUi(self, Character):
        Character.setObjectName("Character")
        Character.resize(480, 452)
        self.verticalLayout = QtWidgets.QVBoxLayout(Character)
        self.verticalLayout.setObjectName("verticalLayout")
        self.nameLineEdit = QtWidgets.QLineEdit(Character)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.verticalLayout.addWidget(self.nameLineEdit)
        self.tabWidget = QtWidgets.QTabWidget(Character)
        self.tabWidget.setObjectName("tabWidget")
        self.mainTab = QtWidgets.QWidget()
        self.mainTab.setObjectName("mainTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.mainTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = CharacterVitalStatisticsWidget(self.mainTab)
        self.widget.setObjectName("widget")
        self.verticalLayout_2.addWidget(self.widget)
        self.tabWidget.addTab(self.mainTab, "")
        self.equipmentTab = QtWidgets.QWidget()
        self.equipmentTab.setObjectName("equipmentTab")
        self.tabWidget.addTab(self.equipmentTab, "")
        self.skillsMagicTab = QtWidgets.QWidget()
        self.skillsMagicTab.setObjectName("skillsMagicTab")
        self.tabWidget.addTab(self.skillsMagicTab, "")
        self.personalityTab = QtWidgets.QWidget()
        self.personalityTab.setObjectName("personalityTab")
        self.tabWidget.addTab(self.personalityTab, "")
        self.historyTab = QtWidgets.QWidget()
        self.historyTab.setObjectName("historyTab")
        self.tabWidget.addTab(self.historyTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.idLabel = QtWidgets.QLabel(Character)
        self.idLabel.setTextFormat(QtCore.Qt.PlainText)
        self.idLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.idLabel.setObjectName("idLabel")
        self.verticalLayout.addWidget(self.idLabel)

        self.retranslateUi(Character)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Character)

    def retranslateUi(self, Character):
        _translate = QtCore.QCoreApplication.translate
        Character.setWindowTitle(_translate("Character", "Form"))
        self.nameLineEdit.setPlaceholderText(_translate("Character", "Character Name"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mainTab), _translate("Character", "Vital Statistics"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.equipmentTab), _translate("Character", "Equipment"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.skillsMagicTab), _translate("Character", "Skills / Magic"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.personalityTab), _translate("Character", "Personality"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.historyTab), _translate("Character", "History"))
        self.idLabel.setText(_translate("Character", "00000"))

from CharacterVitalStatisticsWidget import CharacterVitalStatisticsWidget
