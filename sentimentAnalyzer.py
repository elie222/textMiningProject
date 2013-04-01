import sys
import csv
import copy
import re
import os
from HTMLParser import HTMLParser
from progressbar import ProgressBar

class SentimentAnalyzer:
    def __init__(self):
        """
        self.pos_sentiment_array = pos_sentiment_array
        self.neg_sentiment_array = neg_sentiment_array
        """
        
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
        h = HTMLParser()
        
    """
    def analyze(self, twit_data):
        pos_score = 0
        neg_score = 0
        tagged_twit = twit_data['body']

        if len(twit_data['stock_symbols']) == 0:
            return pos_score, tagged_twit

        for row in self.pos_sentiment_array:
            result = re.search(row['sentence'], tagged_twit, re.X)

            if result is not None:
                pos_score += row['score']
                # print 'POS'
                # print tagged_twit
                # print row['score']
                # print row['sentence']

        for row in self.neg_sentiment_array:
            result = re.search(row['sentence'], tagged_twit, re.X)

            if result is not None:
                neg_score += row['score']
                # print 'NEG'
                # print tagged_twit
                # print row['score']
                # print row['sentence']

        return pos_score - neg_score, tagged_twit
    """
    def analyze(self, twit_data):
        score = 0
        tagged_twit = twit_data['body']
        fixed_twit = h.unescape(twit_data['body'])
        for key in self.SlangLookupTableMap:
            fixed_twit.replace(key,self.SlangLookupTableMap[key])
        wordList = nltk.word_tokenize(fixed_twit)
        
        
        twit_negating_word_index_set = set([])
        twit_booster_word_index_to_score_map = {}
        twit_emotion_word_index_to_score_map = {}
        for i in xrange(__len__(wordList)):
            if wordList[i] in self.NegatingWordSet:
                twit_negating_word_index_set.add(i)
            elif wordList[i] in self.BoosterWordMap:
                twit_booster_word_index_to_score_map[i] = self.BoosterWordMap[key]
            elif wordList[i] in self.EmoticonLookupTableMap:
                score += int(self.EmoticonLookupTableMap[i])
            else:
                for key in self.EmotionLookupTableMap:
                    if not re.match(key, wordList[i]) is None:
                        twit_emotion_word_index_to_score_map[i] = self.EmotionLookupTableMap[key]
        
        for emotionalWordIndex in twit_emotion_word_index_to_score_map:
            siman = 0
            emScore = int(twit_emotion_word_index_to_score_map[emotionalWordIndex])
            absScore = abs(emScore)
            if emScore < 0:
                siman = -1
            else:
                siman = 1
            if i == 1:
                if  (i - 1) in twit_booster_word_index_to_score_map:
                    absScore += twit_booster_word_index_to_score_map[i - 1]
                elif (i - 1) in twit_negating_word_index_set:
                    absScore *= -1
            elif i > 1:
                if  (i - 1) in twit_booster_word_index_to_score_map:
                    absScore += twit_booster_word_index_to_score_map[i - 1]
                elif (i - 1) in twit_negating_word_index_set:
                    absScore *= -1
                    
                if  (i - 2) in twit_booster_word_index_to_score_map:
                    absScore += twit_booster_word_index_to_score_map[i - 1]
                elif (i - 2) in twit_negating_word_index_set:
                    absScore *= -1
                
            emScore = absScore * siman
            
            score += emScore
            
        if not re.match('!!!', fixed_twit ) is None:
            siman = 0 
            if score < 0:
                siman = -1
            else:
                siman = 1
            score = siman*(abs(score) + 1)
        return score
    
    
def convert_csv_file_to_array_of_dicts(csv_filename, headers='first row'):
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

def buildMapFromFile (fname, sep):
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
    retSet = set([])
    with open(fname) as f:
        content = f.readlines()
        for row in content:
            fixedRow = row.replace('\n','')
            fixedRow = fixedRow.replace('\xa0','')
            retSet.add(fixedRow)           
    return retSet
    
def clean_up_sentiment_array(array):
    clean_array = []

    for row in array:
        clean_sentence = clean_up_sentence(row['sentence'])
        # clean_row = copy.deepcopy(row)
        clean_row = {}
        clean_row['sentence'] = clean_sentence
        clean_row['score'] = float(row['score'])
        clean_array.append(clean_row)

    return clean_array

def clean_up_sentence(sentence):
    clean_sentence = sentence
    clean_sentence = clean_sentence.replace('0','\d+')
    clean_sentence = clean_sentence.replace('& ','')
    clean_sentence = clean_sentence.replace('&amp ', '')
    clean_sentence = clean_sentence.replace('\"', '')

    return clean_sentence

def clean_up_twits_array(twits_array):
    '''
    In an attempt to speed things up, this function removes most of the stuff from the array
    that we don't need. If we need more stuff from it, we can always add it at a later date.
    '''

    clean_array = []

    for twit_data in twits_array:
        clean_row = {}
        clean_row['body'] = twit_data['body']
        clean_row['stock_symbols'] = twit_data['stock_symbols']
        clean_array.append(clean_row)

    return clean_array

def main():
    # twits_array = convert_csv_file_to_array_of_dicts('StockTwits-Data(beginning of file).csv')
    """
    twits_array = convert_csv_file_to_array_of_dicts('StockTwitsData1000.csv')
    # headers = ['id', 'body', 'user_id', 'user_login', 'message_source', 'message_type', 'avatar_url', 
    # 'avatar_url_ssl', 'investor_relations', 'private_relations', 'reply_count', 'reply_parent', 'chart', 
    # 'forex', 'future', 'filtered', 'followers', 'following', 'recommended', 'mention_ids', 'stock_ids', 
    # 'stock_symbols', 'in_reply_to_message_id', 'in_reply_to_user_id', 'in_reply_to_user_login', 'updated_at', 
    # 'created_at']
    # twits_array = convert_csv_file_to_array_of_dicts('some twits.csv', headers)
    twits_array = clean_up_twits_array(twits_array)

    #i don't know what n is. i removed n and keyword anyway to try speed things up, but it didn't help
    headers = ['sentence','n','score','keyword']
    pos_sentiment_array = convert_csv_file_to_array_of_dicts('wschemaPositive.xml.csv', headers)
    neg_sentiment_array = convert_csv_file_to_array_of_dicts('wschemaNegative.xml.csv', headers)

    pos_sentiment_array = clean_up_sentiment_array(pos_sentiment_array)
    neg_sentiment_array = clean_up_sentiment_array(neg_sentiment_array)

    sa = SentimentAnalyzer(pos_sentiment_array, neg_sentiment_array)

    pbar = ProgressBar(maxval=len(twits_array)).start()
    i = 0

    for twit_data in twits_array:
        score, tagged_twit = sa.analyze(twit_data)

        if not score == 0:
            print 'TAGGED TWIT:', tagged_twit
            print 'SCORE:', score

        pbar.update(i)
        i += 1

    pbar.finish()
    """
    sa = SentimentAnalyzer()


if __name__ == '__main__':
    main()