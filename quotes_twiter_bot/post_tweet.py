
import json
import os
import sys
import random
import tweepy
from dotenv import load_dotenv
from os.path import join, dirname


load_dotenv(join(dirname(__file__), '.env'))

twitter_auth_keys = {
    "consumer_key"        : os.environ.get("QUOTES_TWITER_BOT_CONSUMER_KEY"),
    "consumer_secret"     : os.environ.get("QUOTES_TWITER_BOT_CONSUMER_SECRET"),
    "access_token"        : os.environ.get("QUOTES_TWITER_BOT_ACCESS_TOKEN"),
    "access_token_secret" : os.environ.get("QUOTES_TWITER_BOT_ACCESS_TOKEN_SECRET")
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


interies = os.listdir('resources/quotes/')

quote_file = random.choice(interies)
with open(f'resources/quotes/{quote_file}') as f:
    quote_file_content =  json.load(f)
author_name = random.choice(list(quote_file_content.keys()))
all_author_quotes = quote_file_content[author_name]
author_quote = random.choice(all_author_quotes)

auth_tag = author_name.replace(' ','').lower()
tweet = f'"{author_quote}" -- {author_name.title()}\n#{auth_tag} #quotes #quotesandsayings #motivation #inspiration #sayings #quote #quoteoftheday"'
if len(author_quote) > 280 :
    tweet = f'{author_quote[:280]}'


    
api.update_status(tweet)








