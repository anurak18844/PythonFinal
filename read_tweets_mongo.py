from re import L
import pymongo
import pandas as pd
import numpy as np

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
                    "name": "$predict_value.topic.name",
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

def agg_unit_tweets():
    collection = init_mongo()
    agg = collection.aggregate([
        {
            '$project': {
                "hashTagName": 1,
                "createdAt": 1,
                "tweet_counts": {'$size': "$predict_value"}
            }
        }
    ])
    return agg

def agg_by_sentiment():
    new_agg=[]
    agg = agg_tweets()
    # เรียงค่าทุกฟิลด์ใหม่ให้อยู่ใน level เดียวกัน
    for a in agg:
        new_ent = { 
            "id": a["_id"]['topic'], 
            "topic": a["_id"]['name'], 
            "sentiment": a["_id"]['sentiment'], 
            "tweet_count": a['tweet_count']
        }
        new_agg.append(new_ent)
    df = pd.DataFrame(new_agg)
    # เก็บค่า topic name 
    topic_names=df['topic'].unique()

    # สร้าง pivot table ให้แจงค่าตามประเภท sentiment และแสดงตามแถว id, topic
    table = pd.pivot_table(df, 'tweet_count', index=['id','topic'], columns=['sentiment'], aggfunc=np.sum)
    # ใส่ค่า 0 ให้กับเซลล์ที่เป็น NaN
    table = table.fillna(0)

    # ดึงข้อมูลมาจัด output ใหม่
    new_dict = table.to_dict('records')
    new_result=[]
    for idx,n in enumerate(new_dict):
        b = { "id": idx, "topic": topic_names[idx], "sentiment": list(n.values()) }
        new_result.append(b)
    return new_result

def get_tweets_texts(topic_id, sentiment):
    collection = init_mongo()
    return collection.aggregate([
        { 
        '$unwind': "$predict_value"
        },
        {
            '$match': {
                "predict_value.topic.id" : topic_id,
                "predict_value.sentiment": sentiment
            }
        },
        {
            '$limit': 5
        }
    ]);
