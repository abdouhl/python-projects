import json
import random
import sys
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), '.env'))

access_token = os.environ.get("QUOTES_LINKEDIN_BOT_ACCESS_TOKEN")

api_url_base = 'https://api.linkedin.com/v2/'

URN= os.environ.get("QUOTES_LINKEDIN_BOT_URN")

headers = {'X-Restli-Protocol-Version': '2.0.0',
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'}


ch = random.choice(range(1,3))
if ch == 1:
    interies = os.listdir('resources/quotes/')
    all_author_quotes = []
    while all_author_quotes == [] :
        quote_file = random.choice(interies)
        print(quote_file)
        with open(f'resources/quotes/{quote_file}') as f:
            quote_file_content =  json.load(f)
        author_name = random.choice(list(quote_file_content.keys()))
        all_author_quotes = quote_file_content[author_name]
    author_quote = random.choice(all_author_quotes)
    print(author_name)
    print(author_quote)
    author_tag = author_name.lower()
    author_tag = author_tag.replace(' ','')
    author_tag = author_tag.replace('.','')
    author_tag = author_tag.replace('-','')
    author_tag = author_tag.replace("'",'')
    text = f'"{author_quote}" -- {author_name.title()}\n #{author_tag} #quotes #quotesandsayings #motivation #inspiration #sayings #quote #quoteoftheday'
else:
    with open('quotes_twiter_bot/quotes.json') as f:
        quotes = json.load(f)
         
    quote_link = random.choice(list(quotes.keys()))
    quote_text = quotes[quote_link][1]
    author_name = quotes[quote_link][0]
    users = api.search_users(author_name)
    auth_username = users[0].screen_name
    auth_tag = author_name.replace(' ','').lower()
    text = f'#{auth_tag} #quotes #quotesandsayings #motivation #inspiration #sayings #quote #quoteoftheday {quote_link}'
    

def post_on_linkedin():
    api_url = f'{api_url_base}ugcPosts'

    post_data = {
        "author": URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text":  text
                },
                "shareMediaCategory": "NONE"
            },
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        },
    }

    response = requests.post(api_url, headers=headers, json=post_data)

    if response.status_code == 201:
        print("Success")
        print(response.content)
    else:
        print(response.content)
post_on_linkedin()



