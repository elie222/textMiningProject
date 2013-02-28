def analyze(twit):
    taggedTwit = ""

    return taggedTwit

"""
data is in the form:
id,body,user_id,user_login,message_source,message_type,avatar_url,avatar_url_ssl,investor_relations,private_relations,reply_count,reply_parent,chart,forex,future,filtered,followers,following,recommended,mention_ids,stock_ids,stock_symbols,in_reply_to_message_id,in_reply_to_user_id,in_reply_to_user_login,updated_at,created_at
"""
def parseTwitData(twitData):

    data = []
    parsedTwit = {}

    toAppend = ''
    remainingTwitData = twitData

    while not len(remainingTwitData) == 0:
        p = remainingTwitData.partition(',')
        toAppend = p[0]
        remainingTwitData = p[2]
        if not toAppend.startswith('"'):
            data.append(toAppend)
        else:
            while not toAppend.endswith('"'):
                print toAppend
                p = remainingTwitData.partition(',')
                toAppend += (',' + p[0])
                remainingTwitData = p[2]

            data.append(toAppend)
        
    parsedTwit['id'] = data[0]
    parsedTwit['body'] = data[1]
    parsedTwit['user_id'] = data[2]
    parsedTwit['user_login'] = data[3]
    parsedTwit['message_source'] = data[4]
    parsedTwit['message_type'] = data[5]
    parsedTwit['avatar_url'] = data[6]
    parsedTwit['avatar_url_ssl'] = data[7]
    parsedTwit['investor_relations'] = data[8]
    parsedTwit['private_relations'] = data[9]
    parsedTwit['reply_count'] = data[10]
    parsedTwit['reply_parent'] = data[11]
    parsedTwit['chart'] = data[12]
    parsedTwit['forex'] = data[13]
    parsedTwit['future'] = data[14]
    parsedTwit['filtered'] = data[15]
    parsedTwit['followers'] = data[16]
    parsedTwit['following'] = data[17]
    parsedTwit['recommended'] = data[18]
    parsedTwit['mention_ids'] = data[19]
    parsedTwit['stock_ids'] = data[20]#be careful here
    parsedTwit['stock_symbols'] = data[21]#be careful here
    parsedTwit['in_reply_to_message_id'] = data[22]
    parsedTwit['in_reply_to_user_id'] = data[23]
    parsedTwit['in_reply_to_user_login'] = data[24]
    parsedTwit['updated_at'] = data[25]
    parsedTwit['created_at'] = data[26]

    return parsedTwit


twitData = '407487,@dustin I&amp;#39;m long $aapl or at least until $goog OS is out next year.,2,genevate,default,normal,http://avatars.stocktwits.com/production/2/thumb-1330556785.png?407487,https://s3.amazonaws.com/st-avatars/production/2/thumb-1330556785.png?407487,false,false,0,false,false,false,false,false,0,0,false,1,"686,2044","AAPL,GOOG",,1,dustin,Fri Jul 10 21:47:36 UTC 2009,Fri Jul 10 21:47:36 UTC 2009'

pt = parseTwitData(twitData)

for x in pt:
    print x, ':', pt[x]
