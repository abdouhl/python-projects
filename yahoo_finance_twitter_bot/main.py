import tweepy
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from os.path import join, dirname


load_dotenv(join(dirname(__file__), '.env'))



req = requests.get('https://finance.yahoo.com/news/rssindex')
bs = BeautifulSoup(req.text, 'xml')
items = bs.find_all('item')

print(join(dirname(__file__), '.env'))
print(os.environ.get("YAHOO_FINANCE_TWITTER_BOT_CONSUMER_KEY"))

twitter_auth_keys = {
    "consumer_key"        : os.environ.get("YAHOO_FINANCE_TWITTER_BOT_CONSUMER_KEY"),
    "consumer_secret"     : os.environ.get("YAHOO_FINANCE_TWITTER_BOT_CONSUMER_SECRET"),
    "access_token"        : os.environ.get("YAHOO_FINANCE_TWITTER_BOT_ACCESS_TOKEN"),
    "access_token_secret" : os.environ.get("YAHOO_FINANCE_TWITTER_BOT_ACCESS_TOKEN_SECRET")
}

auth = tweepy.OAuthHandler(
    twitter_auth_keys['consumer_key'],
    twitter_auth_keys['consumer_secret']
    )
auth.set_access_token(
    twitter_auth_keys['access_token'],
    twitter_auth_keys['access_token_secret']
    )
api = tweepy.API(auth)


last_tweet_title = api.user_timeline(count=1)[0].text

items.reverse()
try:
    tweet_index = items.index(last_tweet_title)
except:
    tweet_index = 0


title = items[tweet_index].find('title').text
#link = item.find('link').text
#image_url = item.find('media:content').attrs['url']
    

api.update_status(title[:280])