import tweepy

bearer_token = "YOUR_BEARER_TOKEN"
client = tweepy.Client(bearer_token)

def get_author(tweet_id):
    tweet = client.get_tweet(tweet_id, expansions="author_id")
    return tweet.includes["users"][0].id

def get_nested_replies(tweet_id, author_id):
    replies = []
    # Search for replies to this tweet
    query = f"conversation_id:{tweet_id} to:{author_id}"
    for tweet in client.search_recent_tweets(query=query, tweet_fields=["in_reply_to_user_id", "conversation_id", "author_id", "text"], max_results=100).data or []:
        replies.append(tweet)
        # Recursively fetch replies to replies
        replies.extend(get_nested_replies(tweet.id, author_id))
    return replies

def get_quote_tweets(tweet_id, author_id):
    # Search for quote tweets by the same author
    query = f"url:twitter.com/i/web/status/{tweet_id} from:{author_id}"
    return client.search_recent_tweets(query=query, tweet_fields=["author_id", "text"], max_results=100).data or []

def main(selected_tweet_ids):
    all_threads = []
    all_quotes = []
    for tweet_id in selected_tweet_ids:
        author_id = get_author(tweet_id)
        # Fetch nested threads
        threads = get_nested_replies(tweet_id, author_id)
        all_threads.extend(threads)
        # Fetch quote tweets by author
        quotes = get_quote_tweets(tweet_id, author_id)
        all_quotes.extend(quotes)
    return all_threads, all_quotes

# Example usage
selected_tweet_ids = ["1674822258647527424"]
threads, quotes = main(selected_tweet_ids)
print("Threads:")
for t in threads:
    print(t.text)
print("Quote Tweets:")
for q in quotes:
    print(q.text)