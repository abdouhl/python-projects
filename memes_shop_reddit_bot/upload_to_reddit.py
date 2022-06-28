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
import praw
import urllib.request
from os.path import join, dirname
from dotenv import load_dotenv


load_dotenv(join(dirname(__file__), '.env'))
 
reddit = praw.Reddit(client_id=os.environ.get("MEMES_SHOP_REDDIT_BOT_CLIENT_ID"),
                     client_secret=os.environ.get("MEMES_SHOP_REDDIT_BOT_CLIENT_SECRET"),
                     user_agent=os.environ.get("MEMES_SHOP_REDDIT_BOT_USER_AGENT"),
                     redirect_uri=os.environ.get("MEMES_SHOP_REDDIT_BOT_REDIRECT_URI"),
                     refresh_token=os.environ.get("MEMES_SHOP_REDDIT_BOT_REFRESH_TOKEN"))





def create_post():
    subr = 'memes_shop_' # Choose your subreddit 

    subreddit = reddit.subreddit(subr) # Initialize the subreddit to a variable

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
    filename = join(dirname(__file__),'img.jpg')


    # calling urlretrieve function to get resource
    urllib.request.urlretrieve(img_url, filename)
    reddit.validate_on_submit = True        
    selftext = title 
    try:
        choices = list(subreddit.flair.link_templates.user_selectable())
    
        template_id = next(x for x in choices if x["flair_text"] == flair)["flair_template_id"] 
    except:
        d = subreddit.flair.link_templates.add(flair)
        choices = list(subreddit.flair.link_templates.user_selectable())
    
        template_id = next(x for x in choices if x["flair_text"] == flair)["flair_template_id"] 
    title = selftext
    image = join(dirname(__file__),'img.jpg')
    images = [
        {
            "image_path": image,
            "caption": "➡️Check it out Now!➡️➡️",
            "outbound_url": url,
        },
        {
            "image_path": image,
            "caption": "➡️Check it out Now!➡️➡️",
            "outbound_url": url,
        },
    ]
    submission = subreddit.submit_gallery(title, images,flair_id=template_id)

    submission.mod.approve()

#    comment = submission.reply(title +f"➡️[Check it out Now!]({url})⬅️")
#    comment.mod.approve()
    return title
    
"""    
def invetation(title):
    with open('/root/memesssss/reddit/is_done.json') as f:
            is_done = json.load(f)
    authors = set()
    keywords_list = title.replace(":","").split(" ")
    for keyword in keywords_list:
        try:
            for submission in reddit.subreddit("all").search(keyword):
                authors.add(str(submission.author))
        except:
            continue

    pk = 1
    for author in authors:
        if pk == 5:
            break
        if author not in is_done.keys():
            try:
                print(author)
                reddit.redditor(author).message(
                "the best reddit shop", f"I've invited you to join our community r/memes_shop and see our last {title}", from_subreddit="memes_shop")
                
                pk += 1
                is_done[author] ="w"
                with open(f'/root/memesssss/reddit/is_done.json','w') as f:
                    json.dump(is_done,f)
            except:
                continue
    pk = 1
    for submission in reddit.subreddit("redbubblestores+redbubblepod+RedBubbleDesigns").new(limit=400):
        
        if pk == 10:
            break
        if str(submission.author) not in is_done.keys():
            try:
                print(str(submission.author),' red')
                reddit.redditor(str(submission.author)).message(
                "promote your redbubble store products on all social media", "hi, I'm a developer and marketing automation specialist\nI can create and set up a bot to promote your redbubble store products on all social media platforms\nthis is my example subreddit r/memes_shop\nand this is my all examples social media accounts:https://www.upwork.com/freelancers/~01ad28dd94deee7b56?viewMode=1&s=1017484851352698948", from_subreddit="memes_shop")
                
                pk += 1
                is_done[str(submission.author)] ="w"
                with open('/root/memesssss/reddit/is_done.json','w') as f:
                    json.dump(is_done,f)
            except:
                continue

"""




    
    
title = create_post()
#invetation(title)
