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
        # single twit tab
        twitLabel = QLabel('Tweet:', self)
        self.twitInput = QTextEdit(self)
        self.twitInput.setMaximumHeight(100)
        tickerLabel = QLabel('Ticker Symbol:', self)
        self.tickerInput = QLineEdit(self)
        self.getSentimentBtn = QPushButton('Get Sentiment', self)
        
        vboxTwitDataInput = QVBoxLayout()
        vboxTwitDataInput.addWidget(twitLabel)
        vboxTwitDataInput.addWidget(self.twitInput)
        vboxTwitDataInput.addWidget(tickerLabel)
        vboxTwitDataInput.addWidget(self.tickerInput)
        vboxTwitDataInput.addWidget(self.getSentimentBtn)

        # hboxTwitInput = QHBoxLayout()
        # hboxTwitInput.addLayout(vboxTwitDataInput)
        # hboxTwitInput.addWidget(self.getSentimentBtn)


        sentimentResultTitleLabel = QLabel('Sentiment:', self)
        self.sentimentResultLabel = QLabel('', self)

        sentimentScoreTitleLabel = QLabel('Score:', self)
        self.sentimentScoreLabel = QLabel('', self)

        hboxSentimentResult = QHBoxLayout()
        hboxSentimentResult.addWidget(sentimentResultTitleLabel)
        hboxSentimentResult.addWidget(self.sentimentResultLabel)
        hboxSentimentResult.addWidget(sentimentScoreTitleLabel)
        hboxSentimentResult.addWidget(self.sentimentScoreLabel)

        vboxSingleTwit = QVBoxLayout()
        vboxSingleTwit.addLayout(vboxTwitDataInput)
        vboxSingleTwit.addLayout(hboxSentimentResult)



        # graph tab

        tickerLabel = QLabel('Ticker:', self)
        self.tickerGraphInput = QLineEdit(self)
        startDateLabel = QLabel('Start Date (DD/MM/YYYY):', self)
        self.startDateGraphInput = QLineEdit(self)
        endDateLabel = QLabel('End Date (DD/MM/YYYY):', self)
        self.endDateGraphInput = QLineEdit(self)

        # hboxTickerAndDate = QHBoxLayout()
        # hboxTickerAndDate.addWidget(tickerLabel)
        # hboxTickerAndDate.addWidget(self.tickerGraphInput)
        # hboxTickerAndDate.addWidget(startDateLabel)
        # hboxTickerAndDate.addWidget(self.startDateGraphInput)
        # hboxTickerAndDate.addWidget(endDateLabel)
        # hboxTickerAndDate.addWidget(self.endDateGraphInput)

        self.getGraphBtn = QPushButton('Get Sentiment Graph', self)

        # hboxBtn = QHBoxLayout()
        # hboxBtn.addWidget(self.getGraphBtn)

        vboxGraph = QVBoxLayout()
        vboxGraph.addWidget(tickerLabel)
        vboxGraph.addWidget(self.tickerGraphInput)
        vboxGraph.addWidget(startDateLabel)
        vboxGraph.addWidget(self.startDateGraphInput)
        vboxGraph.addWidget(endDateLabel)
        vboxGraph.addWidget(self.endDateGraphInput)
        vboxGraph.addWidget(self.getGraphBtn)

        # vboxGraph.addLayout(hboxTickerAndDate)
        # vboxGraph.addLayout(hboxBtn)


        # main window
        tabWidget = QTabWidget()

        singleTwitWidget = QWidget()
        graphWidget = QWidget()

        singleTwitWidget.setLayout(vboxSingleTwit)
        graphWidget.setLayout(vboxGraph)

        tabWidget.addTab(singleTwitWidget, 'Single Twit')
        tabWidget.addTab(graphWidget, 'Graph')

        # mainWidget = QWidget()
        # mainWidget.setLayout(vbox)

        self.setCentralWidget(tabWidget)

        self.setGeometry(100, 100, 600, 200)
        self.setWindowTitle('Stock Twits Sentiment Analyzer')

    def connectObjects(self):
        self.getSentimentBtn.clicked.connect(self.getSentimentClicked)
        self.getGraphBtn.clicked.connect(self.getGraphClicked)

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

    def getGraphClicked(self):
        ticker = str(self.tickerGraphInput.displayText())
        startDate = str(self.startDateGraphInput.displayText())
        endDate = str(self.endDateGraphInput.displayText())

        print 'TODO'
        print ticker
        print startDate
        print endDate




def main():

    app = QApplication(sys.argv)
    ex = SA()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()