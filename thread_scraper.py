import os
from dotenv import load_dotenv
import tweepy
import requests
import json

load_dotenv()
BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")

if not BEARER_TOKEN:
    raise ValueError("TWITTER_BEARER_TOKEN environment variable not set. Please set it in your shell or .env file.")

client = tweepy.Client(bearer_token=BEARER_TOKEN)

def get_replies(tweet_id):
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
    mindmap = {}
    for tweet in tweets:
        parent = getattr(tweet, "in_reply_to_user_id", None)
        if parent:
            mindmap.setdefault(str(parent), []).append(str(tweet.id))
    path = os.path.join(folder, f"mindmap_{tweet_id}.json")
    with open(path, "w") as f:
        json.dump(mindmap, f, indent=2)
    return mindmap

def main(selected_tweet_ids):
    os.makedirs("images", exist_ok=True)
    os.makedirs("mindmaps", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    media_dict = {}
    for tweet_id in selected_tweet_ids:
        replies = get_replies(tweet_id)
        # Save images from replies
        if replies:
            for resp in replies:
                if resp.attachments:
                    for media_key in resp.attachments["media_keys"]:
                        media_dict[media_key] = resp
            save_images(replies, media_dict, folder="images")
        # Build and save mindmap
        build_mindmap(replies, tweet_id, folder="mindmaps")
        # Save thread data
        with open(f"data/threads_{tweet_id}.json", "w") as f:
            json.dump([t.data for t in replies], f, indent=2)

if __name__ == "__main__":
    # Example: Replace with your list of tweet IDs
    selected_tweet_ids = ["1674822258647527424"]
    main(selected_tweet_ids)
