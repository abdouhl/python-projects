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
import time
from os import listdir, remove
from PIL import Image, ImageEnhance,ImageDraw,ImageFont
import praw 
from praw.models import InlineImage
from os.path import join, dirname
from dotenv import load_dotenv
import pygsheets

time.sleep(60)
load_dotenv(join(dirname(__file__), '.env'))

reddit = praw.Reddit(client_id=os.environ.get("QUOTES_REDDIT_BOT_CLIENT_ID"),
                     client_secret=os.environ.get("QUOTES_REDDIT_BOT_CLIENT_SECRET"),
                     user_agent=os.environ.get("QUOTES_REDDIT_BOT_USER_AGENT"),
                     redirect_uri=os.environ.get("QUOTES_REDDIT_BOT_REDIRECT_URI"),
                     refresh_token=os.environ.get("QUOTES_REDDIT_BOT_REFRESH_TOKEN"))

def create_post():
    subr = 'quotes_and_sayings_' # Choose your subreddit quotesandsayings root

    subreddit = reddit.subreddit(subr) # Initialize the subreddit to a variable


        


    enteries = os.listdir('resources/quotes/') 
    quotes_len = 0
    while quotes_len <= 20:
        quote_file = random.choice(enteries)
        print(quote_file)
        with open(f'resources/quotes/{quote_file}') as f:
            quote_file_content =  json.load(f)
        if quote_file_content =={}:
            continue
        author_name = random.choice(list(quote_file_content.keys()))
        all_author_quotes = quote_file_content[author_name]
        quotes_len = len(all_author_quotes)
    all_author_quotes = all_author_quotes[:20]

    aauthor_name = author_name
    auth = author_name.replace(',','')
    auth = auth.replace('.','')
    auth = auth.replace("'",'')
    auth = auth.replace(" ",'-')
    auth = auth.lower()
    site_url = f"https://quotesandsayings.net/{auth}-quotes/"
    title =f"The Best 20 {author_name.title()} Quotes"

    content = ""
    k = 1
    for quote in all_author_quotes:
        content += f"- {quote}\n"
        if k ==5:
            content +=f'## for more {author_name.title()} quotes:[Click Here]({site_url})\n'
        k+=1
    
    choices = list(subreddit.flair.link_templates.user_selectable())
   
    template_id = next(x for x in choices if x["flair_text"] == "multi quotes")["flair_template_id"] #quote image | quote
    

    reddit.validate_on_submit = True
    submission = subreddit.submit(title,flair_id=template_id,selftext=content)
    submission.mod.approve()
 


