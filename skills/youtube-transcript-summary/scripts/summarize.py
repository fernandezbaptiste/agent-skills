#!/usr/bin/env python3
"""
Fetch a YouTube transcript and extract what the main interviewee (Boris)
currently does that would be useful for engineers, using Claude.
"""

import argparse
import os
import re
import sys
from urllib.parse import parse_qs, urlparse


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from a YouTube URL or bare video ID."""
    # Bare 11-char video ID
    if re.match(r'^[A-Za-z0-9_-]{11}$', url_or_id):
        return url_or_id

    parsed = urlparse(url_or_id)

    # youtu.be short links
    if parsed.netloc in ('youtu.be', 'www.youtu.be'):
        vid = parsed.path.lstrip('/')
        # Strip any extra path segments
        return vid.split('/')[0]

    # youtube.com/watch?v=ID
    qs = parse_qs(parsed.query)
    if 'v' in qs:
        return qs['v'][0]

    # youtube.com/embed/ID or youtube.com/v/ID
    match = re.search(r'(?:embed|v)/([A-Za-z0-9_-]{11})', parsed.path)
    if match:
        return match.group(1)

    print(f"Error: Could not extract video ID from: {url_or_id}", file=sys.stderr)
    sys.exit(1)


def fetch_transcript(video_id: str) -> str:
    """Fetch and concatenate transcript text for a YouTube video."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print(
            "Error: youtube-transcript-api is not installed. "
            "Run: pip install -r requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    api = YouTubeTranscriptApi()
    try:
        # v1.x API: instance method, returns iterable of snippet objects
        fetched = api.fetch(video_id, languages=['en'])
    except Exception:
        try:
            # Fall back: try any available language
            transcript_list = api.list(video_id)
            fetched = transcript_list.find_generated_transcript(
                list(transcript_list._generated_transcripts.keys())
            ).fetch()
        except Exception as e:
            print(f"Error fetching transcript for video {video_id}: {e}", file=sys.stderr)
            sys.exit(1)

    return " ".join(snippet.text for snippet in fetched)


def get_api_key() -> str:
    """Get Anthropic API key from environment."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print(
            "Error: ANTHROPIC_API_KEY environment variable is not set.",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def analyze_transcript(transcript: str, api_key: str) -> str:
    """Send transcript to Claude and get bullet-point list of Boris's current practices."""
    try:
        import anthropic
    except ImportError:
        print(
            "Error: anthropic is not installed. Run: pip install -r requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = (
        "You are an expert at extracting actionable engineering practices from interview transcripts. "
        "Your task is to identify exactly what a specific person does RIGHT NOW in their current workflow — "
        "not what they used to do, not general advice, not hypotheticals. "
        "Output must be a clean bullet-point list, each point starting with a present-tense verb, "
        "written for a software engineer audience."
    )

    user_prompt = f"""Below is the full transcript of a YouTube interview.
The main interviewee is Boris.

Your job:
- Read the entire transcript carefully.
- Identify ONLY the things Boris personally does NOW, in his current day-to-day work.
- EXCLUDE: things he used to do, things he tried once, things he recommends others do but does not do himself,
  general tips not tied to his own current practice, historical anecdotes, things he stopped doing.
- INCLUDE: habits, tools, workflows, mental models, and techniques he explicitly states he currently uses.
- Format output as a clean bullet-point list. Each bullet should:
  - Start with a present-tense verb (e.g., "Uses...", "Runs...", "Keeps...", "Writes...")
  - Be concrete and specific — include tool names, numbers, or process details where mentioned
  - Be immediately useful to a software engineer

Do not include a preamble, introduction, or conclusion. Output only the bullet list.

TRANSCRIPT:
{transcript}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ],
    )

    return message.content[0].text


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Fetch a YouTube transcript and extract what the main interviewee (Boris) "
            "currently does that would be useful for engineers."
        )
    )
    parser.add_argument(
        "url",
        nargs="?",
        default="https://youtu.be/julbw1JuAz0",
        help="YouTube video URL or bare video ID (default: https://youtu.be/julbw1JuAz0)",
    )
    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    print(f"Fetching transcript for video: {video_id}", file=sys.stderr)

    transcript = fetch_transcript(video_id)
    print(f"Transcript fetched: {len(transcript)} characters", file=sys.stderr)

    api_key = get_api_key()
    print("Analyzing with Claude...", file=sys.stderr)

    result = analyze_transcript(transcript, api_key)
    print(result)


if __name__ == "__main__":
    main()
