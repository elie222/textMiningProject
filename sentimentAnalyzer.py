import csv

def analyze(twit):
    taggedTwit = ""

    return taggedTwit

def convertCSVFileToArrayOfDicts(csvFileName):
    arrayOfDicts = []

    with open(csvFileName, 'r') as f:
        reader = csv.reader(f)

        headers = reader.next()

        for row in reader:
            rowDict = dict(zip(headers,row))
            arrayOfDicts.append(rowDict)

    return arrayOfDicts

def main():
    #example twit
    # twitData = '407487,@dustin I&amp;#39;m long $aapl or at least until $goog OS is out next year.,2,genevate,default,normal,http://avatars.stocktwits.com/production/2/thumb-1330556785.png?407487,https://s3.amazonaws.com/st-avatars/production/2/thumb-1330556785.png?407487,false,false,0,false,false,false,false,false,0,0,false,1,"686,2044","AAPL,GOOG",,1,dustin,Fri Jul 10 21:47:36 UTC 2009,Fri Jul 10 21:47:36 UTC 2009'

    csvFileName = 'StockTwits-Data(beginning of file).csv'
    twitsArray = convertCSVFileToArrayOfDicts(csvFileName)

    print twitsArray[10]['body']

if __name__ == '__main__':
    main()