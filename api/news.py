from fastapi import FastAPI
import urllib.request
import xml.etree.ElementTree as ET

from config.sources import RSS_SOURCES
from config.keywords import KEYWORDS

app = FastAPI()

def fetch_rss(site, url):
    with urllib.request.urlopen(url, timeout=10) as r:
        root = ET.fromstring(r.read())

    articles = []
    for item in root.findall(".//item")[:40]:
        title = item.findtext("title")
        link = item.findtext("link")
        date = item.findtext("pubDate")

        if not title:
            continue

        articles.append({
            "site": site,
            "title": title,
            "link": link,
            "date": date
        })
    return articles


@app.get("/api/news")
def news():
    bucket = {k: [] for k in KEYWORDS}

    for src in RSS_SOURCES:
        try:
            articles = fetch_rss(src["site"], src["url"])
        except Exception:
            continue

        for a in articles:
            for k in KEYWORDS:
                if k in a["title"]:
                    bucket[k].append(a)

    return {
        "keywords": KEYWORDS,
        "data": bucket
    }
