import tweepy

bearer_token = "YOUR_BEARER_TOKEN"

client = tweepy.Client(bearer_token=bearer_token)

# Search for recent tweets containing "python"
for tweet in client.search_recent_tweets(query="python", max_results=10, tweet_fields=["created_at", "author_id", "text"]).data:
    print(tweet.created_at, tweet.author_id, tweet.text)