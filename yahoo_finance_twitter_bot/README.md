# yahoo finance twitter bot

1. Download the folder:
```
svn checkout https://github.com/abdouhl/python-projects/trunk/yahoo_finance_twitter_bot
cd yahoo_finance_twitter_bot
```
2. Set up your virtualenv.
```
python3 -m venv ./venv/api
. ./venv/api/bin/activate
pip install -r requirements.txt
```
3. Edit virtualenv variables
```
cp .env.example .env
```
open the .env file and Edit add your twitter api keys

4. Run the script
```
python3 main.py
```
