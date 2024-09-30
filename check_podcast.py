import feedparser
import requests
import os

# Your podcast RSS feed URL
rss_feed_url = "https://shows.acast.com/thegrottopod/episodes.rss"

# Discord webhook URL from environment variable
discord_webhook_url = os.getenv("https://discord.com/api/webhooks/1290158642968006746/MbqHBCLSOFuL2GxDBWEEArMAEvnDnBDCAxRQ7otf1UtTTujGUU4V2YuFJB-cRe1E1oNc")

# Store the last published episode link to avoid duplicates
last_episode_url = None

def check_for_new_episode():
    global last_episode_url
    feed = feedparser.parse(rss_feed_url)
    
    if feed.entries:
        # Get the latest episode from the RSS feed
        latest_episode = feed.entries[0]
        episode_title = latest_episode.title
        episode_link = latest_episode.link
        episode_description = latest_episode.description

        # Check if this is a new episode (not the last one we posted about)
        if episode_link != last_episode_url:
            # Send a message to Discord via webhook
            data = {
                "content": f"New episode of THE GROTTO is now live: click here to listen to {episode_title}. {episode_description} \n{episode_link}"
            }
            requests.post(discord_webhook_url, json=data)
            
            # Update the last_episode_url to avoid duplicate posts
            last_episode_url = episode_link
            print(f"Posted new episode: {episode_title}")
        else:
            print("No new episode.")

# Run the check once (GitHub Actions will schedule the script)
check_for_new_episode()
