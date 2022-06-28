from datetime import date,datetime
import tweepy
from os.path import join, dirname
from dotenv import load_dotenv
import json
import pygsheets
import os
import random
import time

time.sleep(60)
load_dotenv(join(dirname(__file__), '.env'))

twitter_auth_keys = {
    "consumer_key"        : os.environ.get("MEMES_SHOP_TWITTER_BOT_CONSUMER_KEY"),
    "consumer_secret"     : os.environ.get("MEMES_SHOP_TWITTER_BOT_CONSUMER_SECRET"),
    "access_token"        : os.environ.get("MEMES_SHOP_TWITTER_BOT_ACCESS_TOKEN"),
    "access_token_secret" : os.environ.get("MEMES_SHOP_TWITTER_BOT_ACCESS_TOKEN_SECRET")
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
	json.dump(json.loads(os.environ.get("MEMES_SHOP_TWITTER_BOT_GDRIVE_API_CREDENTIALS")),f)
gc = pygsheets.authorize(service_file=join(dirname(__file__), 'gsheets_api-credentials.json'))

sht = gc.open_by_key(os.environ.get("MEMES_SHOP_TWITTER_BOT_SHEET_KEY"))
wks_users = sht.worksheet_by_title("memes follow unfollow")
wks_tweets = sht.worksheet_by_title("memes likes")
    





#follow users
done_users = []
for number in range(1,1000000):
	user_screen_name = wks_users.cell(f'A{number}').value
	done_users.append(user_screen_name)
	if user_screen_name == '':
		user_num = number
		break

ids_list = ['369583954','2423920854','178463040','946502779','1409798257','47786101','391037985']
for user in api.get_followers(id =random.choice(ids_list),count=200):
	if user.screen_name not in done_users:
		user.follow()
		print('follow',user.screen_name)
		wks_users.cell(f'A{user_num}').value = user.screen_name
		wks_users.cell(f'B{user_num}').value = f'{date.today().strftime("%d/%m/%y")}'
		break

#unfollow users

for number in range(1,1000000):
	b_val = wks_users.cell(f'B{number}').value
	user_screen_name = wks_users.cell(f'A{number}').value
	if b_val != 'unfollow' and b_val != '':
		if datetime.strptime(b_val, '%d/%m/%y') <  datetime.strptime(date.today().strftime("%d/%m/%y"),"%d/%m/%y"):
			try:
				api.get_user(screen_name=user_screen_name).unfollow()
			except:
				pass
			print('unfollow',user_screen_name)
			wks_users.cell(f'B{number}').value = 'unfollow'
			break
		if datetime.strptime(b_val, '%d/%m/%y') >=  datetime.strptime(date.today().strftime("%d/%m/%y"),"%d/%m/%y"):
			break
	if b_val == "":
		break
		


#like tweets
done_tweets = []
for number in range(1,1000000):
	tweet_id_str = wks_tweets.cell(f'A{number}').value
	done_tweets.append(tweet_id_str)
	if tweet_id_str == '':
		tweet_num = number
		break

hashtags_list = ['TheNotoriousMMA','roses_are_reosi','RobertDowneyJr','twhiddleston','Cumberbitches','KeanuReevess_','bts_bighit']
for tweet in api.search_tweets(random.choice(hashtags_list),result_type='recent',count=100):
	if tweet.id_str not in done_tweets:
		try:
			api.create_favorite(tweet.id_str)
		except:
			pass
		
		#api.destroy_favorite()
		print('like',tweet.id_str)
		wks_tweets.cell(f'A{tweet_num}').value = tweet.id_str
		break


