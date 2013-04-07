#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sentimentAnalyzer import SentimentAnalyzer
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class SA(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)

        self.initUI()
        self.connectObjects()

    def initUI(self):
        twitLabel = QLabel('Twit:', self)
        self.twitInput = QTextEdit(self)
        self.twitInput.setMaximumHeight(100)
        tickerLabel = QLabel('Ticker Symbol:', self)
        self.tickerInput = QLineEdit(self)
        
        vboxTwitDataInput = QVBoxLayout()
        vboxTwitDataInput.addWidget(twitLabel)
        vboxTwitDataInput.addWidget(self.twitInput)
        vboxTwitDataInput.addWidget(tickerLabel)
        vboxTwitDataInput.addWidget(self.tickerInput)

        self.getSentimentBtn = QPushButton('Get Sentiment', self)

        hboxTwitInput = QHBoxLayout()
        hboxTwitInput.addLayout(vboxTwitDataInput)
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

        self.setGeometry(100, 100, 600, 200)
        self.setWindowTitle('Stock Twits Sentiment Analyzer')

    def connectObjects(self):
        self.getSentimentBtn.clicked.connect(self.getSentimentClicked)

    def getSentimentClicked(self):
        twitData = {}
        twitData['body'] = str(self.twitInput.toPlainText())

        #it doesn't actually matter what you put in here, since our SA gives every stock the same score anyway.
        twitData['stock_symbols'] = str(self.tickerInput.displayText()).upper()

        # print twitData['body']
        # print twitData['stock_symbols']

        sa = SentimentAnalyzer()
        score = sa.analyze(twitData)
        sentiment = sa.getSentiment(score)
        self.sentimentResultLabel.setText(str(sentiment))
        self.sentimentScoreLabel.setText(str(score))




def main():

    app = QApplication(sys.argv)
    ex = SA()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()