import json
import os
import sys
import random
import time
import tweepy
from PIL import Image, ImageEnhance,ImageDraw,ImageFont
import urllib.request
twitter_auth_keys = {
    "consumer_key"        : "eA2pLQMuVuhD10flCoIM4AsNq",
    "consumer_secret"     : "Nb6kOiyydXEkCopgDd0yIfrz0QBJLfcWr3hv6i0PqkcQXP3Rgn",
    "access_token"        : "765948457706225664-FUYkkjF2GJB0uyL9aqa8MNYe6uXndtj",
    "access_token_secret" : "OibqjClkbYAxeqb0KI2ASZil5H8ORkHtOR7K5elgrfXYY"
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
with open('/root/quotes_and_sayings/done_tweets.json') as j_f:
    done_tweets = json.load(j_f) 

statuses = api.mentions_timeline(count = 20)
ppkp = 0
if statuses[ppkp].in_reply_to_status_id_str in list(done_tweets.keys()):
    ppkp+= 1

tweet_text = api.get_status(statuses[ppkp].in_reply_to_status_id).text
profile_image_url_https = api.get_status(statuses[ppkp].in_reply_to_status_id).author.profile_image_url_https.replace('normal','400x400')
name = api.get_status(statuses[ppkp].in_reply_to_status_id).author.name
screen_name = api.get_status(statuses[ppkp].in_reply_to_status_id).author.screen_name
quote = tweet_text








opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

# setting filename and image URL
filename = '/root/quotes_and_sayings/quotes_bot.png'


# calling urlretrieve function to get resource
urllib.request.urlretrieve(profile_image_url_https, filename)




time.sleep(2)

im = Image.open("/root/quotes_and_sayings/quotes_bot.png")

#Display actual image
im.show()

#Make the new image half the width and half the height of the original image
resized_im = im.resize((round(1080), round(1080)))



enhancer = ImageEnhance.Brightness(resized_im)

factor = 0.3 #brightens the image
cropped_image = enhancer.enhance(factor)

enhancer = ImageEnhance.Contrast(cropped_image)

factor = 0.5 #brightens the image
cropped_image = enhancer.enhance(factor)

enhancer = ImageEnhance.Sharpness(cropped_image)

factor = 0.0 
resized_im = enhancer.enhance(factor)

resized_im.save('/root/quotes_and_sayings/quotes_bot.png')



time.sleep(2)

with Image.open("/root/quotes_and_sayings/quotes_bot.png") as im:
    draw = ImageDraw.Draw(im)
    
    fff = 51
    hig=1400
    while hig >800:
        txt = f'{quote}'
        fff -= 1
        fnt = ImageFont.truetype('/root/quotes_and_sayings/resources/fonts/Fraunces/static/Fraunces/Fraunces-MediumItalic.ttf', fff)
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
    fnt = ImageFont.truetype("/root/quotes_and_sayings/resources/fonts/Tajawal-Bold.ttf", 35)
    draw.text((540, (450+hig/2+100)), f'»»—— {name.title()} ——««', font=fnt,anchor="mb",align="center",spacing=20, fill="white")
    fnt = ImageFont.truetype("/root/quotes_and_sayings/resources/fonts/Tajawal-Bold.ttf", 25)
    draw.text((540, (450+hig/2+200)), f'@{screen_name}', font=fnt,anchor="mb",align="center",spacing=20, fill="white")

    im.save("/root/quotes_and_sayings/quotes_bot.png")





api.update_status_with_media(status=f'@{screen_name}',filename="/root/quotes_and_sayings/quotes_bot.png", in_reply_to_status_id = statuses[ppkp].in_reply_to_status_id )

done_tweets[statuses[ppkp].in_reply_to_status_id_str] = statuses[ppkp].in_reply_to_status_id_str
with open('/root/quotes_and_sayings/done_tweets.json','w') as f:
    json.dump(done_tweets,f)
