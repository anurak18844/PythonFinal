import pymongo

def init_mongo():
    myclient = pymongo.MongoClient(
        'mongodb+srv://root:0823632737@bcit-anurak.7belh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = myclient["myfirstpythonmongo"]
    collection = db['twitter2']
    return collection

def agg_tweets():
    collection = init_mongo()
    agg = collection.aggregate([
        { '$unwind': "$predict_value" },
        {
            '$group':{
                "_id":{
                    "topic": "$predict_value.topic.id",
                    "sentiment": "$predict_value.sentiment"
                },
                "tweet_count": {
                    '$sum' : 1
                }
            }
        },
        {
            '$sort':{
                "_id.topic": 1,
                "_id.sentiment": 1
            }
        }
    ])
    return agg

def agg_tweets_by_topic():
    collection = init_mongo()
    agg = collection.aggregate([
        { '$unwind': "$predict_value" },
        {
            '$group':{
                "_id":{
                    "topic_id": "$predict_value.topic.id",
                    "name": "$predict_value.topic.name"
                },
                "tweet_count": {
                    '$sum' : 1
                }
            }
        },
        {
            '$sort':{
                "_id": 1
            }
        }
    ])
    return agg
    

