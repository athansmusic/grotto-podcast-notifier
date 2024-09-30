import feedparser
import requests
import os

rss_feed_url = "https://feeds.acast.com/public/shows/thegrottopod"

discord_webhook_url = "https://discord.com/api/webhooks/1290158642968006746/MbqHBCLSOFuL2GxDBWEEArMAEvnDnBDCAxRQ7otf1UtTTujGUU4V2YuFJB-cRe1E1oNc"

def strip_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def post_latest_episode():
    try:
        print("Fetching RSS feed...")
        feed = feedparser.parse(rss_feed_url)
        
        if feed.entries:
            # Get the latest episode from the RSS feed
            latest_episode = feed.entries[0]
            episode_title = latest_episode.title
            episode_link = latest_episode.link
            episode_description = strip_html_tags(latest_episode.description)  # Strip HTML tags

            print(f"Latest episode found: {episode_title}")
            print(f"Episode link: {episode_link}")
            print(f"Episode description: {episode_description}")

            # Send a nicely formatted embed message to Discord via webhook
            embed = {
                "title": f"🎙️ New Episode: {episode_title}",
                "description": episode_description[:200] + "..." if len(episode_description) > 200 else episode_description,  # Truncate if too long
                "url": episode_link,
                "color": 16776960,  # Yellow color in decimal
                "fields": [
                    {
                        "name": "Listen Now",
                        "value": f"[Click here to listen to the episode]({episode_link})"
                    }
                ]
            }
            payload = {
                "embeds": [embed]
            }

            print(f"Posting to Discord via webhook: {discord_webhook_url}")
            response = requests.post(discord_webhook_url, json=payload)

            # Print the response for debugging
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

# Run the check once (for testing)
post_latest_episode()
