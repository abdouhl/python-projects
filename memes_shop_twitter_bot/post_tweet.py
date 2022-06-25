
import json
import os
import sys
import random
import tweepy
import urllib.request
from dotenv import load_dotenv
from os.path import join, dirname

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




with open('resources/products_detail.json') as f:
    products = json.load(f)
if products == {}:
        sys.exit()
url = random.choice(list(products.keys()))

information = products[url]
img_url = information["img"]
title = information["title"]
flair = information["category"]

print(url,img_url,title,flair)

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

# setting filename and image URL
filename = join(dirname(__file__), 'img.jpg')


# calling urlretrieve function to get resource
urllib.request.urlretrieve(img_url, filename)

media = api.media_upload(filename)
tags = title.split(' ')
tags_text = ''
for tag in tags:
    tag = tag.replace('-','')
    tags_text += f" #{tag}"

tweet = f"{title}\n➡️Check it out Now!➡️➡️{url}\n{tags_text}"
post_result = api.update_status(status=tweet[:500], media_ids=[media.media_id])

