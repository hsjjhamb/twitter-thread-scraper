import tweepy

# Replace with your credentials
bearer_token = "YOUR_BEARER_TOKEN"

# Authenticate
client = tweepy.Client(bearer_token=bearer_token)

# Retrieve a tweet by its ID
tweet_id = "1674822258647527424"
tweet = client.get_tweet(tweet_id, expansions=["author_id"], tweet_fields=["created_at", "text"])

print("Tweet text:", tweet.data["text"])
print("Author ID:", tweet.includes["users"][0].id)
