from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>CE 키워드 뉴스</title>

  <!-- =========================
       [1] 전체 스타일 영역
       - 카드 디자인
       - 탭(오늘/주간/월간) 선택 표시
       ========================= -->
  <style>
    body { font-family: Arial; margin: 20px; }

    /* ---------- 탭 UI ---------- */
    .tabs button {
      padding: 6px 14px;
      margin-right: 6px;
      border: 1px solid #ccc;
      background: #f8f8f8;
      cursor: pointer;
      border-radius: 4px;
    }

    .tabs button.active {
      background: #2f6df6;
      color: white;
      border-color: #2f6df6;
      font-weight: bold;
    }

    /* ---------- 키워드 섹션 ---------- */
    .keyword { margin-top: 36px; }

    /* ---------- 카드 레이아웃 ---------- */
    .cards {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 12px;
    }

    .card {
      border: 1px solid #e0e0e0;
      border-radius: 6px;
      padding: 12px;
      background: white;
    }

    /* ---------- 기사 제목 (메인) ---------- */
    .card-title {
      font-size: 15px;
      font-weight: bold;
      line-height: 1.4;
    }

    .card-title a {
      text-decoration: none;
      color: #111;
    }

    .card-title a:hover {
      text-decoration: underline;
    }

    /* ---------- 출처 (보조 정보) ---------- */
    .card-site {
      margin-top: 6px;
      font-size: 12px;
      color: #777;
    }
  </style>
</head>

<body>

  <!-- =========================
       [2] 페이지 헤더
       ========================= -->
  <h1>📊 CE 키워드 뉴스</h1>

  <!-- =========================
       [3] 기간 탭 영역
       - 오늘 / 주간 / 월간
       ========================= -->
  <div class="tabs">
    <button id="tab-today" onclick="loadView('today')">오늘</button>
    <button id="tab-week" onclick="loadView('week')">주간</button>
    <button id="tab-month" onclick="loadView('month')">월간</button>
  </div>

  <!-- =========================
       [4] 뉴스 카드가 그려질 영역
       ========================= -->
  <div id="app"></div>

  <!-- =========================
       [5] 데이터 처리 & 렌더링 스크립트
       ========================= -->
  <script>
    let rawData = null;
    let currentTab = "today";

    /* ---------- API에서 뉴스 데이터 로딩 ---------- */
    async function loadData() {
      const res = await fetch('/api/news');
      rawData = await res.json();
      setActiveTab('today');
      render();
    }

    /* ---------- 선택된 탭 가시화 ---------- */
    function setActiveTab(tab) {
      currentTab = tab;
      document.querySelectorAll('.tabs button')
        .forEach(b => b.classList.remove('active'));

      document.getElementById(`tab-${tab}`)
        .classList.add('active');
    }

    function loadView(tab) {
      setActiveTab(tab);
      render();
    }

    /* ---------- 키워드별 카드 렌더링 ---------- */
    function render() {
      const app = document.getElementById('app');
      app.innerHTML = '';

      for (const keyword of rawData.keywords) {
        const items = rawData.data[keyword];
        if (!items || items.length === 0) continue;

        app.innerHTML += `
          <div class="keyword">
            <h2>${keyword} (${items.length})</h2>
            <div class="cards" id="k-${keyword}"></div>
          </div>
        `;

        const box = document.getElementById(`k-${keyword}`);

        items.forEach(i => {
          box.innerHTML += `
            <div class="card">
              <div class="card-title">
                <a href="${i.link}" target="_         </div>
              <div class="card-site">${i.site}</div>
            </div>
          `;
        });
      }
    }

    loadData();
  </script>

</body>
</html>
"""
