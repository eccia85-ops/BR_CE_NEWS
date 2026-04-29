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

  <!-- ===== [1] 스타일 영역 ===== -->
  <style>
    body {
      font-family: Arial;
      margin: 20px;
    }

    /* ---- 탭 버튼 ---- */
    .tabs button {
      padding: 6px 14px;
      margin-right: 6px;
      border: 1px solid #ccc;
      background: #f8f8f8;
      cursor: pointer;
      border-radius: 4px;
    }

    .tabs button.active {
      background: #4f67ff;
      color: white;
      border-color: #4f67ff;
      font-weight: bold;
    }

    /* ---- 키워드 섹션 ---- */
    .keyword {
      margin-top: 36px;
    }

    /* ---- 카드 목록 ---- */
    .cards {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 12px;
    }

    /* ---- 카드 ---- */
    .card {
      border: 1px solid #e0e0e0;
      border-radius: 6px;
      padding: 12px;
      background: white;
    }

    /* ---- 카드 제목 (가장 중요) ---- */
    .card-title {
      font-size: 15px;
      font-weight: bold;
      line-height: 1.4;
    }

    .card-title a {
      color: #111;
      text-decoration: none;
    }

    .card-title a:hover {
      text-decoration: underline;
    }

    /* ---- 카드 하단 정보 (출처 + 날짜) ---- */
    .card-meta {
      margin-top: 6px;
      font-size: 12px;
      color: #777;
    }
  </style>
</head>

<body>

  <!-- ===== [2] 페이지 제목 ===== -->
  <h1>📊 CE 키워드 뉴스</h1>

  <!-- ===== [3] 기간 탭 ===== -->
  <div class="tabs">
    <button id="tab-today" onclick="loadView('today')">오늘</button>
    <button id="tab-week" onclick="loadView('week')">주간</button>
    <button id="tab-month" onclick="loadView('month')">월간</button>
  </div>

  <!-- ===== [4] 뉴스 카드가 들어갈 영역 ===== -->
  <div id="app"></div>

  <!-- ===== [5] 자바스크립트 ===== -->
  <script>
    let rawData = null;
    let currentTab = "today";

    // [5-1] 날짜 문자열 → YYYY-MM-DD 변환
    function formatDate(raw) {
      if (!raw) return "";
      const d = new Date(raw);
      return d.toISOString().slice(0, 10);
    }

    // [5-2] API 데이터 로드
    async function loadData() {
      const res = await fetch('/api/news');
      rawData = await res.json();
      setActiveTab('today');
      render();
    }

    // [5-3] 선택된 탭 표시
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

    // [5-4] 화면에 카드 그리기 (★ 여기 중요)
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
          // box.innerHTML += `<pre style="font-size:11px">${JSON.stringify(i, null,
          
          box.innerHTML += `
              <div class="card">
                <div class="card-title">
                  <a href="${i.link}" targete}
                  </a>
                </div>
                <div class="card-meta">
                  ${i.site} · ${formatDate(i.date)}
                </div>
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
