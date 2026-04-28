import requests
from datetime import datetime, timedelta, timezone

base_url = "https://hacker-news.firebaseio.com/v0"

num_to_print = 10
fetch_limit = 50
days_back = 5

# Create the cutoff time used to filter out older stories
cutoff_time = datetime.now(timezone.utc) - timedelta(days=days_back)

story_ids = requests.get(f"{base_url}/topstories.json", timeout=10).json()

stories = []

# Fetch story details from the selected pool of top story IDs
for story_id in story_ids[:fetch_limit]:
    story = requests.get(f"{base_url}/item/{story_id}.json", timeout=10).json()

    if "score" not in story or "time" not in story or not story.get("title"):
        continue

    story_time = datetime.fromtimestamp(story["time"], timezone.utc)

    if story_time >= cutoff_time:
        stories.append(story)

# Sort stories by score from highest to lowest
stories.sort(key=lambda story: story["score"], reverse=True)

for i, story in enumerate(stories[:num_to_print], start=1):
    print(f"{i}.")
    print(f"Title: {story.get('title')}")
    print(f"Score: {story.get('score')}")
    print(f"By: {story.get('by')}")
    print(f"URL: {story.get('url')}")
    print("-" * 60)