from PyQt5.QtGui import QResizeEvent

from GameController.GameControllerModel import GameControllerModel
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QFormLayout, QMainWindow, \
    QInputDialog, QGridLayout
import os
from GameController.QToolboxActions import QToolboxActions
from GameController.QToolboxRun import QToolboxRun


class GameControllerWindow(QtWidgets.QWidget):

    def __init__(self, model: GameControllerModel):
        super().__init__()
        self.toolbar_w = 70
        self.toolbar_h = 70
        self.model = model
        self.main_layout = QGridLayout()
        self.lblCurrentDungeon = QLabel()
        self.widRun = QToolboxRun(self)
        self.widActions = QToolboxActions(self)
        self.content_wid = QtWidgets.QWidget()
        self.currentChapter = 1
        self.setupUi()
        # self.model.onSourceChanged.connect(self.source_changed)

    def changeCurrentChapter(self, ch_number: int):
        self.lblCurrentDungeon.clear()
        pixmap = QtGui.QPixmap(self.model.getChapterImagePath(ch_number))
        pixmap = pixmap.scaled(self.lblCurrentDungeon.width(), self.lblCurrentDungeon.height(), Qt.KeepAspectRatio)
        self.lblCurrentDungeon.setPixmap(pixmap)
        self.currentChapter = ch_number

    def setupUi(self):
        self.setObjectName("main_window")
        self.resize(800, 600)
        self.setMinimumWidth(640)
        self.setMinimumHeight(480)

        # centralwidget = QtWidgets.QWidget(main_window)
        # centralwidget.setStyleSheet("background-color: #6e6e6e")
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        # self.setVerticalSpacing(10)
        # self.setHorizontalSpacing(0)
        self.main_layout.setColumnStretch(0, 0)
        self.main_layout.setRowStretch(0, 0)
        self.main_layout.setColumnStretch(1, 200)
        self.main_layout.setRowStretch(1, 200)
        self.setLayout(self.main_layout)

        # Init currentDungeonWidget
        self.lblCurrentDungeon.setText("")
        # self.lblCurrentDungeon.setStyleSheet("background-color: white")
        self.lblCurrentDungeon.setAlignment(Qt.AlignCenter)
        self.lblCurrentDungeon.setFixedWidth(self.toolbar_w)
        self.lblCurrentDungeon.setFixedHeight(self.toolbar_h)
        self.changeCurrentChapter(1)
        self.lblCurrentDungeon.mousePressEvent = self.onChapterClick

        self.main_layout.addWidget(self.lblCurrentDungeon, 0, 0)

        self.widRun.setFixedHeight(self.toolbar_h)
        self.main_layout.addWidget(self.widRun, 0, 1)

        self.widActions.setFixedWidth(self.toolbar_w)
        self.main_layout.addWidget(self.widActions, 1, 0)

        self.content_wid.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.content_wid.setStyleSheet("background-color: rgb(43, 43, 43)")
        self.main_layout.addWidget(self.content_wid, 1, 1)

        self.setStyleSheet("background-color: #6e6e6e")

        # self.setCentralWidget(centralwidget)
        # centralwidget.setLayout(self.main_layout)

    def onChapterClick(self, event):
        self.askForChapter()
        pass

    def askForChapter(self):
        chapters = self.model.getChapters()
        item, ok = QInputDialog.getItem(self, "Select chapter",
                                        "Chapter:", chapters, self.currentChapter - 1, False)
        if ok and item:
            selected_ch = self.model.getChNumberFromString(item)
            if selected_ch != -1:
                self.changeCurrentChapter(selected_ch)
