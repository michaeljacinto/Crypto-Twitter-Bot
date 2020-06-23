from PyQt5.QtWidgets import (QSpinBox, QWidget, QTabWidget, QSpinBox, QLineEdit, QLabel, QRadioButton, QStackedWidget,
                             QVBoxLayout, QMainWindow, QApplication, QPushButton, QDialog, QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout)
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QRect
from PyQt5 import QtCore


class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.title = "Market Price Bot"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 100
        self.iconName = "icon.png"
        # self.InitWindow()

    # def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        vbox = QVBoxLayout()
        tabWidget = QTabWidget()

        tabWidget.addTab(TabCrypto(), "Crypto Details")
        tabWidget.addTab(TabStocks(), "Stock Details")
        vbox.addWidget(tabWidget)
        self.setLayout(vbox)


class TabCrypto(QWidget):
    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout()

        coinsLabel = QLabel("Coins: ")
        coinsLabel.setFont(QtGui.QFont("Sanserif", 10))
        vbox.addWidget(coinsLabel)
        coinsEdit = QLineEdit()
        coinsEdit.setToolTip("Enter coins here. E.g: BTC ETH LTC")
        coinsEdit.setFont(QtGui.QFont("Sanserif", 10))
        vbox.addWidget(coinsEdit)

        coinsLabelMinutes = QLabel("Minutes: ")
        coinsLabelMinutes.setFont(QtGui.QFont("Sanserif", 10))
        vbox.addWidget(coinsLabelMinutes)
        spinBox = QSpinBox()
        vbox.addWidget(spinBox)
        self.setLayout(vbox)

        button_1 = QPushButton("Twitter", self)
        # size of button
        # button_1.setGeometry(QRect(100, 100, 80, 25))
        button_1.setIcon(QtGui.QIcon("twitter.png"))
        button_1.setIconSize(QtCore.QSize(40, 40))
        # button_1.clicked.connect(self.ClickMe)
        button_1.setMinimumHeight(40)
        vbox.addWidget(button_1)

        button_2 = QPushButton("Text", self)
        # button_2.setGeometry(QRect(50, 100, 80, 25))
        button_2.setIcon(QtGui.QIcon("text-message.png"))
        button_2.setIconSize(QtCore.QSize(40, 40))
        # button_2.clicked.connect(self.ClickMe)
        button_2.setMinimumHeight(40)
        vbox.addWidget(button_2)


class TabStocks(QWidget):
    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout()

        stockLabel = QLabel("Stock: ")
        stockLabel.setFont(QtGui.QFont("Sanserif", 10))
        vbox.addWidget(stockLabel)
        stockEdit = QLineEdit()
        stockEdit.setToolTip("Only one stock ticker is supported. E.g: AAPL")
        stockEdit.setFont(QtGui.QFont("Sanserif", 10))
        vbox.addWidget(stockEdit)

        stockLabelMinutes = QLabel("Minutes: ")
        stockLabelMinutes.setFont(QtGui.QFont("Sanserif", 10))
        vbox.addWidget(stockLabelMinutes)
        spinBox = QSpinBox()
        vbox.addWidget(spinBox)
        self.setLayout(vbox)

        button_1 = QPushButton("Twitter", self)
        # size of button
        # button_1.setGeometry(QRect(100, 100, 80, 25))
        button_1.setIcon(QtGui.QIcon("twitter.png"))
        button_1.setIconSize(QtCore.QSize(40, 40))
        # button_1.clicked.connect(self.ClickMe)
        button_1.setMinimumHeight(40)
        vbox.addWidget(button_1)

        button_2 = QPushButton("Text", self)
        # button_2.setGeometry(QRect(50, 100, 80, 25))
        button_2.setIcon(QtGui.QIcon("text-message.png"))
        button_2.setIconSize(QtCore.QSize(40, 40))
        # button_2.clicked.connect(self.ClickMe)
        button_2.setMinimumHeight(40)
        vbox.addWidget(button_2)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())
