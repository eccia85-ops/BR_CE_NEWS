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
from collections import Counter
import time
import json
import base64
import re

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


def norm_title(t):
    return re.sub(r'[^\w]', '', t)[:20]


@app.get("/api/news")
def get_news(range: str = Query("today")):
    if range not in ("today", "week", "month"):
        range = "today"

    all_articles, errors = get_all_articles()
    filtered = [a for a in all_articles if in_range(a, range)]

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

    norm_count = Counter(norm_title(a["title"]) for a in article_kws.values())
    for link, art in article_kws.items():
        art["mention_count"] = norm_count[norm_title(art["title"])]

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
        articles.sort(key=lambda x: (
            -(x.get("mention_count", 1)),
            x.get("date") or ""
        ), reverse=False)
        cat_bucket[cat] = articles

    bucket = {k: [] for k in KEYWORDS}
    for link, art in article_kws.items():
        for tag in art["tags"]:
            bucket[tag].append({
                "site":          art["site"],
                "title":         art["title"],
                "link":          art["link"],
                "date":          art["date"],
                "mention_count": art.get("mention_count", 1),
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


@app.get("/api/articles")
def get_articles(range: str = Query("today")):
    if range not in ("today", "week", "month"):
        range = "today"

    all_articles, errors = get_all_articles()
    filtered = [a for a in all_articles if in_range(a, range)]

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


def gemini_summarize(articles_by_cat, range_label, brief=False):
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return {}

    lines = []
    lines.append(f"아래는 {range_label} 제약 업계 뉴스입니다.")
    lines.append("보령제약 CE기획팀 관점에서 카테고리별로 핵심 내용을 2~3줄로 요약해주세요.")
    lines.append("주요 사업: 만성질환(순환기/당뇨/이상지질), 항암, 항생제, CDMO")
    lines.append("")
    if brief:
        lines.append("[출력 형식] 아래 형식으로만 답하세요. 마크다운 사용 금지. 간결하게:")
    else:
        lines.append("[출력 형식] 아래 형식으로만 답하세요. 마크다운 사용 금지:")
    lines.append("각 카테고리 안에서 항목별로 아래 형식으로 나열하세요.")
    lines.append("중요도 높은 항목부터 나열하세요.")
    lines.append("동일한 사건을 다룬 기사는 하나로 통합해서 표기하세요.")
    lines.append("해당 카테고리 기사가 없으면 '해당 없음'으로 표기하세요.")
    lines.append("")
    lines.append("예시:")
    lines.append("자사 직결:")
    lines.append("- 보령 탁소텔 인수 완료, 글로벌 판매 개시")
    lines.append("  항암 포트폴리오 확대 발판 마련")
    lines.append("- 온베브지 급여 확대 검토 중")
    lines.append("  매출 확대 기회 가능성")
    lines.append("시장 영향:")
    lines.append("- GLP-1 계열 급여 논의 본격화")
    lines.append("  당뇨 시장 지형 변화 예상")
    lines.append("업계 동향:")
    lines.append("- AI 신약 개발 투자 확대")
    lines.append("  중장기 파이프라인 경쟁 심화")
    lines.append("")
    lines.append("========================================")
    lines.append("")

    for cat, arts in articles_by_cat.items():
        if not arts:
            continue
        lines.append(f"=== {cat} ===")
        for a in arts[:20]:
            lines.append(f"- {a['title']} ({a['site']})")
        lines.append("")

    prompt = "\n".join(lines)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 1000, "temperature": 0.3}
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            res = json.loads(r.read())
            text = res["candidates"][0]["content"]["parts"][0]["text"]
            return parse_summary(text)
    except Exception as e:
        return {"error": str(e)}


def parse_summary(text):
    result = {}
    patterns = {
        "자사 직결": r"자사 직결[:：]\s*(.+?)(?=\n시장 영향|\n업계 동향|$)",
        "시장 영향": r"시장 영향[:：]\s*(.+?)(?=\n자사 직결|\n업계 동향|$)",
        "업계 동향": r"업계 동향[:：]\s*(.+?)(?=\n자사 직결|\n시장 영향|$)",
    }
    for cat, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            result[cat] = match.group(1).strip()
    return result


def load_news_json():
    token  = os.environ.get("GITHUB_TOKEN", "")
    repo   = os.environ.get("GITHUB_REPO", "")
    branch = os.environ.get("GITHUB_BRANCH", "main")

    if not token or not repo:
        return [], None

    url = f"https://api.github.com/repos/{repo}/contents/data/news.json?ref={branch}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "CE-NewsBot/1.0"
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            res = json.loads(r.read())
            content = base64.b64decode(res["content"]).decode("utf-8")
            data = json.loads(content)
            return data.get("articles", []), res["sha"]
    except Exception:
        return [], None


def save_news_json(articles, sha=None, daily_summary=None, weekly_summaries=None, monthly_summaries=None):
    token  = os.environ.get("GITHUB_TOKEN", "")
    repo   = os.environ.get("GITHUB_REPO", "")
    branch = os.environ.get("GITHUB_BRANCH", "main")

    if not token or not repo:
        return False

    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=90)
    filtered = []
    for a in articles:
        dt = parse_date(a.get("date", ""))
        if dt is None or ensure_aware(dt) >= cutoff:
            filtered.append(a)

    existing, _ = load_news_json()
    existing_data = existing[0] if isinstance(existing, tuple) else {}

    saved_weekly = existing_data.get("weekly_summaries", []) if isinstance(existing_data, dict) else []
    if weekly_summaries:
        saved_weekly = [weekly_summaries] + saved_weekly
        saved_weekly = saved_weekly[:12]

    saved_monthly = existing_data.get("monthly_summaries", []) if isinstance(existing_data, dict) else []
    if monthly_summaries:
        saved_monthly = [monthly_summaries] + saved_monthly
        saved_monthly = saved_monthly[:6]

    data = {
        "updated_at":        datetime.now(tz=KST).strftime("%Y-%m-%d %H:%M"),
        "total":             len(filtered),
        "articles":          filtered,
        "daily_summary":     daily_summary or {},
        "weekly_summaries":  saved_weekly,
        "monthly_summaries": saved_monthly,
    }

    content = base64.b64encode(
        json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("utf-8")

    body = {
        "message": f"Update news.json ({data['updated_at']})",
        "content": content,
        "branch":  branch
    }
    if sha:
        body["sha"] = sha

    url = f"https://api.github.com/repos/{repo}/contents/data/news.json"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "CE-NewsBot/1.0",
            "Content-Type": "application/json"
        },
        method="PUT"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status in (200, 201)
    except Exception:
        return False


