#!/usr/bin/env python
 
"""This example demonstrates the flow for retrieving a refresh token.
 
In order for this example to work your application's redirect URI must be set to
http://localhost:8080.
 
This tool can be used to conveniently create refresh tokens for later use with your web
application OAuth2 credentials.
token = '808708533690-9vRl3_wlRfUsOcuMpCIkbvAEHcT4Sw' 
"""
import json
import os
import random
import socket
import sys
from os import listdir, remove
from PIL import Image, ImageEnhance,ImageDraw,ImageFont
import urllib.request
import pytumblr
from os.path import join, dirname
from dotenv import load_dotenv


load_dotenv(join(dirname(__file__), '.env'))

client = pytumblr.TumblrRestClient(
    os.environ.get("MEMES_SHOP_TUMBLR_BOT_CONSUMER_KEY"),
    os.environ.get("MEMES_SHOP_TUMBLR_BOT_CONSUMER_SECRET"),
    os.environ.get("MEMES_SHOP_TUMBLR_BOT_OAUTH_TOKEN"),
    os.environ.get("MEMES_SHOP_TUMBLR_BOT_OAUTH_SECRET")
    )



def create_post():
    
    with open('resources/products_detail.json') as f:
        products = json.load(f)
    if products == {}:
        sys.exit()
    url = random.choice(list(products.keys()))

    information = products[url]
    img_url = information["img"]
    title = information["title"]
    category = information["category"]
    print(category)
    

    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    # setting filename and image URL
    filename = join(dirname(__file__),'img.jpg')


    # calling urlretrieve function to get resource
    urllib.request.urlretrieve(img_url, filename)
    tags = f"{title} {category}".split(" ")
    text =f"![Foo]({img_url})➡️➡️[Check it out Now!]({url})⬅️⬅️"



    res = client.create_photo('memesshop', state="published", tags=tags,
                    tweet=title,
                    link=url,
                    caption=f'<a href="{url}">{title}</a>',
                    data=join(dirname(__file__),'img.jpg')) 
      


    
    
    





    
    
create_post()

