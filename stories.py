import requests
import time
import argparse

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

# Parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch and display top Hacker News stories"
    )

    parser.add_argument(
        "--num",
        type=int,
        default=10,
        help="Number of stories to print. Default: 10",
    )

    parser.add_argument(
        "--fetch-limit",
        type=int,
        default=50,
        help="Number of top story IDs to fetch before filtering. Default: 50",
    )

    parser.add_argument(
        "--days",
        type=int,
        default=5,
        help="Only show stories from the last number of days you choose. Default:5",
    )

    return parser.parse_args()

args = parse_args()


# Be sure to use your timezone for accurate user greetings
local_tz = ZoneInfo("America/Los_Angeles")

now = datetime.now(local_tz)
current_hour = now.hour

# User greetings
if current_hour < 12:
    greeting = "\nGood morning, user"

elif current_hour < 18:
    greeting = "\nGood afternoon, user"

else:
    greeting = "\nGood evening, user"

print(f"{greeting}, please give me a few moments to fetch the top stories.\n")

time.sleep(1)

print("Use python3 stories.py --help to view command-line options for changing the filters.")

base_url = "https://hacker-news.firebaseio.com/v0"

num_to_print = args.num
fetch_limit = args.fetch_limit
days_back = args.days

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
    print(f"\n{i}.")
    print(f"Title: {story.get('title')}")
    print(f"Score: {story.get('score')}")
    print(f"By: {story.get('by')}")
    print(f"URL: {story.get('url')}")
    print("-" * 60)