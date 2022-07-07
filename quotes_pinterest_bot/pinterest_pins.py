from os import listdir, remove
import os
import random
import json
import base64
import sys
from PIL import Image, ImageEnhance,ImageDraw,ImageFont
from dotenv import load_dotenv
from os.path import join, dirname
import imgbbpy
from ayrshare import SocialPost


load_dotenv(join(dirname(__file__), '.env'))

with open(join(dirname(__file__), 'is_done.json'), 'r') as f:
	authors_done = json.load(f)

quotes = []
images = []
author = ''
interies = listdir('resources/pinterest_images/')
if interies == []:
	sys.exit()
for inter in interies:
	if inter.endswith(".jpg"):
		images.append(inter)

while quotes == [] and author not in authors_done.keys():
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




with Image.open(f"resources/pinterest_images/{image_path}") as im:
	draw = ImageDraw.Draw(im)
	
	fff = 51
	hig=1400
	while hig >1200:
		txt = f'"{quote}"'
		fff -= 1
		fnt = ImageFont.truetype('resources/fonts/Fraunces/static/Fraunces/Fraunces-MediumItalic.ttf', fff)
		wid,hig =draw.multiline_textsize( txt, font=fnt, spacing=20)
		pkk = int(wid/800)+1
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
	draw.multiline_text((540, 860), txt, font=fnt,anchor="mm",align="center",spacing=20, fill="white")
	fnt = ImageFont.truetype("resources/fonts//Tajawal-Bold.ttf", 40)
	draw.multiline_text((540, (860+hig/2+100)), f'»»—— {author.title()} ——««', font=fnt,anchor="mm",align="center",spacing=20, fill="white")
	fnt = ImageFont.truetype("resources/fonts//Tajawal-Bold.ttf", 30)
	draw.multiline_text((540, (860+hig/2+200)), '– quotesandsayings.net', font=fnt,anchor="mm",align="center",spacing=20, fill="white")
	img = Image.open('resources/click.png', 'r')
	offset = (190, 1760)

	im.paste(img, offset)
	im.save(join(dirname(__file__), f"{quote[:50]}.jpg"))



imgbb_client = imgbbpy.SyncClient(os.environ.get("QUOTES_META_BOT_IMGBB_CLIENT"))
file_from = join(dirname(__file__), f"{quote[:50]}.jpg")
image = imgbb_client.upload(file=file_from)
print('imgbbpy image url',image.url)












access_token = os.environ.get("QUOTES_PINTEREST_BOT_ACCESS_TOKEN")
if author in authors_done.keys():
	idid = authors_done[author] 
else:
	sys.exit()
auth = str(author.replace(' ','-'))
aauth = auth.replace('.','')
aauth = aauth.replace("'",'')
aauth = aauth.replace(",",'')
aauth = aauth.lower()
img_url = f"https://quotesandsayings.net/{aauth}-quotes/"



auth_tag = author.replace(' ','')
title_pin = f"{author} quote:{quote[:50]}"
des_pin = f"the best {author} quote:\n{quote} \n #{auth_tag} #quotes #quotesandsayings #motivation #inspiration #sayings #quote #quoteoftheday"
alt_text_pin = f"the best {author} quote:\n{quote}"

social = SocialPost(os.environ.get("QUOTES_PINTEREST_BOT_AYRSH"))
postResult = social.post({
   "post": des_pin[:500],
   "platforms": ["pinterest"],
   "mediaUrls": [image.url],
   "pinterestOptions": {
      "title": title_pin[:100], 
      "link": img_url,  
      "boardId": idid             
   }
} )


