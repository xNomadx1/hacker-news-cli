import requests

# Base endpoint for the Hacker News public API
BASE_URL = "https://hacker-news.firebaseio.com/v0"

# Fetch a list of IDs for the current top stories
# This returns a list like: [id1, id2, id3, ...]
story_ids = requests.get(f"{BASE_URL}/topstories.json", timeout=10).json()

# Loop through the first 10 story IDs and enumerate them (1–10)
# This is where you can change the amount of articles pulled
for i, story_id in enumerate(story_ids[:10], start=1):
    
    # Fetch full details for each story using its ID
    # Endpoint: /item/<story_id>.json
    story = requests.get(f"{BASE_URL}/item/{story_id}.json").json()
    
    # Print formatted story information
    # .get() is used to avoid crashes if a key is missing
    print(f"\n{i}. {story.get('title')}")
    print(f"Score: {story.get('score')}")   # Number of upvotes
    print(f"By: {story.get('by')}")         # Author username
    print(f"URL: {story.get('url')}")       # External link (may be None)

    print("-" * 60)