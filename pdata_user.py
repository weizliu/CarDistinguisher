# -*- codingL: utf-8 -*-
import twitter
import csv
import re
import time


def textProcessing(tweetText):
#This is used to catch tweets(up to 100 tweets) of a spcific user(using user id)
    tweetText_list = tweetText.lower().split()
    for ind in range(0, len(tweetText_list)):
        for word in tweetText_list:
            if '@' in word or 'http' in word:
                tweetText_list.remove(word)
    tweetText_string = ' '.join(tweetText_list)
    return tweetText_string


api = twitter.Api(consumer_key = 'wfU6nyT3GroxdPX2F7jerlhGG',
consumer_secret = '0v7H1pWfEpsSChCd5ZsRAkL7hGNcxmBby1DUtYq0ehaGyOfnXR',
access_token_key = '2586502365-3u24Ea0wYAZc6np2lUY7FoOOZoVhTQspL7H3xuw',
access_token_secret = 'nZAM8wwwXiJM0Fq9Yj0DuEqULJS0GSvVgRXmRuwX87wq4')

userID_file = open('user_id.csv', 'r') #user_id is a file storing user id
line = userID_file.readline()

while 1:
    if len(line) == 0:
        break
    try:
        content = re.split(',', line)
        userid = content[0]
        user_label = content[1][0:(len(content[1])-2)]
        print userid
        file_name = str(userid) + '.' + user_label + '.csv'
        twitter_f = open(file_name, 'w')
        twitter_c = csv.writer(twitter_f)
        statuses = api.GetUserTimeline(user_id = userid, count = 200)
        count = 0
        for s in statuses:
            #print s.text
            ss = str(s.text.encode('utf-8')).rstrip()
            ss_tp = textProcessing(ss)
            twitter_c.writerow([ss_tp])
        line = userID_file.readline()
        time.sleep(7)
        twitter_f.close()
    except BaseException, e:
        print 'failed on data ', str(e)
        line = userID_file.readline()
        time.sleep(7)
userID_file.close()
