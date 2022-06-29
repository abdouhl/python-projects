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
def post_on_linkedin():
    api_url = f'{api_url_base}ugcPosts'

    post_data = {
        "author": URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text":  f'"{author_quote}" -- {author_name.title()}\n #{author_tag} #quotes #quotesandsayings #motivation #inspiration #sayings #quote #quoteoftheday'
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



