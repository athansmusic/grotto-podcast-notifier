import feedparser
import requests
import os

rss_feed_url = "https://shows.acast.com/thegrottopod/episodes.rss"

discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

def post_latest_episode():
    feed = feedparser.parse(rss_feed_url)
    
    if feed.entries:
        latest_episode = feed.entries[0]
        episode_title = latest_episode.title
        episode_link = latest_episode.link
        episode_description = latest_episode.description

        data = {
            "content": f"New episode of THE GROTTO is now live: click here to listen to {episode_title}. {episode_description} \n{episode_link}"
        }

        response = requests.post(discord_webhook_url, json=data)

        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")

        if response.status_code == 204:
            print(f"Successfully posted new episode: {episode_title}")
        else:
            print(f"Failed to post to Discord: {response.status_code}, {response.text}")

post_latest_episode()
