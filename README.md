# CarDistinguisher
Using ones' tweets to decide which brand of car a person owns.

This project is to decide what kind of cars a person may owns from inspecting their tweets which not contain that car branch.

Firstly, download twitter API from https://github.com/tweepy/tweepy.git and install it

Secondly, download twitter-python from https://github.com/bear/python-twitter.git


# Grab_data.py uses twitter API to crawl tweets( mentions certain car brands in car_brands.txt) from twitter.


# pdata_user.py catches tweets of a specific user( specified the use id).


# brands_stats.py computes the percetage of tweets related to a certain car brand over the data we grab.
