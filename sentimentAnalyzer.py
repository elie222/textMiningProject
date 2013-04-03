import sys
import csv
import copy
import re
import os
import nltk # http://nltk.org/install.html
from HTMLParser import HTMLParser
from progressbar import ProgressBar

'''
These are the headers in the StocksTwitFiles:
    ['id', 'body', 'user_id', 'user_login', 'message_source', 'message_type', 'avatar_url', 
    'avatar_url_ssl', 'investor_relations', 'private_relations', 'reply_count', 'reply_parent', 'chart', 
    'forex', 'future', 'filtered', 'followers', 'following', 'recommended', 'mention_ids', 'stock_ids', 
    'stock_symbols', 'in_reply_to_message_id', 'in_reply_to_user_id', 'in_reply_to_user_login', 'updated_at', 
    'created_at']
To access the body of a twit you would write twit_data['body']. 
'''

'''
BUGS on this line:
absScore += int(twit_booster_word_index_to_score_map[i - 1])


Maybe we should deal with this. I'm not sure.

A list of twits with bad scores:

TWIT: $INTC is the bomb.
SCORE: -2
Probably leave this one. Bomb could be bad.

TWIT: $DRIV looks like it is breaking down from base.
SCORE: 2
The problem is probably with like. Maybe we should avoid looks like.

TWIT: $WBSN looks like it is headed down for a gap fill.
SCORE: 2
The problem is probably with like. Maybe we should avoid looks like.

TWIT: $CRY was a good one today sorry for not posting it sooner
SCORE: -4
What went wrong here? The word CRY? If so, we should deal with that. Shouldn't
be checking things that start with $ or @.

TWIT: $QQQQ up big on the year. don't fight the tape?
SCORE: -3
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
        
        # Needs to be self.h if you want to put it here.
        # h = HTMLParser()
        

    def analyze(self, twit_data):
        '''
        TODO: Doesn't work ATM.
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
        #print wordList
        
        twit_negating_word_index_set = set([])
        twit_booster_word_index_to_score_map = {}
        twit_emotion_word_index_to_score_map = {}

        # print '===TWIT:', twit

        for i in xrange(len(wordList)):
            if i>0:
                if wordList[i - 1] == '$':
                    continue
            if wordList[i] in self.NegatingWordSet:
                # print 'NEGATING WORD:', wordList[i]
                twit_negating_word_index_set.add(i)
            elif wordList[i] in self.BoosterWordMap:
                # print 'BOOSTER WORD:', wordList[i]
                twit_booster_word_index_to_score_map[i] = self.BoosterWordMap[wordList[i]]
            else:
                for key in self.EmotionLookupTableMap:
                    if key.endswith('*'):
                        if re.match(key[:-1], wordList[i]) is not None:
                            twit_emotion_word_index_to_score_map[i] = self.EmotionLookupTableMap[key]
                            #if not twit_emotion_word_index_to_score_map[i] == 0:
                            #    print wordList[i], twit_emotion_word_index_to_score_map[i]
                    else:
                        if i > 0 and wordList[i].lower()=='like' and (wordList[i-1].lower() in ['look','looks']):
                            continue
                        if key == wordList[i].lower():
                            twit_emotion_word_index_to_score_map[i] = self.EmotionLookupTableMap[key]
                            #if not twit_emotion_word_index_to_score_map[i] == 0:
                            #    print wordList[i], twit_emotion_word_index_to_score_map[i]
        #print twit_booster_word_index_to_score_map
        #print twit_negating_word_index_set
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
            #print absScore   
            emScore = absScore * sign
            ###looking for eomoticons
            #print self.EmoticonLookupTableMap
            for eomoticon in self.EmoticonLookupTableMap:
                if not fixed_twit.find(eomoticon) == -1:
                    emScore += int(self.EmoticonLookupTableMap[eomoticon])
            score += emScore
           
        if not re.search('!!!', fixed_twit ) is None:
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
            
            rowTickers = rowDict['stock_symbols'].split(",")
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

def tagBody(body, score):
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
    
def getAllTickerTwits(ticker, sa):
    twits_array = convert_csv_file_to_array_of_dicts_for_ticker('StockTwitsData100000.csv', ticker)
    with open(ticker + ".csv", 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for twit_data in twits_array:
            score = sa.analyze(twit_data)
            taggedBody = tagBody(twit_data['body'], score)
            writer.writerow([twit_data['created_at'],twit_data['stock_symbols'], taggedBody, score])


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
    sa = SentimentAnalyzer()
    getAllTickerTwits("MU", sa)
    getAllTickerTwits("C", sa)
    getAllTickerTwits("MLNX", sa)
    getAllTickerTwits("GOOG", sa)
    getAllTickerTwits("GS", sa)
    getAllTickerTwits("POT", sa)
    getAllTickerTwits("AAPL", sa)
    getAllTickerTwits("LVS", sa)
    getAllTickerTwits("INTC", sa)
    getAllTickerTwits("MSFT", sa)    
if __name__ == '__main__':
    main()