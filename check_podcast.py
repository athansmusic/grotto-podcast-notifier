import feedparser
import requests
import os

rss_feed_url = "https://feeds.acast.com/public/shows/thegrottopod"
discord_webhook_url = "https://discord.com/api/webhooks/1290158642968006746/MbqHBCLSOFuL2GxDBWEEArMAEvnDnBDCAxRQ7otf1UtTTujGUU4V2YuFJB-cRe1E1oNc"
last_posted_file = "last_posted.txt"

def get_last_posted_episode():
    if os.path.exists(last_posted_file):
        with open(last_posted_file, "r") as file:
            return file.read().strip()
    return None

def update_last_posted_episode(episode_link):
    with open(last_posted_file, "w") as file:
        file.write(episode_link)

def post_latest_episode():
    try:
        feed = feedparser.parse(rss_feed_url)
        if feed.entries:
            latest_episode = feed.entries[0]
            episode_title = latest_episode.title
            episode_link = latest_episode.link
            episode_image = latest_episode.image['href'] if 'image' in latest_episode else None

            last_posted_episode = get_last_posted_episode()

            if episode_link != last_posted_episode:
                embed = {
                    "title": f"🎙️ New Episode: {episode_title}",
                    "url": episode_link,
                    "color": 16776960,
                    "fields": [
                        {
                            "name": "Listen Now",
                            "value": f"[Click here to listen]({episode_link})"
                        }
                    ]
                }

                if episode_image:
                    embed["thumbnail"] = {"url": episode_image}

                payload = {"embeds": [embed]}
                response = requests.post(discord_webhook_url, json=payload)

                if response.status_code == 204:
                    print(f"Successfully posted new episode: {episode_title}")
                    update_last_posted_episode(episode_link)
                else:
                    print(f"Failed to post to Discord: {response.status_code}, {response.text}")
            else:
                print("No new episode to post.")
        else:
            print("No episodes found in the RSS feed.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

post_latest_episode()
