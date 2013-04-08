import sys
import csv
import copy
import re
import os
import nltk # http://nltk.org/install.html
from HTMLParser import HTMLParser
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import datetime as dt



'''
These are the headers in the StocksTwitFiles:
    ['id', 'body', 'user_id', 'user_login', 'message_source', 'message_type', 'avatar_url', 
    'avatar_url_ssl', 'investor_relations', 'private_relations', 'reply_count', 'reply_parent', 'chart', 
    'forex', 'future', 'filtered', 'followers', 'following', 'recommended', 'mention_ids', 'stock_ids', 
    'stock_symbols', 'in_reply_to_message_id', 'in_reply_to_user_id', 'in_reply_to_user_login', 'updated_at', 
    'created_at']
To access the body of a twit you would write twit_data['body']. 
'''

class SentimentAnalyzer:
    def __init__(self):        
        SlangLookupTablePath = os.path.join(os.path.dirname(__file__), 'SentStrength_Data_Sept2011/SlangLookupTable.txt')
        self.SlangLookupTableMap = buildMapFromFile(SlangLookupTablePath,"\t")

        NegatingWordListPath = os.path.join(os.path.dirname(__file__), 'SentStrength_Data_Sept2011/NegatingWordList.txt')
        self.NegatingWordSet = buildSetFromFile(NegatingWordListPath)
        
        EmotionLookupTablePath = os.path.join(os.path.dirname(__file__), 'SentStrength_Data_Sept2011/EmotionLookupTable.txt')
        self.EmotionLookupTableMap = buildMapFromFile(EmotionLookupTablePath,"\t")
        
        EmoticonLookupTablePath = os.path.join(os.path.dirname(__file__), 'SentStrength_Data_Sept2011/EmoticonLookupTable.txt')
        self.EmoticonLookupTableMap = buildMapFromFile(EmoticonLookupTablePath,"\t")
        
        BoosterWordListPath = os.path.join(os.path.dirname(__file__), 'SentStrength_Data_Sept2011/BoosterWordList.txt')
        self.BoosterWordMap = buildMapFromFile(BoosterWordListPath,"\t")


        # some other words:
        self.addMoreEmotionWords()

    def analyze(self, twit_data):
        '''
        Returns the score for the given twit data.
        '''

        h = HTMLParser()

        score = 0
        twit = clean_up_twit(twit_data['body'])
        

        if len(twit_data['stock_symbols']) == 0:
            return score

        fixed_twit = h.unescape(twit)

        # this just splits the sentence into an array (including putting punctuation into its own array cell).
        wordList = nltk.word_tokenize(fixed_twit)

        wordList = self.convertSlangToWords(wordList)
        
        twit_negating_word_index_set = set([])
        twit_booster_word_index_to_score_map = {}
        twit_emotion_word_index_to_score_map = {}

        for i in xrange(len(wordList)):
            if i>0:
                if wordList[i - 1] == '$':
                    continue
            if wordList[i] in self.NegatingWordSet:
                twit_negating_word_index_set.add(i)
            elif wordList[i] in self.BoosterWordMap:
                twit_booster_word_index_to_score_map[i] = self.BoosterWordMap[wordList[i]]
            else:
                for key in self.EmotionLookupTableMap:
                    if key.endswith('*'):
                        if re.match(key[:-1], wordList[i]) is not None:
                            twit_emotion_word_index_to_score_map[i] = self.EmotionLookupTableMap[key]
                    else:
                        if i > 0 and wordList[i].lower()=='like' and (wordList[i-1].lower() in ['look','looks']):
                            continue
                        if key == wordList[i].lower():
                            twit_emotion_word_index_to_score_map[i] = self.EmotionLookupTableMap[key]

        for i in twit_emotion_word_index_to_score_map:
            sign = 0
            emScore = int(twit_emotion_word_index_to_score_map[i])
            absScore = abs(emScore)
            if emScore < 0:
                sign = -1
            else:
                sign = 1
            if i == 1:
                if  (i - 1) in twit_booster_word_index_to_score_map:
                    absScore += int(twit_booster_word_index_to_score_map[i - 1])
                elif (i - 1) in twit_negating_word_index_set:
                    absScore *= -1
            elif i > 1:
                if  (i - 1) in twit_booster_word_index_to_score_map:
                    absScore += int(twit_booster_word_index_to_score_map[i - 1])
                elif (i - 1) in twit_negating_word_index_set:
                    absScore *= -1
                    
                if  (i - 2) in twit_booster_word_index_to_score_map:
                    absScore += int(twit_booster_word_index_to_score_map[i - 2])
                elif (i - 2) in twit_negating_word_index_set:
                    absScore *= -1

            emScore = absScore * sign

            ###looking for emoticons
            for emoticon in self.EmoticonLookupTableMap:
                if not fixed_twit.find(emoticon) == -1:
                    emScore += int(self.EmoticonLookupTableMap[emoticon])
            score += emScore
           
        if not re.search('!!!', fixed_twit) is None:
            sign = 0 
            if score < 0:
                sign = -1
            else:
                sign = 1
            score = sign*(abs(score) + 1)

        return score

    def convertSlangToWords(self, wordList):
        '''
        Returns the twit with the slang replaced as actual words.
        For example, if the twit is 'btw nobody likes Ofir'. This function will return
        'by the way nobody likes Ofir'.
        '''
        convertedWordList = []
        
        for word in wordList:
            isReplaced = False
            for key in self.SlangLookupTableMap:
                if key == word:
                    slangTraslationList = nltk.word_tokenize(self.SlangLookupTableMap[key])
                    for word in slangTraslationList:
                        convertedWordList.append(word)
                    isReplaced = True
                    break

            # word is not an abbreviation
            if not isReplaced:
                convertedWordList.append(word)

        return convertedWordList

    def addMoreEmotionWords(self):
        '''
        Adds some important stock specific words to emotionMap.
        TODO: Not sure about the scoring.
        '''
        self.EmotionLookupTableMap['bear'] = '-5'
        self.EmotionLookupTableMap['bearish'] = '-5'

        self.EmotionLookupTableMap['bull'] = '5'
        self.EmotionLookupTableMap['bullish'] = '5'

        self.EmotionLookupTableMap['long'] = '4'
        self.EmotionLookupTableMap['short'] = '-4'

    def tagBody(self, body, score):
        retStr = ""
        if score > 3:
            retStr = "<very positive>" + body + "</very positive>"
        elif score > 0:
            retStr = "<positive>" + body + "</positive>"
        elif score == 0:
            retStr = "<neutral>" + body + "</neutral>"
        elif score < -3:
            retStr = "<very negative>" + body + "</very negative>"
        elif score < 0:
            retStr = "<negative>" + body + "</negative>"
        return retStr

    def getSentiment(self, score):
        if score > 3:
            return 'Very Positive'
        elif score > 0:
            return 'Positive'
        elif score == 0:
            return 'Neutral'
        elif score < -3:
            return 'Very Negative'
        elif score < 0:
            return 'Negative'

    def converDate(strDate):
        monthsMap = {'Jan': '01', 'Feb': '02', 'Mar': '03','Apr': '04','May': '05','Jun': '06','Jul': '07','Aug': '08','Sep': '09','Oct': '10','Nov': '11','Dec': '12'}
        splitted = strDate.split(' ')
        month= monthsMap[splitted[1]]
        d = splitted[2] + '/' + month + '/' + splitted[5]
        return dt.datetime.strptime(d,'%d/%m/%Y').date()
        
    def drawByCoordinates(self, x, posY, negY): 
        
        mpl.rcParams['axes.color_cycle'] = ['r', 'b']

        #dates = ['01/02/1991','01/03/1991','01/04/1991','01/05/1991','03/05/1991','04/06/1991','06/06/1991','17/06/1991','22/06/1991']
        #x = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in dates]

        #posY = [3,7,90,3,55,78,99,3,25]
        #negY = [2,6,77,8,98,12,32,5,17]

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plot = plt.plot(x,negY,x,posY)
        plt.xlabel('dates')
        plt.ylabel('sentiment')
        plt.show(plot)

    def drawGraph(self, ticker, startDate, endDate):
        convStartDate = dt.datetime.strptime(startDate,'%d/%m/%Y').date()
        convEndDate = dt.datetime.strptime(endDate,'%d/%m/%Y').date()
        ticker = ticker.upper()
        twits_array = convert_csv_file_to_array_of_dicts(ticker +'.csv')
        date_score = {}
        for twit_data in twits_array:
            twitDate = converDate(twit_data['date'])
            if twitDate > convStartDate and twitDate < convEndDate:
                if not twitDate in date_score:
                    date_score[twitDate] = [0,0]
                if int(twit_data['score']) > 0:
                    date_score[twitDate][0] += int(twit_data['score'])
                else:
                    date_score[twitDate][1] -= int(twit_data['score'])
        keylist = date_score.keys()
        keylist.sort()       
        x = [i for i in keylist]
        posY = [date_score[i][0] for i in keylist]
        negY = [date_score[i][1] for i in keylist]
        #print date_score
        print x
        print posY
        print negY
        drawByCoordinates(x, posY, negY)

    
