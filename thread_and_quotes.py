import os
from dotenv import load_dotenv
import tweepy
import requests
import json
from collections import defaultdict

# Load environment variables from .env if present
load_dotenv()
BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")

if not BEARER_TOKEN:
    raise ValueError("TWITTER_BEARER_TOKEN environment variable not set. Please set it in your shell or .env file.")

client = tweepy.Client(bearer_token=BEARER_TOKEN)

def get_author(tweet_id):
    tweet = client.get_tweet(tweet_id, expansions="author_id")
    return tweet.includes["users"][0].id

def get_replies(tweet_id, author_id):
    replies = []
    query = f"conversation_id:{tweet_id}"
    paginator = tweepy.Paginator(
        client.search_recent_tweets,
        query=query,
        tweet_fields=["in_reply_to_user_id", "conversation_id", "author_id", "attachments", "text"],
        expansions=["attachments.media_keys"],
        media_fields=["url", "preview_image_url"],
        max_results=100
    )
    for response in paginator:
        if response.data:
            replies.extend(response.data)
    return replies

def get_quote_tweets(tweet_id, author_id):
    query = f"url:twitter.com/i/web/status/{tweet_id} from:{author_id} is:quote"
    quotes = []
    paginator = tweepy.Paginator(
        client.search_recent_tweets,
        query=query,
        tweet_fields=["author_id", "attachments", "text"],
        expansions=["attachments.media_keys"],
        media_fields=["url", "preview_image_url"],
        max_results=100
    )
    for response in paginator:
        if response.data:
            quotes.extend(response.data)
    return quotes

def save_images(tweets, media_dict, folder="images"):
    os.makedirs(folder, exist_ok=True)
    for tweet in tweets:
        if hasattr(tweet, "attachments") and tweet.attachments:
            for media_key in tweet.attachments["media_keys"]:
                media = media_dict.get(media_key)
                if media and "url" in media.data:
                    url = media.data["url"]
                    filename = os.path.join(folder, f"{tweet.id}_{media_key}.jpg")
                    try:
                        img = requests.get(url)
                        with open(filename, "wb") as f:
                            f.write(img.content)
                    except Exception as e:
                        print(f"Failed to download {url}: {e}")

def build_mindmap(tweets, tweet_id, folder="mindmaps"):
    os.makedirs(folder, exist_ok=True)
    mindmap = defaultdict(list)
    for tweet in tweets:
        if hasattr(tweet, "in_reply_to_user_id") and tweet.in_reply_to_user_id:
            mindmap[str(tweet.in_reply_to_user_id)].append(str(tweet.id))
    path = os.path.join(folder, f"mindmap_{tweet_id}.json")
    with open(path, "w") as f:
        json.dump(mindmap, f, indent=2)
    return mindmap

def main(selected_tweet_ids):
    os.makedirs("images", exist_ok=True)
    os.makedirs("mindmaps", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    all_threads = {}
    all_quotes = {}
    media_dict = {}
    for tweet_id in selected_tweet_ids:
        author_id = get_author(tweet_id)
        replies = get_replies(tweet_id, author_id)
        quotes = get_quote_tweets(tweet_id, author_id)
        # Save images from replies and quotes
        if replies:
            for resp in replies:
                if resp.attachments:
                    for media_key in resp.attachments["media_keys"]:
                        media_dict[media_key] = resp
            save_images(replies, media_dict, folder="images")
        if quotes:
            for resp in quotes:
                if resp.attachments:
                    for media_key in resp.attachments["media_keys"]:
                        media_dict[media_key] = resp
            save_images(quotes, media_dict, folder="images")
        # Build and save mindmap
        build_mindmap(replies, tweet_id, folder="mindmaps")
        all_threads[tweet_id] = [t.data for t in replies]
        all_quotes[tweet_id] = [q.data for q in quotes]
        # Save thread and quotes data
        with open(f"data/threads_{tweet_id}.json", "w") as f:
            json.dump([t.data for t in replies], f, indent=2)
        with open(f"data/quotes_{tweet_id}.json", "w") as f:
            json.dump([q.data for q in quotes], f, indent=2)
    # Optionally save all data together
    with open("data/all_threads.json", "w") as f:
        json.dump(all_threads, f, indent=2)
    with open("data/all_quotes.json", "w") as f:
        json.dump(all_quotes, f, indent=2)

if __name__ == "__main__":
    # Example: Replace with your list of tweet IDs
    selected_tweet_ids = ["1674822258647527424"]
    main(selected_tweet_ids)
