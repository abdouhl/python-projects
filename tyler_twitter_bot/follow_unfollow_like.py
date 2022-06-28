from datetime import date,datetime
import tweepy
from os.path import join, dirname
from dotenv import load_dotenv
import json
import pygsheets
import os
import random

load_dotenv(join(dirname(__file__), '.env'))




twitter_auth_keys = {
	"consumer_key"        : os.environ.get("TYLER_BOT_CONSUMER_KEY"),
	"consumer_secret"     : os.environ.get("TYLER_BOT_CONSUMER_SECRET"),
	"access_token"        : os.environ.get("TYLER_BOT_ACCESS_TOKEN"),
	"access_token_secret" : os.environ.get("TYLER_BOT_ACCESS_TOKEN_SECRET")
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


with open( join(dirname(__file__), 'gsheets_api-credentials.json'),'w') as f:
    json.dump(json.loads(os.environ.get("TYLER_BOT_GDRIVE_API_CREDENTIALS")),f)

gc = pygsheets.authorize(service_file=join(dirname(__file__), 'gsheets_api-credentials.json'))

sht = gc.open_by_key(os.environ.get("TYLER_BOT_SHEET_KEY"))
wks_keywords = sht.worksheet_by_title("keywords")
wks_influencers = sht.worksheet_by_title("influencers")
wks_done_tweets = sht.worksheet_by_title("done_tweets")

keywords = []
for number in range(1,100):
    keyword = wks_keywords.cell(f'A{number}').value
    if keyword == '':
        break
    keywords.append(keyword)

influencers = []
for number in range(1,100):
    influencer = wks_influencers.cell(f'A{number}').value
    if influencer == '':
        break
    influencers.append(influencer)
    
done_tweets = []
for number in range(1,200000):
    done_tweet = wks_done_tweets.cell(f'A{number}').value
    if done_tweet == '':
        tweet_num = number
        break
    done_tweets.append(done_tweet)

influencer = random.choice(influencers)
keyword = random.choice(keywords)


for tweet in api.search_tweets(keyword,result_type='recent',count=100):
    if tweet.id_str not in done_tweets:
        try:
             api.create_favorite(tweet.id_str)
        except:
            continue
        print(tweet.id_str)
        wks_done_tweets.cell(f'A{tweet_num}').value = tweet.id_str
        break




















