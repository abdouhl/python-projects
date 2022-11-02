import json
import os
import random
import socket
import sys
from os import listdir, remove
import praw 
from praw.models import InlineImage
from os.path import join, dirname
from dotenv import load_dotenv
import pygsheets
import urllib.request


load_dotenv(join(dirname(__file__), '.env'))

reddit = praw.Reddit(client_id=os.environ.get("QUOTES_REDDIT_BOT_CLIENT_ID"),
                     client_secret=os.environ.get("QUOTES_REDDIT_BOT_CLIENT_SECRET"),
                     user_agent=os.environ.get("QUOTES_REDDIT_BOT_USER_AGENT"),
                     redirect_uri=os.environ.get("QUOTES_REDDIT_BOT_REDIRECT_URI"),
                     refresh_token=os.environ.get("QUOTES_REDDIT_BOT_REFRESH_TOKEN"))



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



    subr = 'quotesandsayings__net' 

    subreddit = reddit.subreddit(subr) # Initialize the subreddit to a variable

    choices = list(subreddit.flair.link_templates.user_selectable())
   
    template_id = next(x for x in choices if x["flair_text"] == "quote")["flair_template_id"] #quote image | quote
    

    reddit.validate_on_submit = True
    submission = subreddit.submit(reddit_quote,flair_id=template_id,url=site_url)
    submission.mod.approve()
 

with open( join(dirname(__file__), 'gsheets_api-credentials.json'),'w') as f:
    json.dump(json.loads(os.environ.get("QUOTES_REDDIT_BOT_GDRIVE_API_CREDENTIALS")),f)

gc = pygsheets.authorize(service_file=join(dirname(__file__), 'gsheets_api-credentials.json'))

sht = gc.open_by_key(os.environ.get("QUOTES_REDDIT_BOT_SHEET_KEY"))
wks_users = sht.worksheet_by_title("users")

done_users = []
for number in range(1,100):
    done_user = wks_users.cell(f'A{number}').value
    if done_user == '':
        break
    done_users.append(done_user)

def invetation(related_subreddits):
    pk = 1
    for submission in reddit.subreddit(related_subreddits).new(limit=400):
        
        if pk == 5:
            break
        if str(submission.author) not in done_users:
            try:
                print(str(submission.author))
                pk += 1
                reddit.redditor(str(submission.author)).message(
                "the best quotes community", "I've invited you to join our community r/quotesandsayings__net", from_subreddit="quotesandsayings__net")
                done_users
                wks_users.cell(f'A{len(done_users)+1}').value = str(submission.author)
                done_users.append(str(submission.author))
            except:
                continue



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
    images = [
        {
            "image_path": image,
            "caption": "➡️Click Here To Read More Quotes!➡️➡️",
            "outbound_url": quote_link,
        },
        {
            "image_path": image,
            "caption": "➡️Click Here To Read More Quotes!➡️➡️",
            "outbound_url": quote_link,
        },
    ]
    submission = subreddit.submit_gallery(quote_text, images)
    submission.mod.approve()

number = random.randint(1,3)

if number == 1:
    create_card()
elif number == 2:
    create_card()
else:
    create_card()

#invetation("Showerthoughts+im14andthisisdeep+quotes+QuotesPorn+Stoicism+GetMotivated")
