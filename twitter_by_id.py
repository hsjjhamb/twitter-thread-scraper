import os
from dotenv import load_dotenv
import tweepy

load_dotenv()
BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")

if not BEARER_TOKEN:
    raise ValueError("TWITTER_BEARER_TOKEN environment variable not set. Please set it in your shell or .env file.")

client = tweepy.Client(bearer_token=BEARER_TOKEN)

def fetch_tweet(tweet_id):
    tweet = client.get_tweet(tweet_id, expansions="author_id", tweet_fields=["created_at", "text", "attachments"])
    print(tweet.data)
    if tweet.includes and "users" in tweet.includes:
        print("Author:", tweet.includes["users"][0].username)
    else:
        print("Author information not available.")

if __name__ == "__main__":
    # Replace with your desired tweet ID
    tweet_id = "1674822258647527424"
    fetch_tweet(tweet_id)
