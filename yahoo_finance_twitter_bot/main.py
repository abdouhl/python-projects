import tweepy
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from os.path import join, dirname
import urllib.request
import random

load_dotenv(join(dirname(__file__), '.env'))

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



req = requests.get('https://ar.quotes.quotesandsayings.net/authors/')
bs = BeautifulSoup(req.text, 'html.parser')
quotes = bs.find_all('li')
quote = random.choice(quotes)
author_name = quote.find('p').text
quote_text = quote.find('a').text

auth_tag = author_name.replace(' ','').lower()
tweet = f'"{quote_text}" -- {author_name}\n\n#{auth_tag} #حكم #معاني #أقوال #أقتباس'
api.update_status(tweet[:280])

"""
req = requests.get('https://finance.yahoo.com/news/rssindex')
bs = BeautifulSoup(req.text, 'xml')
items = bs.find_all('item')


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
    tweet_index = 0
    for item in items:
        if item.find('title').text[:240] in last_tweet_title:
            tweet_index = items.index(item) +1
            break
except:
    tweet_index = 0


item = items[tweet_index]
title = item.find('title').text
link = item.find('link').text
image_url = item.find('media:content').attrs['url']

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

# setting filename and image URL 
img_filename = join(dirname(__file__), 'tshirt_bot.jpeg')


# calling urlretrieve function to get resource
urllib.request.urlretrieve(image_url, img_filename)

api.update_status_with_media(status=f'{title[:240]}\n\n➡️Read More➡️{link}',filename=img_filename )
"""
