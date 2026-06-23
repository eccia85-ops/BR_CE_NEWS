# 모니터링 RSS 소스 목록
# ✅ 활성  ⚠️ 고려중  ❌ 제외

RSS_SOURCES = [
    # ✅ 활성
    {
        "site": "약사공론",
        "url": "https://www.kpanews.co.kr/rss/allArticle.xml"
    },
    # ✅ 활성
    {
        "site": "히트뉴스",
        "url": "http://www.hitnews.co.kr/rss/allArticle.xml"
    },
    # ✅ 활성
    {
        "site": "메디파나뉴스",
        "url": "https://www.medipana.com/rss/allArticle.xml"
    },
    # ✅ 활성
    {
        "site": "의학신문",
        "url": "http://www.bosa.co.kr/rss/allArticle.xml"
    },
    # ✅ 활성
    {
        "site": "팜뉴스",
        "url": "https://www.pharmnews.com/rss/allArticle.xml"
    },
    # ⚠️ 고려중 — 광고성 기사 비중 높음, 추후 품질 확인 후 결정
    # {
    #     "site": "바이오타임즈",
    #     "url": "https://www.biotimes.co.kr/rss/allArticle.xml"
    # },
    # ⚠️ 고려중 — 의사 커뮤니티 관점, CE팀 직접 관련도 낮음
    # {
    #     "site": "청년의사",
    #     "url": "http://www.docdocdoc.co.kr/rss/allArticle.xml"
    # },
    # ⚠️ 고려중 — 청년의사와 커버리지 유사, 중복 가능성
    # {
    #     "site": "메디게이트뉴스",
    #     "url": "https://www.medigatenews.com/rss/allArticle.xml"
    # },
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
    # ❌ 제외 — RSS 미제공
    # {
    #     "site": "약업닷컴",
    #     "url": "https://www.yakup.com/rss/allArticle.xml"
    # },
    # ✅ 활성 — 제약/바이오 전반 + 보령 관련 주요 매체 커버
    {
        "site": "구글뉴스-제약바이오",
        "url": "https://news.google.com/rss/search?q=제약+바이오&hl=ko&gl=KR&ceid=KR:ko"
    },
    {
        "site": "구글뉴스-보령",
        "url": "https://news.google.com/rss/search?q=보령제약&hl=ko&gl=KR&ceid=KR:ko"
    },
]
