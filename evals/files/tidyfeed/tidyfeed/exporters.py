"""Write cached items as JSON, CSV, or Markdown."""
import csv
import json

FIELDS = ["title", "link", "published", "feed"]


def write(fmt, items, output):
    with open(output, "w", newline="") as f:
        if fmt == "json":
            json.dump(items, f, indent=2)
        elif fmt == "csv":
            w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
            w.writeheader()
            w.writerows(items)
        elif fmt == "markdown":
            for it in items:
                f.write(f"- [{it['title']}]({it['link']}) ({it.get('published', 'undated')})\n")
