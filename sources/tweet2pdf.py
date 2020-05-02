import json
import pandas as pd
import twitter

#import api credentials
from twitter_cred import consumer_key, consumer_secret, access_token_key, access_token_secret

#define api
api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)

#download tweets
def get_tweets(api=api, screen_name=None):
    timeline = api.GetUserTimeline(screen_name=screen_name, count=5000)
    earliest_tweet = min(timeline, key=lambda x: x.id).id

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            timeline += tweets
    #convert tweets to df
    date = []
    text = []
    name = []
    for tweet in timeline:
        json_str = json.dumps(tweet._json)
        date.append(json.loads(json_str)['created_at'])
        text.append(json.loads(json_str)['text'])
        name.append(json.loads(json_str)['user']['screen_name'])
    return(pd.DataFrame({'name':name,'text':text,'date':date}))