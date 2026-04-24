import requests
import time

# Base endpoint for the Hacker News public API
base_url = "https://hacker-news.firebaseio.com/v0"

# Number of stories to display
num_to_print = 10

# Number of topstories IDs to inspect
fetch_limit = 50

# Number of days back to look
days_back = 5

# Unix timestamp for 5 days ago
cutoff_time = int(time.time()) - (days_back * 24 * 60 * 60)

# Fetch current top story IDs from Hacker News
story_ids = requests.get(f"{base_url}/topstories.json", timeout=10).json()

# Store stories from the last 5 days that have a score
stories = []

for story_id in story_ids[:fetch_limit]:
    story = requests.get(f"{base_url}/item/{story_id}.json", timeout=10).json()

    # Keep only stories with a score and a timestamp within the last 5 days
    if "score" in story and story.get("time", 0) >= cutoff_time:
        stories.append(story)

# Sort all matching stories by score, highest first
stories.sort(key=lambda story: story["score"], reverse=True)

# Print only the top 10 highest-scoring stories
for i, story in enumerate(stories[:num_to_print], start=1):
    print(f"{i}.")
    print(f"Title: {story.get('title')}")
    print(f"Score: {story.get('score')}")
    print(f"By: {story.get('by')}")
    print(f"URL: {story.get('url')}")
    
    print("-" * 60)