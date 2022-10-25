import json
import random
import sys
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
import urllib.request


load_dotenv(join(dirname(__file__), '.env'))

access_token = os.environ.get("QUOTES_LINKEDIN_BOT_ACCESS_TOKEN")

api_url_base = 'https://api.linkedin.com/v2/'

URN= os.environ.get("QUOTES_LINKEDIN_BOT_URN")

headers = {'X-Restli-Protocol-Version': '2.0.0',
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'}


ch = random.choice(range(2,3))
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
else:
    with open('quotes_twiter_bot/quotes.json') as f:
        quotes = json.load(f)
         
    quote_link = random.choice(list(quotes.keys()))
    quote_text = quotes[quote_link][1]
    author_name = quotes[quote_link][0]
    auth_tag = author_name.replace(' ','').lower()
    text_tags = f'#{auth_tag} #quotes #quotesandsayings #motivation #inspiration #sayings #quote #quoteoftheday'
    
    api_url = 'https://api.linkedin.com/v2/assets?action=registerUpload'
    
    post_data = {
       "registerUploadRequest":{
          "owner":URN,
          "recipes":[
             "urn:li:digitalmediaRecipe:feedshare-image"
          ],
          "serviceRelationships":[
             {
                "identifier":"urn:li:userGeneratedContent",
                "relationshipType":"OWNER"
             }
          ],
          "supportedUploadMechanism":[
             "SYNCHRONOUS_UPLOAD"
          ]
       }
    }
    
    response = requests.post(api_url, headers=headers, json=post_data)
    
    uploadurl = response.json()['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    # "urn:li:image:C4D22AQEWUEuVbYrmAg"  "urn:li:digitalmediaAsset:C5522AQHn46pwH96hxQ"
    imageurn = response.json()['value']['asset'].replace('digitalmediaAsset','image')
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    # setting filename and image URL 
    filename =  join(dirname(__file__),'og_card_image.jpg')
    product_img_url = quote_link + 'og_card_image.jpg'

    # calling urlretrieve function to get resource
    urllib.request.urlretrieve(product_img_url, filename)

    os.system(f'''curl -i --upload-file {join(dirname(__file__),'og_card_image.jpg')} -H 'Authorization: Bearer {access_token}' "{uploadurl}"''')
    
    api_url = 'https://api.linkedin.com/v2/posts'

    post_data = {
      "author": URN,
      "commentary": text_tags,
      "content": {
            "article": {
                "title": quote_text,
                "source": quote_link,
                "thumbnail": imageurn
            }
        },
      "contentLandingPage":quote_link,
       "visibility": "PUBLIC",
       "distribution": {
           "feedDistribution": "MAIN_FEED",
           "targetEntities": [],
           "thirdPartyDistributionChannels": []
       },
       "lifecycleState": "PUBLISHED",
       "isReshareDisabledByAuthor": False
    }

    response = requests.post(api_url, headers=headers, json=post_data)

    if response.status_code == 201:
        print("Success")
        print(response.content)
    else:
        print(response.content)



