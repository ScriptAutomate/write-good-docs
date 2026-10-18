"""Thin client for the Tidyfeed API."""
import json
from pathlib import Path

import requests

CACHE = Path.home() / ".cache" / "tidyfeed" / "items.json"


class Client:
    def __init__(self, api_url, token):
        self.api_url = api_url
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {token}"

    def check_token(self):
        return self.session.get(f"{self.api_url}/me", timeout=10).status_code == 200

    def fetch(self, feeds, since=None, limit=50):
        items, seen = [], set()
        for feed in dict.fromkeys(feeds):  # a URL listed twice is fetched once
            params = {"url": feed, "limit": limit}
            if since:
                params["since"] = since
            resp = self.session.get(f"{self.api_url}/items", params=params, timeout=30)
            resp.raise_for_status()
            for item in resp.json()["items"]:
                if item["link"] not in seen:
                    seen.add(item["link"])
                    items.append(item)
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(items))
        return len(items)

    def export(self, fmt, output):
        items = json.loads(CACHE.read_text())
        from . import exporters
        exporters.write(fmt, items, output)
