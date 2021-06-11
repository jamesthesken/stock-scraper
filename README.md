# stock-scraper

## Build
```
git clone https://github.com/jamesthesken/stock-scraper
cd stock-scraper/

# Initialize and activate the virtual env
python3 -m venv wsb-bets
source wsb-bets/bin/activate

# Install dependencies
pip install -r requirements.txt

```

## Config
Create a file named `config.py` in the top-level of the repository, which includes the credentials needed for the Reddit API: `client_id, client_secret, user_agent`.


## Running
The script pulls comments from /r/wallstreetbets, from posts in the last 7 days under the flair "Daily Discussion". Tickers mentioned are counted, plotted, and saved using matplotlib.

