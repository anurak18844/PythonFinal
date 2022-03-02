import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    def __init__(self):
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'zKx6enUvZYvc9ZnTYHbElfadD'
        consumer_secret = 'KYZN94qX6YRxP4RVr5EVezRsitddDL4JPXiCrOzj13gCIBv668'
        access_token = '86001446-MDeh313maF0A9EOfxgPprQpH5AsDX8qxb4IUGTpjS'
        access_token_secret = 'UPUOC1bHPygRk4ps3TU0UWr0EQuckUyxZjJafVaAKZ01u'
  
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
  
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z\u0E00-\u0E7F \t])|(\w+:\/\/\S+)|(^RT)", " ", tweet).split())
  
    # def get_tweet_sentiment(self, tweet):
    #     '''
    #     Utility function to classify sentiment of passed tweet
    #     using textblob's sentiment method
    #     '''
    #     # create TextBlob object of passed tweet text
    #     analysis = TextBlob(self.clean_tweet(tweet))
    #     # set sentiment
    #     if analysis.sentiment.polarity > 0:
    #         return 'positive'
    #     elif analysis.sentiment.polarity == 0:
    #         return 'neutral'
    #     else:
    #         return 'negative'
  
    def get_tweets(self, query, count = 200):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
  
        try:
            # call twitter api to fetch tweets
            # fetched_tweets = self.api.search(q = query, count = count)
            fetched_tweets=tweepy.Cursor(self.api.search,q=query,tweet_mode="extended").items(count)
  
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
  
                # saving text of tweet
                parsed_tweet['text'] = tweet._json['full_text']
                # saving sentiment of tweet
                # parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
  
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
  
            # return parsed tweets
            return tweets
  
        except tweepy.errors.TweepyException as e:
            # print error (if any)
            print("Error : " + str(e))