@app.get("/api/collect")
def collect():
    saved_articles, sha = load_news_json()
    all_articles, errors = get_all_articles()
    existing_links = set(a["link"] for a in saved_articles)

    new_count = 0
    for a in all_articles:
        if a["link"] not in existing_links:
            saved_articles.append({
                "site":  a["site"],
                "title": a["title"],
                "link":  a["link"],
                "date":  a["date"],
                "tags":  [],
            })
            existing_links.add(a["link"])
            new_count += 1

    articles_by_cat = {}
    for cat, kws in CATEGORIES.items():
        kw_set = set(kws)
        matched = []
        seen = set()
        for a in all_articles:
            if a["link"] not in seen:
                for kw in kw_set:
                    if kw in a["title"]:
                        matched.append(a)
                        seen.add(a["link"])
                        break
        articles_by_cat[cat] = matched

    today_str = datetime.now(tz=KST).strftime("%Y년 %m월 %d일")
    summary = gemini_summarize(articles_by_cat, today_str)

    import datetime as dt
    now_kst  = dt.datetime.now(tz=KST)
    is_friday = now_kst.weekday() == 4
    last_day  = (now_kst + dt.timedelta(days=1)).day == 1

    weekly_summary = None
    if is_friday:
        weekly_summary = {
            "label":   now_kst.strftime("%Y년 %m월 %d일 주간"),
            "summary": summary
        }

    monthly_summary = None
    if last_day:
        monthly_sum = gemini_summarize(articles_by_cat, now_kst.strftime("%Y년 %m월"), brief=True)
        monthly_summary = {
            "label":   now_kst.strftime("%Y년 %m월"),
            "summary": monthly_sum
        }

    ok = save_news_json(
        saved_articles, sha,
        daily_summary=summary,
        weekly_summaries=weekly_summary,
        monthly_summaries=monthly_summary
    )

    return JSONResponse({
        "status":          "ok" if ok else "save_failed",
        "new":             new_count,
        "total":           len(saved_articles),
        "summary":         summary,
        "is_friday":       is_friday,
        "is_month_end":    last_day,
        "monthly_summary": monthly_summary,
        "errors":          errors,
    })


@app.get("/api/brief")
def get_brief():
    cached = _cache.get("brief")
    if cached:
        return JSONResponse(cached)

    token  = os.environ.get("GITHUB_TOKEN", "")
    repo   = os.environ.get("GITHUB_REPO", "")
    branch = os.environ.get("GITHUB_BRANCH", "main")

    url = f"https://api.github.com/repos/{repo}/contents/data/news.json?ref={branch}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "CE-NewsBot/1.0"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            res = json.loads(r.read())
            content = base64.b64decode(res["content"]).decode("utf-8")
            data = json.loads(content)
            brief_data = {
                "updated_at":        data.get("updated_at", ""),
                "daily_summary":     data.get("daily_summary", {}),
                "weekly_summaries":  data.get("weekly_summaries", []),
                "monthly_summaries": data.get("monthly_summaries", []),
            }
            _cache["brief"] = brief_data
            return JSONResponse(brief_data)
    except Exception as e:
        return JSONResponse({"error": str(e)})