def create_image_post():
    quotes = []
    images = []
    interies = listdir('resources/images/')
    if interies == []:
        sys.exit()
    for inter in interies:
        if inter.endswith(".jpg"):
            images.append(inter)

    while quotes == [] :
        image_path = random.choice(images)
        author = image_path.replace('.jpg','')
        author = author.replace('_',' ')
        author = author.lower()
        print(author)
        print(image_path)
        first_let = str(author).lower()[0]
        print(first_let)
        with open(f'resources/quotes/{first_let}_authors.json', 'r') as f:
            aaaaa = json.load(f)

        quotes = aaaaa.get(author.lower())

        quote = random.choice(quotes)
            
            

    print(quote)
    auth_tag = author.replace(' ','').lower()
    title_quote = f"{quote}"



    with Image.open(f"resources/images/{image_path}") as im:
        draw = ImageDraw.Draw(im)
        
        fff = 51
        hig=1400
        while hig >800:
            txt = f'"{quote}"'
            fff -= 1
            fnt = ImageFont.truetype('resources/fonts/Fraunces/static/Fraunces/Fraunces-MediumItalic.ttf', fff)
            wid,hig =draw.multiline_textsize( txt, font=fnt, spacing=20)
            pkk = int(wid/900)+1
            lenn = len(txt)
            index = int(lenn/pkk)
            txt = list(txt)
            while index <lenn:
                while txt[index] != ' ':
                    index -=1
                txt[index] = "\n"
                index += int(lenn/pkk)
            txt = "".join(txt)
            print(txt)
            
            wid,hig =draw.multiline_textsize( txt, font=fnt, spacing=20)
        draw.multiline_text((540, 450), txt, font=fnt,anchor="mm",align="center",spacing=20, fill="white")
        fnt = ImageFont.truetype("resources/fonts/Tajawal-Bold.ttf", 35)
        draw.text((540, (450+hig/2+100)), f'»»—— {author.title()} ——««', font=fnt,anchor="mb",align="center",spacing=20, fill="white")
        fnt = ImageFont.truetype("resources/fonts/Tajawal-Bold.ttf", 25)
        draw.text((540, (450+hig/2+200)), '– quotesandsayings.net', font=fnt,anchor="mb",align="center",spacing=20, fill="white")

        im.save(join(dirname(__file__),'img.jpg'))





    subr = 'quotes_and_sayings_' # Choose your subreddit

    subreddit = reddit.subreddit(subr) # Initialize the subreddit to a variable


        

    
    choices = list(subreddit.flair.link_templates.user_selectable())
   
    template_id = next(x for x in choices if x["flair_text"] == "quote image")["flair_template_id"] #quote image | quote
    reddit.validate_on_submit = True
    title = title_quote
    auth = author.replace(',','')
    auth = auth.replace('.','')
    auth = auth.replace("'",'')
    auth = auth.replace(" ",'-')
    auth = auth.lower()
    site_url = f"https://quotesandsayings.net/{auth}-quotes/"
    image = join(dirname(__file__),'img.jpg')
    images = [
        {
            "image_path": image,
            "caption": "➡️Click Here To Read More Quotes!➡️➡️",
            "outbound_url": site_url,
        },
        {
            "image_path": image,
            "caption": "➡️Click Here To Read More Quotes!➡️➡️",
            "outbound_url": site_url,
        },
    ]
    submission = subreddit.submit_gallery(title, images,flair_id=template_id)

    submission.mod.approve()      




def create_quote():
    interies = os.listdir('resources/quotes/')
    all_author_quotes = []
    while all_author_quotes == [] :
        quote_file = random.choice(interies)
        print(quote_file)
        with open(f'resources/quotes/{quote_file}') as f:
            quote_file_content =  json.load(f)
        author_name = random.choice(list(quote_file_content.keys()))
        all_author_quotes = quote_file_content[author_name]
        try:
            author_quote = random.choice(all_author_quotes)
            
        except:
            print('fff')
            all_author_quotes = []    
    print(author_name)
    print(author_quote)

    reddit_quote = f'"{author_quote}" -- {author_name.title()}\n#quotes #sayings #quotesandsayings'


    aauthor_name = author_name
    auth = author_name.replace(',','')
    auth = auth.replace('.','')
    auth = auth.replace("'",'')
    auth = auth.replace(" ",'-')
    auth = auth.lower()
    site_url = f"https://quotesandsayings.net/{auth}-quotes/"



    subr = 'quotes_and_sayings_' # Choose your subreddit

    subreddit = reddit.subreddit(subr) # Initialize the subreddit to a variable

    choices = list(subreddit.flair.link_templates.user_selectable())
   
    template_id = next(x for x in choices if x["flair_text"] == "quote")["flair_template_id"] #quote image | quote
    

    reddit.validate_on_submit = True
    submission = subreddit.submit(reddit_quote,flair_id=template_id,url=site_url)
    submission.mod.approve()
 

"""
def invetation(related_subreddits):
    with open('resources/reddit/is_done.json') as f:
            is_done = json.load(f)

    pk = 1
    for submission in reddit.subreddit(related_subreddits).new(limit=400):
        
        if pk == 5:
            break
        if str(submission.author) not in is_done.keys():
            try:
                print(str(submission.author))
                pk += 1
                reddit.redditor(str(submission.author)).message(
                "the best quotes community", "I've invited you to join our community r/quotes_and_sayings_", from_subreddit="quotes_and_sayings_")
                
                
                is_done[str(submission.author)] ="w"
                with open(f'resources/reddit/is_done.json','w') as f:
                    json.dump(is_done,f)
            except:
                continue
"""


number = random.randint(1,3)

if number == 1:
    create_image_post()
elif number == 2:
    create_image_post()
else:
    create_post()
"""
invetation("Showerthoughts+im14andthisisdeep+quotes+QuotesPorn+Stoicism+GetMotivated")
"""