"""Command-line entry point for tidyfeed."""
import argparse
import sys

from . import __version__, config
from .client import Client


def main(argv=None):
    parser = argparse.ArgumentParser(prog="tidyfeed", description="Fetch and export feeds.")
    parser.add_argument("--version", action="version", version=f"tidyfeed {__version__}")
    parser.add_argument("--config", help="path to config.toml (default: ~/.config/tidyfeed/config.toml)")
    sub = parser.add_subparsers(dest="command", required=True)

    fetch = sub.add_parser("fetch", help="download new items for every configured feed")
    fetch.add_argument("--since", help="only items published after this ISO date, e.g. 2026-01-31")
    fetch.add_argument("--limit", type=int, default=50, help="maximum items per feed (default: 50)")

    export = sub.add_parser("export", help="write fetched items to a file")
    export.add_argument("--format", choices=["json", "csv", "markdown"], default="json")
    export.add_argument("--output", "-o", required=True, help="file to write")

    sub.add_parser("check-token", help="verify that the configured API token is valid")

    args = parser.parse_args(argv)
    try:
        cfg = config.load(args.config)
    except config.ConfigError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    client = Client(cfg["api_url"], cfg["token"])
    if args.command == "check-token":
        ok = client.check_token()
        print("token OK" if ok else "token rejected (401)")
        return 0 if ok else 1
    if args.command == "fetch":
        n = client.fetch(cfg["feeds"], since=args.since, limit=args.limit)
        print(f"fetched {n} items")
        return 0
    if args.command == "export":
        client.export(args.format, args.output)
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
