from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"/>
  <title>CE 키워드 뉴스</title>
  <style>
    :root {
      --primary:      #1a56db;
      --primary-light:#e8eefb;
      --bg:           #f0f2f7;
      --card:         #ffffff;
      --border:       #e5e7eb;
      --text:         #111827;
      --sub:          #6b7280;
      --badge-bg:     #f3f4f6;
      --error-bg:     #fef2f2;
      --error-txt:    #991b1b;
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
                   'Apple SD Gothic Neo', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
    }
    .header {
      background: var(--primary);
      color: white;
      padding: 14px 18px 12px;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 2px 8px rgba(0,0,0,0.18);
    }
    .header h1  { font-size: 17px; font-weight: 700; letter-spacing: -0.3px; }
    .header .sub { font-size: 11px; opacity: 0.75; margin-top: 2px; }
    .tabs {
      background: white;
      display: flex;
      border-bottom: 2px solid var(--border);
      position: sticky;
      top: 56px;
      z-index: 99;
    }
    .tab {
      flex: 1;
      padding: 11px 0;
      border: none;
      background: none;
      font-size: 14px;
      font-weight: 500;
      color: var(--sub);
      cursor: pointer;
      border-bottom: 2px solid transparent;
      margin-bottom: -2px;
    }
    .tab.active {
      color: var(--primary);
      font-weight: 700;
      border-bottom-color: var(--primary);
    }
    .content { padding: 12px 14px 32px; max-width: 960px; margin: 0 auto; }
    .status-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      color: var(--sub);
      padding: 8px 2px 10px;
    }
    .status-left { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
    .badge {
      background: var(--primary-light);
      color: var(--primary);
      border-radius: 20px;
      padding: 2px 9px;
      font-size: 11px;
      font-weight: 600;
    }
    .badge-error { background: var(--error-bg); color: var(--error-txt); }
    .refresh-btn {
      background: white;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 4px 11px;
      font-size: 12px;
      cursor: pointer;
      color: var(--sub);
    }
    .refresh-btn:active { transform: scale(0.97); }
    .error-banner {
      background: var(--error-bg);
      border: 1px solid #fecaca;
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 12px;
      color: var(--error-txt);
      margin-bottom: 12px;
    }
    .kw-section { margin-bottom: 22px; }
    .kw-header {
      display: flex;
      align-items: center;
      gap: 7px;
      margin-bottom: 9px;
    }
    .kw-name  { font-size: 15px; font-weight: 700; }
    .kw-count {
      background: var(--primary);
      color: white;
      border-radius: 20px;
      padding: 1px 8px;
      font-size: 11px;
      font-weight: 700;
    }
    .cards {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
      gap: 9px;
    }
    .card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 13px 14px;
    }
    .card-title { font-size: 13.5px; font-weight: 600; line-height: 1.5; }
    .card-title a { color: var(--text); text-decoration: none; }
    .card-title a:hover { color: var(--primary); text-decoration: underline; }
    .card-meta {
      margin-top: 8px;
      display: flex;
      gap: 6px;
      align-items: center;
      font-size: 11px;
      color: var(--sub);
    }
    .src-tag {
      background: var(--badge-bg);
      border-radius: 4px;
      padding: 1px 6px;
      font-size: 11px;
      color: #374151;
    }
    .loading { text-align: center; padding: 60px 20px; color: var(--sub); }
    .spinner {
      width: 34px; height: 34px;
      border: 3px solid var(--border);
      border-top-color: var(--primary);
      border-radius: 50%;
      animation: spin 0.75s linear infinite;
      margin: 0 auto 14px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    .loading-text { font-size: 13px; }
    .empty {
      text-align: center;
      padding: 40px 20px;
      color: var(--sub);
      font-size: 13px;
      background: white;
      border-radius: 10px;
      border: 1px dashed var(--border);
    }
  </style>
</head>

<body>
  <div class="header">
    <h1>📊 CE 키워드 뉴스</h1>
    <div class="sub">보령 CE기획팀 · 제약 업계 키워드 모니터링</div>
  </div>

  <div class="tabs">
    <button class="tab active" id="tab-today" onclick="switchTab('today')">오늘</button>
    <button class="tab"        id="tab-week"  onclick="switchTab('week')">주간</button>
    <button class="tab"        id="tab-month" onclick="switchTab('month')">월간</button>
  </div>

  <div class="content">
    <div class="loading" id="loading">
      <div class="spinner"></div>
      <div class="loading-text">뉴스를 수집하는 중입니다…</div>
    </div>
    <div id="app" style="display:none"></div>
  </div>

  <script>
    let currentTab = 'today';
    const clientCache = {};

    function switchTab(tab) {
      document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
      document.getElementById('tab-' + tab).classList.add('active');
      currentTab = tab;
      if (clientCache[tab]) {
        render(clientCache[tab], tab);
      } else {
        loadData(tab);
      }
    }

    async function loadData(range) {
      showLoading();
      try {
        const res = await fetch('/api/news?range=' + range);
        if (!res.ok) throw new Error('서버 오류 ' + res.status);
        const data = await res.json();
        clientCache[range] = data;
        render(data, range);
      } catch (e) {
        showFetchError(e.message);
      }
    }

    function refresh() {
      delete clientCache[currentTab];
      loadData(currentTab);
    }

    function fmtDate(raw) {
      if (!raw) return '';
      const d = new Date(raw);
      if (isNaN(d)) return '';
      const now = new Date();
      const diff = Math.floor((now - d) / 60000);
      if (diff < 1)    return '방금';
      if (diff < 60)   return diff + '분 전';
      if (diff < 1440) return Math.floor(diff / 60) + '시간 전';
      const mm = d.getMonth() + 1, dd = d.getDate();
      return mm + '.' + String(dd).padStart(2, '0');
    }

    function esc(str) {
      return String(str || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }

    function render(data, range) {
      document.getElementById('loading').style.display = 'none';
      const app = document.getElementById('app');
      app.style.display = 'block';

      const LABEL = { today: '오늘', week: '최근 7일', month: '최근 30일' };
      const total = data.keywords.reduce(
        (s, k) => s + (data.data[k]?.length || 0), 0
      );

      let html = '<div class="status-bar"><div class="status-left">';
      html += '<span class="badge">📅 ' + LABEL[range] + '</span>';
      html += '<span class="badge">📰 ' + total + '건</span>';
      if (data.errors?.length) {
        html += '<span class="badge badge-error">⚠️ '
              + data.errors.length + '개 소스 오류</span>';
      }
      html += '</div>';
      html += '<button class="refresh-btn" onclick="refresh()">🔄 새로고침</button>';
      html += '</div>';

      if (data.errors?.length) {
        html += '<div class="error-banner">수집 실패: '
              + esc(data.errors.join(', ')) + '</div>';
      }

      let hasAny = false;
      for (const kw of data.keywords) {
        const items = data.data[kw];
        if (!items || items.length === 0) continue;
        hasAny = true;

        html += '<div class="kw-section">'
              + '<div class="kw-header">'
              + '<span class="kw-name">' + esc(kw) + '</span>'
              + '<span class="kw-count">' + items.length + '</span>'
              + '</div><div class="cards">';

        for (const item of items) {
          html += '<div class="card">'
                + '<div class="card-title"><a href="' + esc(item.link)
                + '" target="_blank" rel="noopener">'
                + esc(item.title || '(제목 없음)') + '</a></div>'
                + '<div class="card-meta">'
                + '<span class="src-tag">' + esc(item.site) + '</span>'
                + '<span>' + fmtDate(item.date) + '</span>'
                + '</div></div>';
        }
        html += '</div></div>';
      }

      if (!hasAny) {
        html += '<div class="empty">📭 '
              + LABEL[range] + ' 기간 내 해당 키워드 뉴스가 없습니다.</div>';
      }

      app.innerHTML = html;
    }

    function showLoading() {
      document.getElementById('loading').style.display = 'block';
      document.getElementById('app').style.display = 'none';
    }

    function showFetchError(msg) {
      document.getElementById('loading').style.display = 'none';
      const app = document.getElementById('app');
      app.style.display = 'block';
      app.innerHTML = '<div class="error-banner">⚠️ 데이터를 불러오지 못했습니다: '
                    + esc(msg) + '</div>';
    }

    loadData('today');
  </script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def home():
    return HTML
