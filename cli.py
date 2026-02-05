"""
Simple command-line UI (CLI) for the AI-Generated Voice Detection API.

Examples:
  python cli.py health
  python cli.py detect sample.mp3 Tamil

Notes:
  - API key is required for detect. Set it via .env (API_KEY=...), env var, or --api-key.
  - Default API URL: http://localhost:8000
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from typing import Any

import requests
from dotenv import load_dotenv


DEFAULT_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")


def _load_env(env_file: str | None) -> None:
    # Load .env if present (or user-specified)
    if env_file:
        load_dotenv(env_file)
    else:
        load_dotenv()


def _b64encode_file(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _pretty_print(obj: Any) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def cmd_health(base_url: str) -> int:
    url = f"{base_url}/health"
    try:
        r = requests.get(url, timeout=20)
        print(f"GET {url} -> {r.status_code}")
        _pretty_print(r.json())
        return 0 if r.ok else 1
    except requests.exceptions.ConnectionError:
        print("Error: could not connect to the API. Start it with: python run.py", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


def cmd_detect(base_url: str, api_key: str, audio_path: str, language: str) -> int:
    url = f"{base_url}/api/voice-detection"
    payload = {
        "language": language,
        "audioFormat": "mp3",
        "audioBase64": _b64encode_file(audio_path),
    }
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=120)
        print(f"POST {url} -> {r.status_code}")
        data = r.json()
        _pretty_print(data)

        if r.ok and data.get("status") == "success":
            return 0
        return 1
    except FileNotFoundError:
        print(f"Error: audio file not found: {audio_path}", file=sys.stderr)
        return 2
    except requests.exceptions.ConnectionError:
        print("Error: could not connect to the API. Start it with: python run.py", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cli.py",
        description="CLI for the AI-Generated Voice Detection API (health + voice check).",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="API base URL (default: http://localhost:8000). You can also set API_BASE_URL env var.",
    )
    parser.add_argument(
        "--env-file",
        default=None,
        help="Path to a .env file to load (default: auto-load .env in project root if present).",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_health = sub.add_parser("health", help="Check API health (GET /health).")
    p_health.set_defaults(_handler="health")

    p_detect = sub.add_parser("detect", help="Voice check (POST /api/voice-detection).")
    p_detect.add_argument("audio_path", help="Path to an MP3 file.")
    p_detect.add_argument("language", help="Tamil | English | Hindi | Malayalam | Telugu")
    p_detect.add_argument(
        "--api-key",
        default=None,
        help="API key (default: read from API_KEY env var / .env).",
    )
    p_detect.set_defaults(_handler="detect")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    _load_env(args.env_file)

    base_url = str(args.base_url).rstrip("/")

    if args._handler == "health":
        return cmd_health(base_url)

    if args._handler == "detect":
        api_key = args.api_key or os.getenv("API_KEY")
        if not api_key:
            print(
                "Error: missing API key. Set API_KEY in .env / env vars, or pass --api-key.",
                file=sys.stderr,
            )
            return 2
        return cmd_detect(base_url, api_key, args.audio_path, args.language)

    print("Error: unknown command", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())


