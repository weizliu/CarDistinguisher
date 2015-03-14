#This is used to catch tweets(up to 100 tweets) of a spcific user(using user id)
import twitter
api = twitter.Api(consumer_key = 'wfU6nyT3GroxdPX2F7jerlhGG',
consumer_secret = '0v7H1pWfEpsSChCd5ZsRAkL7hGNcxmBby1DUtYq0ehaGyOfnXR',
access_token_key = '2586502365-3u24Ea0wYAZc6np2lUY7FoOOZoVhTQspL7H3xuw',
access_token_secret = 'nZAM8wwwXiJM0Fq9Yj0DuEqULJS0GSvVgRXmRuwX87wq4')

userID_file = open('user_id', 'r') #user_id is a file storing user id
user_id = []
line = userID_file.readline()
while line:
    user_id.append(line)
    line = userID_file.readline()
userID_file.close()

twitter = open('tweets_per_user.txt','w') #write user id and 100 tweets(tweets are consecutive) in to a file

for item in user_id:
    twitter.write(item[0:len(item)-1] + ': ')
    statuses = api.GetUserTimeline(user_id = item, count = 100)
    for s in statuses:
        print s.text
        ss = str(s.text.encode('utf-8')).rstrip()
        twitter.write(ss)
        twitter.write(' ')
    twitter.write('\n')
twitter.close()

