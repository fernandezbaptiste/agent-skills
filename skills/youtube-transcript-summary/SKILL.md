---
name: youtube-transcript-summary
description: >
  Fetch a YouTube video transcript and extract what the main interviewee currently
  does NOW using Claude. Use when you have a YouTube interview URL and want a
  bullet-point list of current, actionable habits or workflows from the speaker.
  Keywords: YouTube, transcript, interview, tips, summarize, extract, engineer,
  Boris, practices, tools.
---

# YouTube Transcript Summary

Fetches a YouTube transcript and uses Claude to extract a bullet-point list of
what the main interviewee currently does in their workflow — filtering out past
practices and generic advice.

## Setup

```bash
cd skills/youtube-transcript-summary
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

```bash
# Default video (https://youtu.be/julbw1JuAz0)
python3 scripts/summarize.py

# Custom video URL
python3 scripts/summarize.py https://youtu.be/<video-id>

# Pipe output to a file
python3 scripts/summarize.py https://youtu.be/<video-id> > tips.md
```

## Output

A bullet-point list of things the main interviewee currently does, each starting
with a present-tense verb, written for a software engineer audience.

## What it filters out

- Past practices ("I used to...", "Back then...")
- Generic advice not tied to the speaker's own current workflow
- Historical anecdotes
- Things the speaker tried once but stopped doing
