from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

ckey = 'wfU6nyT3GroxdPX2F7jerlhGG'
csecret = '0v7H1pWfEpsSChCd5ZsRAkL7hGNcxmBby1DUtYq0ehaGyOfnXR'
atoken = '2586502365-3u24Ea0wYAZc6np2lUY7FoOOZoVhTQspL7H3xuw'
asecret = 'nZAM8wwwXiJM0Fq9Yj0DuEqULJS0GSvVgRXmRuwX87wq4'

class listener(StreamListener):
    def on_data(self, data):
        try:
            user_id = data.split(',"id":')[1].split(',"id_str')[0]
            tweet = data.split(',"text":"')[1].split('","source')[0]
            import re
            t_list = re.split('\s+', tweet)
            tweet_new = ""
            label = ""

            for item in t_list:
                if '@' in item or 'http' in item:
                    t_list.remove(item)
                if item == '\n' or item == '\t' or item == '\f' or item == '\v':
                    t_list.remove(item)
                if item.lower() in brands:
                    label = item
            tweet_new = ' '.join(t_list)

            print tweet_new
            saveThis = str(user_id) + '::' + tweet_new + ' | ' + label
            saveFile = open('twitDB.csv','a')
            saveFile.write(saveThis)
            saveFile.write('\n')
            saveFile.close()
            return True
        except BaseException, e:
            print 'failed data', str(e)
            time.sleep(5)
    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
brands_p = ['my Audi', 'my BMW', 'my Cadillac', 'my Ferrari', 'my Jeep']
brands = ['audi', 'bmw', 'cadillac', 'ferrari', 'jeep']
twitterStream.filter(track=[i for i in brands_p])
