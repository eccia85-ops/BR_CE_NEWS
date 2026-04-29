import urllib.request
import xml.etree.ElementTree as ET
import json

KEYWORDS = [
    "약가",
    "급여",
    "보험",
    "임상",
    "식약처",
    "신약",
    "바이오",
    "CDMO",
]

SITES = [
    {
        "name": "DailyPharm",
        "rss": "https://www.dailypharm.com/rss/allArticle.xml",
    },
    {
        "name": "HitNews",
        "rss": "https://www.hitnews.co.kr/rss/allArticle.xml",
    },
]

def fetch_rss(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return ET.fromstring(r.read())

def handler(request):
    results = []

    for site in SITES:
        try:
            root = fetch_rss(site["rss"])
            for item in root.findall(".//item"):
                title = item.findtext("title")
                link = item.findtext("link")

                if title and any(k in title for k in KEYWORDS):
                    results.append({
                        "site": site["name"],
                        "title": title,
                        "link": link,
                    })
        except Exception as e:
            results.append({
                "site": site["name"],
                "error": str(e),
            })

    return {
        "statusCode": 200,
        "headers": { "Content-Type": "application/json" },
        "body": json.dumps({
            "count": len(results),
            "results": results
        }, ensure_ascii=False)
    }
