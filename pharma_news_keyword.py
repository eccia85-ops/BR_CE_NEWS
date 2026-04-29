
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# =========================
# 1. 내가 보고 싶은 키워드
# =========================
KEYWORDS = [
    "약가",
    "급여",
    "보험",
    "임상",
    "식약처",
    "신약",
    "바이오",
    "CDMO",
   "보령",
]

# =========================
# 2. 뉴스 사이트 (RSS)
# =========================
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

# =========================
# 3. 유틸 함수
# =========================
def fetch_rss(rss_url):
    """RSS 주소에서 XML을 가져온다"""
    with urllib.request.urlopen(rss_url, timeout=10) as response:
        return ET.fromstring(response.read())

def contains_keyword(title):
    """제목에 키워드가 하나라도 포함되어 있는지"""
    return any(keyword in title for keyword in KEYWORDS)

# =========================
# 4. 메인 로직
# =========================
results = []

for site in SITES:
    try:
        root = fetch_rss(site["rss"])
        for item in root.findall(".//item"):
            title = item.findtext("title")
            link = item.findtext("link")

            if title and contains_keyword(title):
                results.append({
                    "site": site["name"],
                    "title": title.strip(),
                    "link": link.strip() if link else "",
                })

    except Exception as e:
        print(f"[ERROR] {site['name']} RSS 읽기 실패: {e}")

# =========================
# 5. 출력
# =========================
today = datetime.now().strftime("%Y-%m-%d")

print("=" * 60)
print(f"📌 {today} 제약/바이오 키워드 뉴스")
print("=" * 60)

if not results:
    print("조건에 맞는 뉴스가 없습니다.")
else:
    for i, item in enumerate(results, 1):
        print(f"{i}. [{item['site']}] {item['title']}")
        print(f"   → {item['link']}\n")

print(f"총 {len(results)}건")
print("✅ 완료")
