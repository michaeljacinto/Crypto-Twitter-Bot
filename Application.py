from PyQt5.QtWidgets import (QSpinBox, QWidget, QTabWidget, QSpinBox, QLineEdit, QLabel, QRadioButton, QStackedWidget,
                             QVBoxLayout, QMainWindow, QApplication, QPushButton, QDialog, QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout)
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QRect
from PyQt5 import QtCore
import market_price_bot as mpb


class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.title = "Market Price Bot"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 100
        self.iconName = "icon.png"

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
        self.coinsEdit = QLineEdit()
        self.coinsEdit.setToolTip("Enter coins here. E.g: BTC ETH LTC")
        self.coinsEdit.setFont(QtGui.QFont("Sanserif", 10))
        vbox.addWidget(self.coinsEdit)

        coinsLabelMinutes = QLabel("Minutes: ")
        coinsLabelMinutes.setFont(QtGui.QFont("Sanserif", 10))
        vbox.addWidget(coinsLabelMinutes)
        self.spinBox = QSpinBox()
        vbox.addWidget(self.spinBox)
        self.setLayout(vbox)

        twitterButton = QPushButton("Twitter", self)
        twitterButton.setIcon(QtGui.QIcon("twitter.png"))
        twitterButton.setIconSize(QtCore.QSize(40, 40))
        twitterButton.clicked.connect(self.ClickCryptoTweet)
        twitterButton.setMinimumHeight(40)
        vbox.addWidget(twitterButton)

        textButton = QPushButton("Text", self)
        textButton.setIcon(QtGui.QIcon("text-message.png"))
        textButton.setIconSize(QtCore.QSize(40, 40))
        textButton.clicked.connect(self.ClickCryptoText)
        textButton.setMinimumHeight(40)
        vbox.addWidget(textButton)

    def ClickCryptoTweet(self):
        coin_args = self.coinsEdit.text()
        mins_args = self.spinBox.value()
        message = mpb.get_crypto_data(coin_args)
        mpb.tweet_data(message)

    def ClickCryptoText(self):
        coin_args = self.coinsEdit.text()
        mins_args = self.spinBox.value()
        message = mpb.get_crypto_data(coin_args)
        mpb.text_data(message)


class TabStocks(QWidget):
    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout()

        stockLabel = QLabel("Stock: ")
        stockLabel.setFont(QtGui.QFont("Sanserif", 10))
        vbox.addWidget(stockLabel)
        self.stockEdit = QLineEdit()
        self.stockEdit.setToolTip(
            "Only one stock ticker is supported. E.g: AAPL")
        self.stockEdit.setFont(QtGui.QFont("Sanserif", 10))
        vbox.addWidget(self.stockEdit)

        stockLabelMinutes = QLabel("Minutes: ")
        stockLabelMinutes.setFont(QtGui.QFont("Sanserif", 10))
        vbox.addWidget(stockLabelMinutes)
        self.spinBox = QSpinBox()
        vbox.addWidget(self.spinBox)
        self.setLayout(vbox)

        self.twitterButton = QPushButton("Twitter", self)
        self.twitterButton.setIcon(QtGui.QIcon("twitter.png"))
        self.twitterButton.setIconSize(QtCore.QSize(40, 40))
        self.twitterButton.clicked.connect(self.ClickStockTweet)
        self.twitterButton.setMinimumHeight(40)
        vbox.addWidget(self.twitterButton)

        textButton = QPushButton("Text", self)
        textButton.setIcon(QtGui.QIcon("text-message.png"))
        textButton.setIconSize(QtCore.QSize(40, 40))
        textButton.clicked.connect(self.ClickStockText)
        textButton.setMinimumHeight(40)
        vbox.addWidget(textButton)

    def ClickStockTweet(self):
        stock_args = self.stockEdit.text()
        mins_args = self.spinBox.value()
        message = mpb.get_stock_data(stock_args)
        self.twitterButton.setText("Hi")
        mpb.tweet_data(message)

    def ClickStockText(self):
        stock_args = self.stockEdit.text()
        mins_args = self.spinBox.value()
        message = mpb.get_stock_data(stock_args)
        mpb.text_data(message)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())
