"""Fetch and display recent top stories from Hacker News."""

import requests
import argparse
import tomllib
import re

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from pathlib import Path


BASE_URL = "https://hacker-news.firebaseio.com/v0"
CONFIG_PATH = Path("config.toml")


with CONFIG_PATH.open("rb") as file:
    config = tomllib.load(file)

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch and display top Hacker News stories"
    )

    parser.add_argument(
        "-n", "--num",
        type=int,
        default=config["filters"]["num_to_print"],
        help="Number of stories to print. Default comes from config.toml",
        metavar="",
    )

    parser.add_argument(
        "-fl", "--fetch-limit",
        type=int,
        default=config["filters"]["fetch_limit"],
        help="Number of top story IDs to fetch before filtering. Default comes from config.toml",
        metavar="",
    )

    parser.add_argument(
        "-d", "--days",
        type=int,
        default=config["filters"]["days_back"],
        help="Only show stories from the last number of days you choose. Default comes from config.toml",
        metavar="",
    )

    parser.add_argument(
        "-s", "--search",
        type=str,
        help="Only show stories with this word in the title",
        metavar="",
    )

    return parser.parse_args()

def get_greeting():
    """Return a greeting based on the configured timezone."""
    local_tz = ZoneInfo(config["user_timezone"]["timezone"])
    user_name = config["user_name"]["name"]
    current_hour = datetime.now(local_tz).hour

    # User greetings
    if current_hour < 12:
        return f"\nGood morning {user_name},"

    elif current_hour < 18:
        return f"\nGood afternoon {user_name},"

    else:
        return f"\nGood evening {user_name},"


def fetch_top_story_ids():
    """Fetch top story IDs from Hacker News."""
    response = requests.get(f"{BASE_URL}/topstories.json", timeout=10)
    response.raise_for_status()
    return response.json()

def fetch_story(story_id):
    """Fetch one story from Hacker News."""
    response = requests.get(f"{BASE_URL}/item/{story_id}.json", timeout=10)
    response.raise_for_status()
    return response.json()

def print_stories(stories, num_to_print):
    """Print selected stories to the terminal."""
    for i, story in enumerate(stories[:num_to_print], start=1):
        print(f"\n{i}.")
        print(f"Title: {story.get('title')}")
        print(f"Score: {story.get('score')}")
        print(f"Age: {format_age(story_time)}")
        print(f"By: {story.get('by')}")
        print(f"URL: {story.get('url')}")
        print("-" * 60)

def format_age(story_time):
    """Return a readable age string for a hacker News story."""
    now = datetime.now(timezone.utc)
    age = now - story_time

    days = age.days
    hours = age.seconds // 3600
    minutes = (age.seconds % 3600) // 60

    if days > 0:
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif hours > 0:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    return f"{minutes} minute{'s' if minutes != 1 else ''} ago"

def title_matches_search(title, search_term):
    """Return True if the title contains the search term as a whole word."""
    escaped_search = re.escape(search_term)
    whole_word_pattern = rf"\b{escaped_search}\b"

    return re.search(
        whole_word_pattern,
        title,
        re.IGNORECASE,
    ) is not None

args = parse_args()

greeting = get_greeting()

print(f"{greeting} please give me a few moments to fetch the top {args.num} stories from the past {args.days} days.\n")

num_to_print = args.num
fetch_limit = args.fetch_limit
days_back = args.days

# Create the cutoff time used to filter out older stories
cutoff_time = datetime.now(timezone.utc) - timedelta(days=days_back)

story_ids = fetch_top_story_ids()

stories = []

# Fetch and filter story details from the selected pool of top story IDs
for story_id in story_ids[:fetch_limit]:
    story = fetch_story(story_id)

    if "score" not in story or "time" not in story or not story.get("title"):
        continue

    story_time = datetime.fromtimestamp(story["time"], timezone.utc)

    if args.search and not title_matches_search(story["title"], args.search):
        continue

    if story_time >= cutoff_time:
        stories.append(story)

# Sort stories by score from highest to lowest
stories.sort(key=lambda story: story["score"], reverse=True)

print_stories(stories, num_to_print)