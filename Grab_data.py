
# Using Twitter API for grabing the tweets data from Twitter

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import csv
import json
import time

consumer_key = 'gvUJ9I8YiQHaw2M0Fcfou2CC3'
consumer_secret = 'hvzuD9QjrhnuEhZvvw79jvHfApgtW2DfzlPFQauR26TQEE9TxB'
access_token = '1356806936-M0YK8ZD2ctd7qPOeaVlwBlJwHgqAjzBBig2DeNS'
access_token_secret = 'T7hFnK0HGLuPLIC8Enxn4ecv2Ogf0cxDl4mqQ1BsDVSW3'

class listener(StreamListener):

    num_tweets = 0

    def on_data(self, data):
    	try:
    		#tweet = data.split(',"text":"')[1].split('","source":"')[0]
            raw_tweet = json.loads(data)
            spec_tweet = {}

            if raw_tweet.get('text', None) is None or raw_tweet.get('user', None) is None or str(raw_tweet.get('lang')) != 'en':
                return True
            raw_tweet['text'] = textProcessing(raw_tweet['text'])
            car_label = get_label(raw_tweet['text'], car_brand_list)

            if car_label != '':
                listener.num_tweets += 1
                print "%d tweets retrieved!" %(listener.num_tweets)
                if listener.num_tweets > 5000: # Set the number of tweets to be retrieved
                    print "\nTotal Number of tweets retrieved: ", listener.num_tweets
                    return False
                for attribute in attributes:
                    if 'user_id' == attribute:
                        if raw_tweet.get('user', None) is not None:
                            spec_tweet['user_id'] = str(raw_tweet['user']['id_str'].encode('utf-8')).rstrip()
                    else:
                        if raw_tweet.get(attribute, None) is not None:
                            spec_tweet[attribute] = str(raw_tweet[attribute].encode('utf-8')).rstrip()
                spec_tweet['brand'] = car_label
                print spec_tweet
                with open ('tweet_data_all.csv', 'a') as f_tweet:
                    writer = csv.DictWriter(f_tweet, fieldnames = attributes, delimiter = '|')
                    writer.writerow(spec_tweet)

        	return True
        except BaseException, e:
        	print 'failed on_data, ', str(e)
        	time.sleep(1)

    def on_error(self, status):
       print status

# Process the tweet text, avoid irrelevant words being misassigned as car brand
def textProcessing(tweetText):
    tweetText_list = tweetText.lower().split()
    for ind in range(0, len(tweetText_list)):
        for word in tweetText_list:
            if '@' in word or 'http' in word:
                tweetText_list.remove(word)
    tweetText_string = ' '.join(tweetText_list)

    return tweetText_string

def carBrandList():
    f_carBrand = open('car_brand.txt')
    car_brand = f_carBrand.read().lower().splitlines()
    f_carBrand.close()
    return car_brand

def get_label(tweetText, carBrandList):
    label = ''
    tweetText_list = tweetText.lower().split()
    for brand in carBrandList:
        if brand in tweetText_list:
            return brand
    return label

car_brand_list = carBrandList()
filter_list = carBrandList()
for ind in range(0, len(car_brand_list)):
    filter_list[ind] = "my " + filter_list[ind]

attributes = ['user_id', 'brand', 'text']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=filter_list)


