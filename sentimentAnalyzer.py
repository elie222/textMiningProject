import csv

def analyze(twit):
    taggedTwit = ""

    return taggedTwit

def convertCSVFileToArrayOfDicts(csvFileName, headers='first row'):
    arrayOfDicts = []

    with open(csvFileName, 'r') as f:
        reader = csv.reader(f)

        if headers == 'first row':
            headers = reader.next()

        for row in reader:
            #creates a dict with headers as keys and row as values
            rowDict = dict(zip(headers,row))
            arrayOfDicts.append(rowDict)

    return arrayOfDicts

def main():
    #example twit
    # twitData = '407487,@dustin I&amp;#39;m long $aapl or at least until $goog OS is out next year.,2,genevate,default,normal,http://avatars.stocktwits.com/production/2/thumb-1330556785.png?407487,https://s3.amazonaws.com/st-avatars/production/2/thumb-1330556785.png?407487,false,false,0,false,false,false,false,false,0,0,false,1,"686,2044","AAPL,GOOG",,1,dustin,Fri Jul 10 21:47:36 UTC 2009,Fri Jul 10 21:47:36 UTC 2009'


    twitsArray = convertCSVFileToArrayOfDicts('StockTwits-Data(beginning of file).csv')

    headers = ['sentence','n','score','keyword']#i don't know what n is
    posSentimentArray = convertCSVFileToArrayOfDicts('wschemaPositive.xml.csv', headers)
    negSentimentArray = convertCSVFileToArrayOfDicts('wschemaNegative.xml.csv', headers)

    print twitsArray[0]
    print posSentimentArray[0]
    print negSentimentArray[0]

if __name__ == '__main__':
    main()