def convert_csv_file_to_array_of_dicts(csv_filename, headers='first row'):
    '''
    Returns an array of dictionaries where each dictionary represents a row of the csv file.
    The keys of each dictionary are the headers. The values are the cells of the row.

    Example: if you want to access the stock_ids of the fifth twit in the list, you would do:
    array_of_dicts[4]['stock_ids'].

    headers - the names of the keys of the dictionary. If headers is set to 'first row',
    then the first row of the csv file will be the keys in the dictionary.
    '''
    array_of_dicts = []

    with open(csv_filename, 'r') as f:
        reader = csv.reader(f)

        if headers == 'first row':
            headers = reader.next()

        for row in reader:
            #creates a dict with headers as keys and row as values
            rowDict = dict(zip(headers,row))
            array_of_dicts.append(rowDict)

    return array_of_dicts

def convert_csv_file_to_array_of_dicts_for_ticker(csv_filename, ticker, headers='first row'):
    '''
    Returns an array of dictionaries where each dictionary represents a row of the csv file.
    The keys of each dictionary are the headers. The values are the cells of the row.

    Example: if you want to access the stock_ids of the fifth twit in the list, you would do:
    array_of_dicts[4]['stock_ids'].

    headers - the names of the keys of the dictionary. If headers is set to 'first row',
    then the first row of the csv file will be the keys in the dictionary.
    '''
    array_of_dicts = []

    with open(csv_filename, 'r') as f:
        reader = csv.reader(f)

        if headers == 'first row':
            headers = reader.next()

        for row in reader:
            #creates a dict with headers as keys and row as values
            rowDict = dict(zip(headers,row))
            try:
                rowTickers = rowDict['stock_symbols'].split(",")
            except:
                print 'IGNORING EXCEPTION'
                pass
                # print rowDict
                # sys.exit()
            if ticker in rowTickers:
                array_of_dicts.append(rowDict)

    return array_of_dicts
    
