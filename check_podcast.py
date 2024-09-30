import feedparser
import requests
import os

# Your podcast RSS feed URL
rss_feed_url = "https://shows.acast.com/thegrottopod/episodes.rss"

# Discord webhook URL from environment variable
discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

def post_latest_episode():
    feed = feedparser.parse(rss_feed_url)
    
    if feed.entries:
        # Get the latest episode from the RSS feed
        latest_episode = feed.entries[0]
        episode_title = latest_episode.title
        episode_link = latest_episode.link
        episode_description = latest_episode.description

        # Send a message to Discord via webhook, even if it's not a new episode
        data = {
            "content": f"New episode of THE GROTTO is now live: click here to listen to {episode_title}. {episode_description} \n{episode_link}"
        }
        response = requests.post(discord_webhook_url, json=data)
        
        if response.status_code == 204:
            print(f"Successfully posted new episode: {episode_title}")
        else:
            print(f"Failed to post to Discord: {response.status_code}, {response.text}")

# Run the check once (for testing)
post_latest_episode()
