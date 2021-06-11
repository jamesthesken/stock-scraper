import config
import praw
from praw.models import MoreComments
import pandas as pd
import matplotlib.pyplot as plt

# Creates a set of stock tickers in NASDAQ
def nasdaq_tickers():
    fin = open("nasdaqtraded.txt", 'r')
    tickers = set()
    fin.readline()
    for line in fin.readlines():
        line = line[2:]
        tickers.add(line[:line.index("|")])
    return tickers

def searchFlairs(flair):
    reddit = praw.Reddit(client_id = config.client_id, client_secret = config.client_secret, user_agent = config.user_agent)
    counter = 0
    flagged_words = ["YOLO", "PUMP", "RH", "EOD", "IPO", "ATH", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", 
        "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    ticker_set = nasdaq_tickers()
    tickers = {}
    for submission in reddit.subreddit('wallstreetbets').search('flair:"%s"'%(flair), sort='new', time_filter='week'):
        print(submission.title)
        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, MoreComments):
                continue 
            for word in top_level_comment.body.split():
                if word == word.upper() and word in ticker_set and word not in flagged_words:
                    if word not in tickers:
                        tickers[word] = 1
                    else:
                        tickers[word] += 1
    return tickers

def popularTickers():
    #result = ticker_count()
    result = searchFlairs('Daily Discussion')
    x = []
    y = []
    for a, b in result.items():
        # Can change value to see choose the threshold stock mention count 
        if b > 5:
            x.append(a)
            y.append(b)
    # Uncomment to see a pie graph 
    fig1, ax1 = plt.subplots()
    ax1.pie(y, labels=x, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()
    plt.savefig('mygraph1.png')
    return x, y

#searchFlairs('Daily Discussion')

popularTickers()
