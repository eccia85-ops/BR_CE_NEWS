from fastapi import FastAPI
import urllib.request
import xml.etree.ElementTree as ET

app = FastAPI()

RSS_SOURCES = [
    {
        "site": "DailyPharm",
        "url": "https://www.dailypharm.com/rss/allArticle.xml"
    },
    {
        "site": "HitNews",
        "url": "https://www.hitnews.co.kr/rss/allArticle.xml"
    }
]

def fetch_rss(site, url, keyword=None):
    items = []
    with urllib.request.urlopen(url, timeout=10) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)

    for item in root.findall(".//item")[:30]:
        title = item.findtext("title")
        link = item.findtext("link")
        pub_date = item.findtext("pubDate")

        if not title:
            continue
        if keyword and keyword not in title:
            continue

        items.append({
            "site": site,
            "title": title,
            "link": link,
            "date": pub_date
        })

    return items


@app.get("/api/news")
def news(keyword: str | None = None):
    results = []

    for src in RSS_SOURCES:
        try:
            results.extend(
                fetch_rss(src["site"], src["url"], keyword)
            )
        except Exception:
            continue

    return {
        "keyword": keyword,
        "count": len(results),
        "items": results
    }
