# stock-scraper🚀

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

Create a file named `.env` in the top-level of the repsitory to include variables used by Docker-Compose, for example:
```
PGUSER=postgres
PGHOST=postgres
PGDATABASE=postgres
PGPASSWORD=postgres
PGPORT=5432
```

## Running the scraper
The script pulls comments from /r/wallstreetbets, from posts in the last 7 days under the flair "Daily Discussion". Tickers mentioned are counted, plotted, and saved using matplotlib.

```
python3 wsb_scraper.py
```
## Running the user interface
The front-end is built using ReactJS, and is served through Docker-Compose. This also includes the Postgres database and API written in ExpressJS.

```
docker-compose up --build
```

## Thank you
The backbone of this code was adopted from a repository by user [brian654321](https://github.com/brian654321/wall-street-bets-index)
```
Vader Sentiment Analysis
Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
```