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
    unit_all_tweets = agg_unit_tweets()
    data_all_tweets = []
    for d in unit_all_tweets:
        data_all_tweets.append(d['hashTagName'])
        data_all_tweets.append(d['tweet_counts'])
        data_all_tweets.append(d['createdAt'])

    agg = agg_tweets_by_topic()
    labels=[]
    values=[]
    for a in agg:
        labels.append(a['_id']['name'])
        values.append(a['tweet_count'])

    topic_id = [0, 1, 2, 3]
    sentiment = ['neg', 'neu', 'pos']

    topic_texts = []
    for t in topic_id:
        arr_texts = []
        for s in sentiment:
            arr_texts.append(get_tweets_texts(t, s))
        topic_texts.append(arr_texts)

    tweet_counts = { "labels": labels, "count": values,"data": data_all_tweets}

    tweet_counts_with_sentiment = agg_by_sentiment()
    for tw in tweet_counts_with_sentiment:
        print(tw)
    return render_template('index.html', tweet_counts=tweet_counts,tweet_sentiment=tweet_counts_with_sentiment, topic_texts = topic_texts)

@app.route('/testsentiment')
def testsentiment():
    return render_template('testsentiment.html')

@app.route('/gettweets')
def gettweets():
    return render_template('gettweets.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = []
    text = request.form['text']
    data.append(text)
    pred = predict_text(data)
    return jsonify(predicted_value=pred)

@app.route("/tweet/predict", methods=['POST'])
def predict_tweets_byHasTag():
    tag = request.form['tag']
    pred = predict_tweet(tag)

    collection = init_mongo()
    collection.drop()
    collection = init_mongo()
    datenow = datetime.now()
    datenow = str(datenow.strftime("%d/%m/%Y"))
    myAnalysis = {"hashTagName": tag, "createdAt": datenow, "predict_value": pred}
        
    collection.insert_one(myAnalysis)

    return jsonify(predicted_value=pred)

@app.route("/tweet/predict", methods=['GET'])
def predict_tweets_noHashTag():
    return jsonify(predicted_value=predict_tweet())



if __name__ == "__main__":
    app.run(debug=True)