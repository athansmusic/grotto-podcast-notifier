import feedparser
import requests
import os

rss_feed_url = "https://feeds.acast.com/public/shows/thegrottopod"

discord_webhook_url = "https://discord.com/api/webhooks/1290158642968006746/MbqHBCLSOFuL2GxDBWEEArMAEvnDnBDCAxRQ7otf1UtTTujGUU4V2YuFJB-cRe1E1oNc"

def post_latest_episode():
    try:
        print("Fetching RSS feed...")
        feed = feedparser.parse(rss_feed_url)
        
        if feed.entries:
            latest_episode = feed.entries[0]
            episode_title = latest_episode.title
            episode_link = latest_episode.link
            episode_description = latest_episode.description

            print(f"Latest episode found: {episode_title}")
            print(f"Episode link: {episode_link}")
            print(f"Episode description: {episode_description}")

            data = {
                "content": f"New episode of THE GROTTO is now live: click here to listen to {episode_title}. \n{episode_link}"
            }
            print(f"Posting to Discord via webhook: {discord_webhook_url}")
            response = requests.post(discord_webhook_url, json=data)

            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")

            if response.status_code == 204:
                print(f"Successfully posted new episode: {episode_title}")
            else:
                print(f"Failed to post to Discord: {response.status_code}, {response.text}")
        else:
            print("No episodes found in the RSS feed.")

    except Exception as e:
        print(f"Error occurred: {str(e)}")

post_latest_episode()
