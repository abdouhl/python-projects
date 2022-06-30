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
from admitad import api, items
from os.path import join, dirname
from dotenv import load_dotenv


load_dotenv(join(dirname(__file__), '.env'))

client = pytumblr.TumblrRestClient(
    os.environ.get("ADMITAD_TUMBLR_BOT_CONSUMER_KEY"),
    os.environ.get("ADMITAD_TUMBLR_BOT_CONSUMER_SECRET"),
    os.environ.get("ADMITAD_TUMBLR_BOT_OAUTH_TOKEN"),
    os.environ.get("ADMITAD_TUMBLR_BOT_OAUTH_SECRET")
    )




def create_post():
    with open('resources/admitad_products_details.json') as j_f:
        products_details = json.load(j_f)

    product_url = random.choice(list(products_details.keys()))
    print(product_url)
    product_details = products_details[product_url]
    print(product_details)
    img_url = product_details['img']
    print(img_url)
    commission = product_details.get('off')
    if commission != None:
        commission = float(commission)
        print(commission)
    brand = product_details['brand']
    print(brand)
    title = product_details['title']
    print(title)
    price = float(product_details['price'].replace('US$',''))
    print(price)
    if commission != None:
        before_price = (price *100) / (100-commission)
        before_price = round(before_price, 2)

        print(before_price)


    bg_img = Image.new(mode="RGB",size=(1080,1920),color=(255,255,255))

    brand_name_file = brand.strip()
    brand_name_file = brand_name_file.replace(' ','_')
    brand_img = Image.open(f'resources/brands/{brand_name_file}.jpg')

    # Adding information about user agent
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    # setting filename and image URL
    filename = join(dirname(__file__),'img.jpg')

     
    # calling urlretrieve function to get resource
    urllib.request.urlretrieve(img_url, filename)
    
    product_img = Image.open(join(dirname(__file__),'img.jpg'))
    w,h = product_img.size
    if w == 1000 and h == 1000:
        print('w----h')
        n_w = w
        n_h = h
    else:
        if w == h:
            n_w = 1000
            n_h = 1000
            product_img = product_img.resize((n_w,n_h))
        else:
            if w >= h:
                n_w = 1000
                n_h = ((1000*h)/w)
                product_img = product_img.resize((n_w,n_h))
            else:
                n_w = ((1000*w)/h)
                n_h = 1000
                product_img = product_img.resize((int(n_w),int(n_h)))

    p_w = (1080 - n_w)/2
    bg_img.paste(product_img,(int(p_w),200))


    brand_img = brand_img.resize((300,100))
    print(brand_img.size)
    bg_img.paste(brand_img,(730,50))





    draw = ImageDraw.Draw(bg_img)

    fff = 51
    hig=1400
    while hig >400:
        txt = title
        fff -= 1
        fnt = ImageFont.truetype("resources/fonts/Tajawal-Bold.ttf", fff)
        wid,hig =draw.multiline_textsize( txt, font=fnt, spacing=20)
        pkk = int(wid/1000)+1
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
    draw.multiline_text((540, 1410), txt, font=fnt,anchor="mm",align="center",spacing=20, fill="black")
    if commission != None:
        fnt = ImageFont.truetype("resources/fonts//Tajawal-Bold.ttf", 120)
        draw.text((50, 50), f'{commission}', font=fnt,anchor="lt", fill="black")  
        print(fnt.getsize(f'{commission}'))
        num_w,num_h =fnt.getsize(f'{commission}')
        fnt_s = 65
        length = 200
        while length >= num_h/2:
            fnt_s -= 1
            fnt = ImageFont.truetype("resources/fonts//Tajawal-Bold.ttf", fnt_s)

            print(fnt_s)
            print(fnt.getsize('%'))
            l_w,length =fnt.getsize('%')
        draw.text((50+num_w, 50), '%', font=fnt,anchor="lt", fill="black")
        num_www,num_hhh =fnt.getsize('%')
        fnt_s = 65
        num_hh = 200
        num_ww = 200
        while num_hh >= num_h/2 or num_ww >= num_www: 
            fnt_s -= 1
            fnt = ImageFont.truetype("resources/fonts//Tajawal-Bold.ttf", fnt_s)
            
            print(fnt.getsize('OFF'))
            num_ww,num_hh =fnt.getsize('OFF')
        draw.text((50+num_w, 50+num_h), 'OFF', font=fnt,anchor="ls", fill="Silver")

    fnt = ImageFont.truetype("resources/fonts//Tajawal-Bold.ttf", 60)
    draw.text((50, 1750), f'US${price}', font=fnt,anchor="lb", fill="black") 
    num_ww,num_hh =fnt.getsize(f'US${price}')
    if commission != None:
        before_price = (price*100/(100-commission))
        before_price = round(before_price, 2)
        fnt = ImageFont.truetype("resources/fonts//Tajawal-Bold.ttf", 50)
        draw.text((num_ww+ 70, 1750), f'US${before_price}', font=fnt,anchor="lb", fill="DarkGray") 
        num_www,num_hhh =fnt.getsize(f'US${before_price}')
        draw.line([(num_ww+ 70, 1750-num_hhh//2), (num_ww+ 70+num_www, 1750-num_hhh//2)], fill ="DarkGray", width = 5)

    buy_img = Image.open('resources/buy.png')
    buy_img = buy_img.resize((366,84))
    bg_img.paste(buy_img,(352,1786))
    bg_img.save(join(dirname(__file__),'img.jpg'))


    clientt = api.get_oauth_client_client(
        os.environ.get("ADMITAD_BOT_CLIENT_ID"),
        os.environ.get("ADMITAD_BOT_CLIENT_SECRET"),
        os.environ.get("ADMITAD_BOT_SCOPE")
    )


    product_aff_url = clientt.DeeplinksManage.create(2182985, 13623, ulp=product_url, subid='brands')[0]

    tags = f"{title} {brand}".split(" ")



    res = client.create_photo('dealsstore', state="published", tags=tags, 
                    tweet=f"{brand}:{title}",
                    link=product_aff_url,
                    caption=f'<a href="{product_aff_url}">{brand}:{title}</a>',
                    data=join(dirname(__file__),'img.jpg'))
      
    





    
    
create_post()

