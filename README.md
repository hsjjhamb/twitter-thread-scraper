# Twitter Thread Scraper

A Python toolkit for scraping Twitter/X threads and quote tweets using the official API via Tweepy.  
This project lets you extract complete threads (including nested replies) and quote tweets by the same author for selected tweets.  
It also saves thread structure as mindmap JSON files and downloads any images/media found in tweets.

---

## Features

- Fetch all replies (thread and nested replies) for selected tweets
- Find quote tweets by the same author referencing those tweets
- Save thread structure as mindmap JSON files
- Download images/media from tweets
- Modular scripts for single tweet, search, and thread/quote scraping

---

## Directory Structure

```
twitter-thread-scraper/
├── twitter_by_id.py        # Fetch a single tweet by ID
├── searchpy.py             # Search tweets by keyword/query
├── threadquotespy.py       # Scrape threads & quote tweets (core logic)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── images/                 # Saved images/media from tweets
├── mindmaps/               # Thread mindmap JSON files
├── data/                   # Saved thread/quote data JSON files
```

---

## Setup

1. **Clone this repository:**
   ```bash
   git clone https://github.com/YOURUSERNAME/twitter-thread-scraper.git
   cd twitter-thread-scraper
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get Twitter/X API credentials:**
   - Sign up at [Twitter Developer Portal](https://developer.twitter.com/)
   - Create a project and app
   - Obtain your Bearer Token (API v2)

4. **Set your Bearer Token:**
   - Edit the scripts (`threadquotespy.py`, etc.) and replace `"YOUR_BEARER_TOKEN"` with your token.

---

## Usage

### Scrape Threads and Quotes
```bash
python threadquotespy.py
```
- By default, script runs with example tweet IDs.
- Edit `selected_tweet_ids` in the script to choose your target tweets.

### Fetch a Single Tweet
```bash
python twitter_by_id.py
```

### Search Tweets
```bash
python searchpy.py
```
- Customize queries in each script as needed.

---

## Output

- **images/**: All images/media from tweets
- **mindmaps/**: JSON files representing thread structure for each tweet
- **data/**: JSON files with thread and quote tweet data

---

## Customization

- Change `selected_tweet_ids` in `threadquotespy.py` to scrape specific threads.
- Extend scripts for more features (output formats, user timeline, etc.).

---

## License

MIT License

---

## Contributing

Pull requests and suggestions welcome!  
Open an issue or PR if you'd like to help improve the toolkit.

---

## Credits

- [Tweepy](https://www.tweepy.org/) for Twitter API access
- Twitter/X for API services
