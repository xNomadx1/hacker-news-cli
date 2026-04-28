# Hacker News CLI

Simple Python script that fetches and displays the top 10 stories from Hacker News. 

## What it does
- Fetches stories from the Hacker News API from a 50-story pool over the last 5 days, 
then sorts them by score and prints the top 10.
- Displays:
  - Title
  - Score
  - Author
  - URL

## Limitations
- Minimal implementation: does not include retries or advanced error handling
- Designed as a lightweight example using the Hacker News public API

## Requirements
- Python 3.8+
- pip

## Setup

Create and activate a virtual environment:

    python3 -m venv .venv_stories
    source .venv_stories/bin/activate

Install dependencies:

    pip install -r requirements.txt

## Run

    python3 stories.py