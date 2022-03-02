from flask import Flask, request, jsonify, render_template
import pickle
from model import *
from sentiment import *
from tweetapi import *
from datetime import datetime
import pymongo
from read_tweets_mongo import *

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

def predict_tweet(tag="MyDearNVC"):
    tweets = get_tweets(tag)
    pred = predict_text(tweets)
    return pred

def predict_text(texts):
    my_bow = create_mybow(texts)
    prediction = model.predict(my_bow)
    output = [int(p) for p in prediction]
    pred = []
    sentiments = [get_sentiment(text) for text in texts]
    print(sentiments)
    for t, id, s in zip(texts, output, sentiments):
        pred.append({
            "text": t,
            "topic": {"id": id, "name": id_to_topic[id]},
            "sentiment": s
        })
    return pred

@app.route('/')
def index():
    agg = agg_tweets_by_topic()
    labels=[]
    values=[]
    tweet_counts = { "labels": labels, "count": values }
    for a in agg:
        labels.append(a['_id']['name'])
        values.append(a['tweet_count'])
    print(labels)
    print(values)
    return render_template('index.html', tweet_counts=tweet_counts)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    pred = predict_text(data['data'])
    return jsonify(predicted_value=pred)

@app.route("/tweet/predict/<tag>", methods=['GET'])
def predict_tweets_byHasTag(tag):
    pred = predict_tweet(tag)
    myclient = pymongo.MongoClient(
        'mongodb+srv://root:0823632737@bcit-anurak.7belh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = myclient["myfirstpythonmongo"]
    collection = db['twitter2']

    myAnalysis = {"hashTagName": tag, "createdAt": str(
        datetime.now()), "predict_value": pred}
        
    collection.insert_one(myAnalysis)

    return jsonify(predicted_value=pred)

@app.route("/tweet/predict", methods=['GET'])
def predict_tweets_noHashTag():
    return jsonify(predicted_value=predict_tweet())


if __name__ == "__main__":
    app.run(debug=True)