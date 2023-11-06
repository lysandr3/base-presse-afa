import feedparser
from datetime import datetime
import time
import pandas as pd

def update_database():
    feed = feedparser.parse('https://www.theguardian.com/europe/rss')
    date = datetime.strptime(feed.feed.published[5:-4],"%d %b %Y %H:%M:%S")

    with open('date.txt', 'w') as file:
        file.write(feed.feed.published[5:-4])

    with open('date.txt','r') as file:
        old_date = datetime.strptime(file.read(),"%d %b %Y %H:%M:%S")

    n = 0 
    while n < len(feed.entries) and datetime.fromtimestamp(time.mktime(feed.entries[n].updated_parsed)) > old_date:
        n += 1

    df_to_append = pd.DataFrame(
        {
            'Title': [entry.title for entry in feed.entries[:n]],
            'Link' : [entry.link for entry in feed.entries[:n]],
            'Description' : [entry.summary for entry in feed.entries[:n]],
            'Date' : [datetime.fromtimestamp(time.mktime(entry.updated_parsed)) for entry in feed.entries[:n]]
        }).sort_values('Date',ascending=False)

    pd.concat([df_to_append,pd.read_csv('database.csv')]).to_csv('database.csv',index=False)