def buildMapFromFile (fname, sep):
    '''
    The file is of the form:
    key1 sep value1
    key2 sep value2
    etc.

    Returns {'key1': 'value1', 'key2': 'value2', ...} 
    '''
    retMap = {}
    with open(fname) as f:
        content = f.readlines()
        for row in content:
            splitRows = row.split(sep)
            splitRows[1] = splitRows[1].replace('\n','')
            splitRows[1] = splitRows[1].replace('\xa0','') 
            retMap[splitRows[0]] = splitRows[1]

    return retMap
    
def buildSetFromFile (fname):
    '''
    The file is of the form:
    value1
    value2
    etc.

    Returns ('value1', value2', ...) 
    '''
    retSet = set([])
    with open(fname) as f:
        content = f.readlines()
        for row in content:
            fixedRow = row.replace('\n','')
            fixedRow = fixedRow.replace('\xa0','')
            retSet.add(fixedRow)
     
    return retSet

def clean_up_twit(twit):
    '''
    Returns a twit with charachters converted to normal charachters. eg. &amp; -> &
    Maybe HTMLParser is supposed to do this, but it doesn't handle everything.
    '''
    twit = twit.replace('&amp;#39;', '\'')
    twit = twit.replace('&#39;', '\'')
    twit = twit.replace('&amp;', '&')
    twit = twit.replace('&quot;', '\"')
    twit = twit.replace('&lt;', '<')
    twit = twit.replace('&gt;', '>')

    return twit

def getAllTickerTwits(self, filename, ticker, sa):
    twits_array = convert_csv_file_to_array_of_dicts_for_ticker(filename, ticker)
    print len(twits_array)
    with open(ticker + ".csv", 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        # i = 0
        for twit_data in twits_array:
            # if i == 300:
            #     break
            # i += 1
            score = sa.analyze(twit_data)
            taggedBody = tagBody(twit_data['body'], score)
            writer.writerow([twit_data['created_at'],twit_data['stock_symbols'], taggedBody, score])

    print 'FINISHED:', ticker


    
def main():
    """
    from time import time
    startTime = time()

    # twits_array = convert_csv_file_to_array_of_dicts('StockTwits-Data(beginning of file).csv')
    twits_array = convert_csv_file_to_array_of_dicts('check.csv')

    sa = SentimentAnalyzer()

    #print 'PRINTING THE SCORES OF TWITS WITH SCORE != 0'

    # pbar is just to give a visual indication of the progress made so far.
    # pbar = ProgressBar(maxval=len(twits_array)).start()
    # i = 0

    for twit_data in twits_array:
        score = sa.analyze(twit_data)

        #if not score == 0:
        print 'TWIT:', twit_data['body']
        print 'SCORE:', score

        # pbar.update(i)
        # i += 1

    # pbar.finish()

    endTime = time()
    timeTaken = endTime - startTime

    print 'Total time taken:', timeTaken
    """
    """
    sa = SentimentAnalyzer()

    # filename = 'StockTwitsDataMLNX268.csv'
    # getAllTickerTwits(filename, "MLNX", sa)

    filename = 'StockTwitsDataMU1000.csv'
    getAllTickerTwits(filename, "MU", sa)
    
    # getAllTickerTwits("C", sa)
    
    # getAllTickerTwits("GOOG", sa)
    # getAllTickerTwits("GS", sa)
    # getAllTickerTwits("POT", sa)
    # getAllTickerTwits("AAPL", sa)
    # getAllTickerTwits("LVS", sa)
    # getAllTickerTwits("INTC", sa)
    # getAllTickerTwits("MSFT", sa) 
    """
    sa = SentimentAnalyzer()
    sa.drawGraph('GOOG', '10/09/2009', '05/11/2009')
"""
if __name__ == '__main__':
    main()
"""