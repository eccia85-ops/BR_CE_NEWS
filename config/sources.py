# 모니터링 RSS 소스 목록
# ✅ 정상  ❌ 수집실패(경로 막힘)  ⚠️ 미확인(배포 후 확인 필요)

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
    # ⚠️ 미확인 — RSS 안내페이지 존재, 동일 패턴 추정
    {
        "site": "히트뉴스",
        "url": "http://www.hitnews.co.kr/rss/allArticle.xml"
    },
    # ⚠️ 미확인 — 배포 후 오류 시 주석 처리
    {
        "site": "팜뉴스",
        "url": "https://www.pharmnews.com/rss/allArticle.xml"
    },
    # ✅ 구글뉴스 RSS — 국내 제약언론 전체 커버 (데일리팜·메디칼타임즈 포함)
    {
        "site": "구글뉴스-제약",
        "url": "https://news.google.com/rss/search?q=제약+바이오&hl=ko&gl=KR&ceid=KR:ko"
    },
    {
        "site": "구글뉴스-약가",
        "url": "https://news.google.com/rss/search?q=신약+급여+약가&hl=ko&gl=KR&ceid=KR:ko"
    },
]
