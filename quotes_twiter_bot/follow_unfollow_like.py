from datetime import date
import json
import tweepy
import os
from os.path import join, dirname


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



done_users_file = join(dirname(__file__), 'done_users.json')
done_users_unfollow_file = join(dirname(__file__), 'done_users_unfollow.json')
done_tweets_file = join(dirname(__file__), 'done_tweets.json')


#follow users
with open(done_users_file) as j_f: 
	done_users = json.load(j_f) 
with open(done_users_unfollow_file) as j_f:
	done_users_unfollow = json.load(j_f)
	
for user in api.get_followers(id ='57962071',count=200):
	if user.screen_name not in list(done_users.keys()):
		user.follow()
		print('follow',user.screen_name)
		done_users[user.screen_name] = date.today().strftime("%d/%m/%Y")
		done_users_unfollow[user.screen_name] = date.today().strftime("%d/%m/%Y")
		break

with open(done_users_file,'w') as f:
	json.dump(done_users,f)
with open(done_users_unfollow_file,'w') as f:
	json.dump(done_users_unfollow,f)

#unfollow users
with open(done_users_unfollow_file) as j_f:
	done_users_unfollow = json.load(j_f)
	
for user in list(done_users_unfollow.keys()):
	if done_users_unfollow[user] != date.today().strftime("%d/%m/%Y"):
		api.get_user(screen_name=user).unfollow()
		print('unfollow',user)
		done_users_unfollow.pop(user)
		break

with open(done_users_unfollow_file,'w') as f:
	json.dump(done_users_unfollow,f)



#like tweets
with open(done_tweets_file) as j_f:
	done_tweets = json.load(j_f) 

for tweet in api.search_tweets('kitesurfing',result_type='recent',count=100):
	if tweet.id_str not in list(done_tweets.keys()):
		api.create_favorite(tweet.id_str)
		#api.destroy_favorite()
		print('like',tweet.id_str)
		done_tweets[tweet.id_str] = tweet.id_str
		break

with open(done_tweets_file,'w') as f:
	json.dump(done_tweets,f)



