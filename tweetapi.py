import twitterclient


def get_tweets(tag):
    api = twitterclient.TwitterClient()
    # hashtag = "MyDearNVC"
    hashtag = tag

    # tweets = api.get
    tweets = api.get_tweets(query = '#'+hashtag, count = 500)
    cleaned_tweets = [api.clean_tweet(tw['text']).replace(hashtag,"").lstrip() for tw in tweets]

    return cleaned_tweets
  
# if __name__ == "__main__":
#     main()
