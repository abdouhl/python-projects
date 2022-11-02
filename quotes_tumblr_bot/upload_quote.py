import json
import os
import random
import pytumblr
from os import listdir, remove
from PIL import Image, ImageEnhance,ImageDraw,ImageFont
import sys
from os.path import join, dirname
import urllib.request

# Authenticate via OAuth 
client = pytumblr.TumblrRestClient(os.environ.get("QUOTES_TUMBLR_BOT_CONSUMER_KEY"),os.environ.get("QUOTES_TUMBLR_BOT_CONSUMER_SECRET"),os.environ.get("QUOTES_TUMBLR_BOT_OAUTH_TOKEN"),os.environ.get("QUOTES_TUMBLR_BOT_OAUTH_SECRET")) 

# Make the request 

def create_post():
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
    slug = f"{auth}-quotes"
    content = "<ol>"
    k = 1
    for quote in all_author_quotes:
        content += f"<li>{quote}</li>"
        if k ==5:
            content +="</ol>"
            content +=f'<h4>for more {author_name.title()} quotes:<a href="{site_url}">Click Here</a></h4>'
            content +="[[MORE]]"
            content +='<ol start="6" >'
        k+=1
    content +="</ol>"
    tags=["quotes", "sayings","relatable quotes","relationship", "love quotes","love","quotes", "relationship quotes","life quotes","feelings", "quote","emotions"]
    res = client.create_text('quotesandsayings-net',tags=tags, format='html',state="published", slug=slug, title=title, body=content)
    print(res)
    print(aauthor_name)


def create_card():
    with open('quotes_twiter_bot/quotes.json') as f:
        quotes = json.load(f)
    quote_link = random.choice(list(quotes.keys()))
    quote_text = quotes[quote_link][1]
    author_name = quotes[quote_link][0]
    auth_tag = author_name.replace(' ','').lower()
    tags=[f"{auth_tag}","quotes", "sayings","relatable quotes","relationship", "love quotes","love","quotes", "relationship quotes","life quotes","feelings", "quote","emotions"]
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    # setting filename and image URL 
    filename =  join(dirname(__file__),'og_card_image.jpg')
    image = quote_link + 'og_card_image.jpg'

    # calling urlretrieve function to get resource
    urllib.request.urlretrieve(image, filename)
    client.create_photo('quotesandsayings-net', state="published", tags=tags,
                    tweet=quote_text,
                    caption=f""f'<a href="{quote_link}">{author_name.title()} quote:{quote_text}</a>',
                    data=filename)
    

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
    aauthor_name = author_name
    auth = author_name.replace(',','')
    auth = auth.replace('.','')
    auth = auth.replace("'",'')
    auth = auth.replace(" ",'')
    auth = auth.lower()
    tags=[f"{auth}","quotes", "sayings","relatable quotes","relationship", "love quotes","love","quotes", "relationship quotes","life quotes","feelings", "quote","emotions"]
    source =f"- {author_name} -"
    res = client.create_quote('quotesandsayings-net',tags=tags, state="published", quote=author_quote, source=source)
 


def create_image_link():
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
    image = join(dirname(__file__), 'img.jpg')
    
    
    auth = author.replace(',','')
    auth = auth.replace('.','')
    auth = auth.replace("'",'')
    auth = auth.replace(" ",'')
    auth = auth.lower()
    tags=[f"{auth}","quotes", "sayings","relatable quotes","relationship", "love quotes","love","quotes", "relationship quotes","life quotes","feelings", "quote","emotions"]
    
    auth = author.replace(',','')
    auth = auth.replace('.','')
    auth = auth.replace("'",'')
    auth = auth.replace(" ",'-')
    auth = auth.lower()
    site_url = f"https://quotesandsayings.net/{auth}-quotes/"
    client.create_photo('quotesandsayings-net', state="published", tags=tags,
                    tweet=title_quote,
                    caption=f""f'<a href="{site_url}">{author.title()} quote:{title}</a>',
                    data=image)
      








number = random.randint(1,3)

if number == 1:
    create_card()
elif number == 2:
    create_card()
else:
    create_card()
