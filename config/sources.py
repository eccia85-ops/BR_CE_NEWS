# 모니터링 RSS 소스 목록
# ✅ 정상  ❌ 수집실패/제외  ⚠️ 미확인

RSS_SOURCES = [
    # ✅ 정상 확인
    {
        "site": "약사공론",
        "url": "https://www.kpanews.co.kr/rss/allArticle.xml"
    },
    # ✅ 정상 확인
    {
        "site": "의학신문",
        "url": "http://www.bosa.co.kr/rss/allArticle.xml"
    },
    # ✅ 정상 확인
    {
        "site": "히트뉴스",
        "url": "http://www.hitnews.co.kr/rss/allArticle.xml"
    },
    # ✅ 정상 확인
    {
        "site": "팜뉴스",
        "url": "https://www.pharmnews.com/rss/allArticle.xml"
    },
    # ✅ 정상 확인
    {
        "site": "메디파나뉴스",
        "url": "https://www.medipana.com/rss/allArticle.xml"
    },
    # ✅ 정상 확인
    {
        "site": "바이오타임즈",
        "url": "https://www.biotimes.co.kr/rss/allArticle.xml"
    },
    # ✅ 정상 확인
    {
        "site": "청년의사",
        "url": "http://www.docdocdoc.co.kr/rss/allArticle.xml"
    },
    # ✅ 정상 확인
    {
        "site": "메디게이트뉴스",
        "url": "https://www.medigatenews.com/rss/allArticle.xml"
    },
    # ❌ 수집실패 — 기존 경로 접근 불가 (2026.05 확인)
    # {
    #     "site": "데일리팜",
    #     "url": "https://www.dailypharm.com/rss/allArticle.xml"
    # },
    # ❌ 수집실패 — 기존 경로 접근 불가 (2026.05 확인)
    # {
    #     "site": "메디칼타임즈",
    #     "url": "https://www.medicaltimes.com/rss/allArticle.xml"
    # },
    # ❌ 제외 — 약업닷컴 RSS 미제공
    # {
    #     "site": "약업닷컴",
    #     "url": "https://www.yakup.com/rss/allArticle.xml"
    # },
    # ❌ 제외 — 중복 기사 다수 (2026.05)
    # {
    #     "site": "구글뉴스-제약",
    #     "url": "https://news.google.com/rss/search?q=제약+바이오&hl=ko&gl=KR&ceid=KR:ko"
    # },
    # ❌ 제외 — 중복 기사 다수 (2026.05)
    # {
    #     "site": "구글뉴스-약가",
    #     "url": "https://news.google.com/rss/search?q=신약+급여+약가&hl=ko&gl=KR&ceid=KR:ko"
    # },
]
