import config
import praw
from praw.models import MoreComments
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy import create_engine

# Creates a set of stock tickers in NASDAQ
def nasdaq_tickers():
    fin = open("nasdaqtraded.txt", 'r')
    tickers = set()
    fin.readline()
    for line in fin.readlines():
        line = line[2:]
        tickers.add(line[:line.index("|")])
    return tickers

# Search wsb top level comments given a flair and time interval (week, day, hour, etc.). 
# Returns: 
# results - dictionary containing ticker and amount of times it was mentioned in the time interval.
# ticker_info - list of dictionaries containing ticker name and sentiment. used later in a Pandas dataframe for agg. functions
def searchFlairs(flair, time):
    reddit = praw.Reddit(client_id = config.client_id, client_secret = config.client_secret, user_agent = config.user_agent)
    counter = 0
    flagged_words = ["YOLO", "PUMP", "RH", "EOD", "IPO", "ATH", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", 
        "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    ticker_set = nasdaq_tickers()
    tickers = {}

    ticker_info = []

    analyzer = SentimentIntensityAnalyzer()

    for submission in reddit.subreddit('wallstreetbets').search('flair:"%s"'%(flair), sort='new', time_filter='%s'%(time)):
        print(submission.title)
        for top_level_comment in submission.comments:
            ticker_sentiment = {}
            if isinstance(top_level_comment, MoreComments):
                continue 
            for word in top_level_comment.body.split():
                if word == word.upper() and word in ticker_set and word not in flagged_words:
                    vs = analyzer.polarity_scores(top_level_comment.body)
                    ticker_sentiment['ticker'] = word
                    ticker_sentiment['sent'] = vs['compound']
                    ticker_sentiment['ts'] = top_level_comment.created_utc
                    ticker_info.append(ticker_sentiment)
                    if word not in tickers:
                        tickers[word] = 1
                    else:
                        tickers[word] += 1
    return tickers, ticker_info

# Plotting the tickers on a pie chart
def popularTickers():
    #result = ticker_count()
    result, ticker_info = searchFlairs('Daily Discussion', 'week')
    x = []
    y = []
    for a, b in result.items():
        # Can change value to see choose the threshold stock mention count 
        if b > 5:
            x.append(a)
            y.append(b)
    # Uncomment to see a pie chart 
    fig1, ax1 = plt.subplots()
    ax1.pie(y, labels=x, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()
    plt.savefig('mygraph1.png')
    return x, y

# TODO: Don't replace the table if it exists, should be smart enough to handle duplicates
def wsbPostgres(df):
    engine = create_engine('postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_server}'.format(
        db_user=config.db_user, db_pass=config.password, db_host=config.db_host, db_server=config.db_name
    ))
    df.to_sql('wsb-test', engine, method='multi', if_exists='replace')


results, ticker_info = searchFlairs('Daily Discussion', 'day')

# Calculate the average compound sentiment for the mentioned ticker comment: https://github.com/cjhutto/vaderSentiment#python-demo-and-code-examples
df = pd.DataFrame(ticker_info)
print(df)
df_new = df.groupby(df['ticker'])['sent'].agg(['mean'])

wsbPostgres(df_new)

print(df_new)