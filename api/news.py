from fastapi import FastAPI
import urllib.request
import xml.etree.ElementTree as ET

from config.keywords import KEYWORDS
from config.sources import RSS_SOURCES

app = FastAPI()

def fetch_rss(site, url, keywords=None):
    items = []
    with urllib.request.urlopen(url, timeout=10) as r:
        root = ET.fromstring(r.read())

    for item in root.findall(".//item")[:30]:
        title = item.findtext("title")
        link = item.findtext("link")
        date = item.findtext("pubDate")

        if not title:
            continue

        if keywords:
            if not any(k in title for k in keywords):
                continue

        items.append({
            "site": site,
            "title": title,
            "link": link,
            "date": date
        })

    return items


@app.get("/api/news")
def news():
    results = []

    for src in RSS_SOURCES:
        try:
            results.extend(
                fetch_rss(
                    src["site"],
                    src["url"],
                    KEYWORDS
                )
            )
        except Exception:
            continue

    return {
        "keywords": KEYWORDS,
        "count": len(results),
        "items": results
    }
``
