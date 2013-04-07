#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class SA(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)

        self.initUI()

    def initUI(self):
        twitLabel = QLabel('Twit:', self)
        twitInput = QTextEdit(self)
        self.getSentimentBtn = QPushButton('Get Sentiment', self)

        hboxTwitInput = QHBoxLayout()
        hboxTwitInput.addWidget(twitLabel)
        hboxTwitInput.addWidget(twitInput)
        hboxTwitInput.addWidget(self.getSentimentBtn)


        sentimentResultTitleLabel = QLabel('Sentiment:', self)
        self.sentimentResultLabel = QLabel('', self)

        sentimentScoreTitleLabel = QLabel('Score:', self)
        self.sentimentScoreLabel = QLabel('', self)

        hboxSentimentResult = QHBoxLayout()
        hboxSentimentResult.addWidget(sentimentResultTitleLabel)
        hboxSentimentResult.addWidget(self.sentimentResultLabel)
        hboxSentimentResult.addWidget(sentimentScoreTitleLabel)
        hboxSentimentResult.addWidget(self.sentimentScoreLabel)

        vbox = QVBoxLayout()
        vbox.addLayout(hboxTwitInput)
        vbox.addLayout(hboxSentimentResult)


        mainWidget = QWidget()
        mainWidget.setLayout(vbox)

        self.setCentralWidget(mainWidget)

        self.setGeometry(100, 100, 700, 400)
        self.setWindowTitle('Stock Twits Sentiment Analyzer')





def main():

    app = QApplication(sys.argv)
    ex = SA()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()