import requests
import json
from os import listdir, remove
import os
import random
import imgbbpy
import facebook
import base64
import sys
from PIL import Image, ImageEnhance,ImageDraw,ImageFont
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), '.env'))

facebook_access_token = os.environ.get("QUOTES_META_BOT_FACEBOOK_ACCESS_TOKEN")
insta_token = os.environ.get("QUOTES_META_BOT_INSTA_TOKEN")
imgbb_client = imgbbpy.SyncClient(os.environ.get("QUOTES_META_BOT_IMGBB_CLIENT"))
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
fb_quote = f"the best {author.title()} quote:\n{quote}\n #{auth_tag} #quotes #quotesandsayings #motivation #inspiration #sayings #quote #quoteoftheday"



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






file_from = join(dirname(__file__), 'img.jpg')
image = imgbb_client.upload(file=file_from)
print(image.url)









#Post the Image
image_location_1 = image.url

post_url = 'https://graph.facebook.com/v10.0/{}/media'.format('17841432761702016')
payload = {
'image_url': image_location_1,
'caption': fb_quote,
'access_token': insta_token
}
result = requests.post(post_url, data=payload)
print(result.text[7:-2])

if 'id' in result.text:
  
  second_url = 'https://graph.facebook.com/v10.0/{}/media_publish'.format('17841432761702016')
  second_payload = {
  'creation_id': result.text[7:-2],
  'access_token': insta_token
  }
  r = requests.post(second_url, data=second_payload)
  print('--------Just posted to instagram--------')
  print(r.text)
else:
  print('HOUSTON we have a problem')




graph = facebook.GraphAPI(access_token=facebook_access_token, version="3.0")
graph.put_photo(image=open(join(dirname(__file__), 'img.jpg'), 'rb'),message=fb_quote)









