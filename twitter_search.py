import os
from dotenv import load_dotenv
import tweepy

load_dotenv()
BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")

if not BEARER_TOKEN:
    raise ValueError("TWITTER_BEARER_TOKEN environment variable not set. Please set it in your shell or .env file.")

client = tweepy.Client(bearer_token=BEARER_TOKEN)

def search_tweets(query, max_results=10):
    response = client.search_recent_tweets(query=query, tweet_fields=["created_at", "text", "author_id"], max_results=max_results)
    if response.data:
        for tweet in response.data:
            print(f"Tweet ID: {tweet.id}")
            print(f"Author ID: {tweet.author_id}")
            print(f"Created At: {tweet.created_at}")
            print(f"Text: {tweet.text}")
            print("-" * 40)
    else:
        print("No tweets found for this query.")

if __name__ == "__main__":
    # Example query
    search_query = "OpenAI"
    search_tweets(search_query, max_results=5)
