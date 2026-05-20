import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import urllib.request
from urllib.parse import quote
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from config.sources import RSS_SOURCES
from config.keywords import KEYWORDS, CATEGORIES

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"])

_cache: dict = {}
CACHE_TTL = 1800

KST = timezone(timedelta(hours=9))


def parse_date(raw):
    if not raw:
        return None
    try:
        return parsedate_to_datetime(raw.strip())
    except Exception:
        pass
    try:
        return datetime.fromisoformat(raw.strip())
    except Exception:
        return None


def ensure_aware(dt):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=KST)
    return dt


def in_range(article, range_):
    dt = article.get("date_obj")
    if dt is None:
        return range_ == "month"

    dt = ensure_aware(dt)
    now = datetime.now(tz=timezone.utc)

    if range_ == "today":
        today_kst = now.astimezone(KST).date()
        return dt.astimezone(KST).date() == today_kst

    if range_ == "week":
        return dt >= now - timedelta(days=7)

    if range_ == "month":
        return dt >= now - timedelta(days=30)

    return True


def fetch_one(site, url):
    url = quote(url, safe=':/?=&#+@')
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (CE-NewsBot/1.0)"}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        root = ET.fromstring(r.read())

    DC = "{http://purl.org/dc/elements/1.1/}"
    articles = []

    for item in root.findall(".//item")[:60]:
        title = (item.findtext("title") or "").strip()
        link  = (item.findtext("link")  or "").strip()
        raw_date = (
            item.findtext("pubDate")
            or item.findtext(f"{DC}date")
            or ""
        )
        if not title:
            continue

        articles.append({
            "site":     site,
            "title":    title,
            "link":     link,
            "date":     raw_date,
            "date_obj": parse_date(raw_date),
        })

    return articles


def get_all_articles():
    now = time.time()
    cached = _cache.get("main")

    if cached and (now - cached["ts"]) < CACHE_TTL:
        return cached["articles"], cached["errors"]

    all_articles = []
    errors = []

    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {
            pool.submit(fetch_one, src["site"], src["url"]): src["site"]
            for src in RSS_SOURCES
        }
        for fut in as_completed(futures):
            site = futures[fut]
            try:
                all_articles.extend(fut.result())
            except Exception:
                errors.append(site)

    _cache["main"] = {
        "articles": all_articles,
        "errors": errors,
        "ts": now
    }
    return all_articles, errors


@app.get("/api/news")
def get_news(range: str = Query("today")):
    if range not in ("today", "week", "month"):
        range = "today"

    all_articles, errors = get_all_articles()
    filtered = [a for a in all_articles if in_range(a, range)]

    bucket = {k: [] for k in KEYWORDS}
    seen = set()

    # 기사별 매칭 키워드 수집
    article_kws = {}
    for article in filtered:
        link = article["link"]
        for keyword in KEYWORDS:
            if keyword in article["title"]:
                if link not in article_kws:
                    article_kws[link] = {
                        "site":  article["site"],
                        "title": article["title"],
                        "link":  link,
                        "date":  article["date"],
                        "tags":  [],
                    }
                if keyword not in article_kws[link]["tags"]:
                    article_kws[link]["tags"].append(keyword)

    # 다수 보도 카운트 (제목 앞 20자 정규화 후 비교)
    import re
    from collections import Counter

    def norm_title(t):
        return re.sub(r'[^\w]', '', t)[:20]

    norm_count = Counter(norm_title(a["title"]) for a in article_kws.values())

    for link, art in article_kws.items():
        art["mention_count"] = norm_count[norm_title(art["title"])]

    # 카테고리별 버킷 구성
    cat_bucket = {}
    for cat, kws in CATEGORIES.items():
        kw_set = set(kws)
        articles = []
        seen_links = set()
        for link, art in article_kws.items():
            if kw_set & set(art["tags"]):
                if link not in seen_links:
                    seen_links.add(link)
                    articles.append(art)
        # 다수 보도 우선 + 날짜 순
        articles.sort(key=lambda x: (
            -(x.get("mention_count", 1)),
            x.get("date") or ""
        ), reverse=False)
        cat_bucket[cat] = articles

    # 오늘 탭용 기존 버킷도 유지
    bucket = {k: [] for k in KEYWORDS}
    for link, art in article_kws.items():
        for tag in art["tags"]:
            bucket[tag].append({
                "site":  art["site"],
                "title": art["title"],
                "link":  art["link"],
                "date":  art["date"],
            })
    for k in bucket:
        bucket[k].sort(key=lambda x: x["date"] or "", reverse=True)

    return JSONResponse({
        "keywords":   KEYWORDS,
        "categories": {cat: kws for cat, kws in CATEGORIES.items()},
        "data":       bucket,
        "cat_data":   cat_bucket,
        "sources":    [src["site"] for src in RSS_SOURCES],
        "errors":     errors,
    })

    for k in bucket:
        bucket[k].sort(key=lambda x: x["date"] or "", reverse=True)

    return JSONResponse({
        "keywords":   KEYWORDS,
        "categories": {cat: kws for cat, kws in CATEGORIES.items()},
        "data":       bucket,
        "errors":     errors,
    })
@app.get("/api/articles")
def get_articles(range: str = Query("today")):
    if range not in ("today", "week", "month"):
        range = "today"

    all_articles, errors = get_all_articles()
    filtered = [a for a in all_articles if in_range(a, range)]

    # 중복 링크 제거
    seen = set()
    articles = []
    for a in filtered:
        if a["link"] not in seen:
            seen.add(a["link"])
            articles.append({
                "site":  a["site"],
                "title": a["title"],
                "link":  a["link"],
                "date":  a["date"],
            })

    articles.sort(key=lambda x: x["date"] or "", reverse=True)

    return JSONResponse({
        "articles": articles,
        "total":    len(articles),
        "errors":   errors,
    })
