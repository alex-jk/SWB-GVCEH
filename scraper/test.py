import datetime
import os
import pickle
import os.path
import time
import model  # gvceh functions
import cleaner  # gvceh functions
import tweepy as tw
import pandas as pd
import io
import requests

from github import Github
from transformers import pipeline

from pprint import pprint
import dotenv



USERNAME = os.environ["USERNAME"]  # for github api
TOKEN = os.environ["TOKEN"]  # for github api

# open github api connection
g = Github(USERNAME, TOKEN)
user = g.get_user(USERNAME)
repo = user.get_repo("SWB-GVCEH")


print("READING CSV FROM GITHUB")

consolidated_file_path = f"https://raw.githubusercontent.com/sheilaflood/SWB-GVCEH/main/data/processed/twitter/GVCEH-tweets-combined.csv"
r=requests.get(consolidated_file_path).content

df_old=pd.read_csv(io.StringIO(r.decode('utf-8')))
print('Original CSV: ', df_old.shape)

df_old = df_old[["text", "scrape_time", "tweet_id", "created_at", "reply_count", "quote_count",
                    "like_count", "retweet_count", "geo_full_name", "geo_id", "username", "num_followers",
                    "search_keywords", "search_neighbourhood", "sentiment", "score"]]
    

df_csv = df_old.to_csv()


repo.create_file(path = '/data/processed/twitter/GVCEH-tweets-combined.csv', message = "Adding new tweets", branch="main", content = df_csv)
print("Done with scraper.py!!!")
