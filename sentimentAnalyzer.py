import csv
import copy
import re
from progressbar import ProgressBar

class SentimentAnalyzer:
    def __init__(self, pos_sentiment_array, neg_sentiment_array):
        self.pos_sentiment_array = pos_sentiment_array
        self.neg_sentiment_array = neg_sentiment_array

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
    twits_array = convert_csv_file_to_array_of_dicts('StockTwits-Data(beginning of file).csv')
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


if __name__ == '__main__':
    main()