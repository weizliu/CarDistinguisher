import csv
import operator
brand_counts = {}
total_tweet = 0
total_brand = []
with open('tweet_data_all.csv', 'r') as f:
    r = csv.reader(f, delimiter = '|')
    for row in r:
        total_tweet = total_tweet + 1
        brand = row[1]
        total_brand.append(brand)
        brand_counts[brand] = brand_counts.get(brand, 0) + 1

l = sorted(brand_counts.items(), key = operator.itemgetter(1), reverse = True)

print "Total %d tweets for %d car brands " %(total_tweet, len(list(set(total_brand))))
for x in l:
    print x[0] + ' %f' %(x[1]*1.0/total_tweet)