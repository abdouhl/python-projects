
import json
import os
import sys
import random
import tweepy
from dotenv import load_dotenv
from os.path import join, dirname
from PIL import Image,ImageDraw,ImageFont
load_dotenv(join(dirname(__file__), '.env'))
from os import listdir

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

    im.save(join(dirname(__file__), 'img.jpg'))





title = title_quote
image_file = join(dirname(__file__), 'img.jpg')

    
users = api.search_users(author)
auth_username = users[0].screen_name



auth_tag = author.replace(' ','').lower()
if len(title_quote) > 100 :
    title_quote = f'{title_quote[:100]}...'
tweet = f'"{title_quote}" -- {author.title()} | @{auth_username}\n\n#{auth_tag} #quotes #quotesandsayings #motivation #inspiration #sayings #quote #quoteoftheday"'



    




media = api.media_upload(image_file)



post_result = api.update_status(status=tweet[:280], media_ids=[media.media_id])




