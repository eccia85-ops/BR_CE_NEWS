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
      --primary:       #1a56db;
      --primary-light: #e8eefb;
      --bg:            #f0f2f7;
      --card:          #ffffff;
      --border:        #e5e7eb;
      --text:          #111827;
      --sub:           #6b7280;
      --badge-bg:      #f3f4f6;
      --error-bg:      #fef2f2;
      --error-txt:     #991b1b;
      --cat1-bg:  #fff1f2; --cat1-txt: #be123c; --cat1-bd: #fda4af;
      --cat2-bg:  #fffbeb; --cat2-txt: #b45309; --cat2-bd: #fcd34d;
      --cat3-bg:  #f0fdf4; --cat3-txt: #166534; --cat3-bd: #86efac;
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
                   'Apple SD Gothic Neo', sans-serif;
      background: var(--bg); color: var(--text); min-height: 100vh;
    }
    .header {
      background: var(--primary); color: white;
      padding: 14px 18px 12px;
      position: sticky; top: 0; z-index: 100;
      box-shadow: 0 2px 8px rgba(0,0,0,0.18);
    }
    .header h1  { font-size: 17px; font-weight: 700; letter-spacing: -0.3px; }
    .header .sub { font-size: 11px; opacity: 0.75; margin-top: 2px; }
    .tabs {
      background: white; display: flex;
      border-bottom: 2px solid var(--border);
      position: sticky; top: 56px; z-index: 99;
    }
    .tab {
      flex: 1; padding: 11px 0; border: none; background: none;
      font-size: 14px; font-weight: 500; color: var(--sub);
      cursor: pointer; border-bottom: 2px solid transparent; margin-bottom: -2px;
    }
    .tab.active { color: var(--primary); font-weight: 700; border-bottom-color: var(--primary); }
    .content { padding: 12px 14px 32px; max-width: 960px; margin: 0 auto; }
    .status-bar {
      display: flex; justify-content: space-between; align-items: center;
      font-size: 12px; color: var(--sub); padding: 8px 2px 10px;
    }
    .status-left { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
    .badge {
      background: var(--primary-light); color: var(--primary);
      border-radius: 20px; padding: 2px 9px; font-size: 11px; font-weight: 600;
    }
    .badge-error { background: var(--error-bg); color: var(--error-txt); }
    .refresh-btn {
      background: white; border: 1px solid var(--border); border-radius: 6px;
      padding: 4px 11px; font-size: 12px; cursor: pointer; color: var(--sub);
    }
    .refresh-btn:active { transform: scale(0.97); }
    .error-banner {
      background: var(--error-bg); border: 1px solid #fecaca;
      border-radius: 8px; padding: 10px 14px; font-size: 12px;
      color: var(--error-txt); margin-bottom: 12px;
    }
    .prompt-bar {
      background: #1e293b; border-radius: 10px;
      padding: 12px 16px; margin-bottom: 16px;
      display: flex; justify-content: space-between; align-items: center; gap: 12px;
    }
    .prompt-bar-txt { font-size: 12px; color: #94a3b8; line-height: 1.5; }
    .prompt-bar-txt strong { color: #e2e8f0; display: block; margin-bottom: 2px; }
    .copy-btn {
      background: var(--primary); color: white; border: none;
      border-radius: 7px; padding: 8px 16px; font-size: 13px;
      font-weight: 600; cursor: pointer; white-space: nowrap;
    }
    .copy-btn:hover  { background: #1740a8; }
    .copy-btn:active { transform: scale(0.97); }
    .copy-btn.copied { background: #166534; }
    .cat-section { margin-bottom: 20px; }
    .cat-header {
      display: flex; align-items: center; gap: 8px;
      padding: 10px 14px; border-radius: 10px 10px 0 0;
      border: 1px solid; border-bottom: none;
      font-size: 14px; font-weight: 700;
    }
    .cat-header.c1 { background: var(--cat1-bg); color: var(--cat1-txt); border-color: var(--cat1-bd); }
    .cat-header.c2 { background: var(--cat2-bg); color: var(--cat2-txt); border-color: var(--cat2-bd); }
    .cat-header.c3 { background: var(--cat3-bg); color: var(--cat3-txt); border-color: var(--cat3-bd); }
    .cat-total {
      margin-left: auto; font-size: 11px; font-weight: 600;
      background: rgba(0,0,0,0.08); border-radius: 20px; padding: 1px 8px;
    }
    .kw-list {
      border: 1px solid var(--border); border-top: none;
      border-radius: 0 0 10px 10px; overflow: hidden; background: white;
    }
    .kw-row {
      display: flex; align-items: center; padding: 11px 14px;
      border-bottom: 1px solid var(--border); cursor: pointer;
      transition: background 0.1s; gap: 10px;
    }
    .kw-row:last-child { border-bottom: none; }
    .kw-row:hover { background: var(--badge-bg); }
    .kw-row.empty { cursor: default; opacity: 0.4; }
    .kw-row.empty:hover { background: white; }
    .kw-label { font-size: 14px; font-weight: 600; min-width: 80px; }
    .kw-bar-wrap { flex: 1; height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; }
    .kw-bar { height: 100%; border-radius: 3px; background: var(--primary); transition: width 0.3s; }
    .kw-num { font-size: 12px; font-weight: 700; color: var(--primary); min-width: 32px; text-align: right; }
    .kw-toggle { font-size: 11px; color: var(--sub); }
    .article-list {
      display: none; border-top: 1px solid var(--border);
      padding: 10px 14px 12px; background: #fafafa;
    }
    .article-list.open { display: block; }
    .article-item { padding: 7px 0; border-bottom: 1px solid var(--border); font-size: 13px; }
    .article-item:last-child { border-bottom: none; }
    .article-item a { color: var(--text); text-decoration: none; line-height: 1.5; }
    .article-item a:hover { color: var(--primary); text-decoration: underline; }
    .article-meta { font-size: 11px; color: var(--sub); margin-top: 3px; display: flex; gap: 6px; }
    .src-tag { background: var(--badge-bg); border-radius: 4px; padding: 1px 6px; font-size: 11px; color: #374151; }
    .kw-section { margin-bottom: 22px; }
    .kw-section-header { display: flex; align-items: center; gap: 7px; margin-bottom: 9px; }
    .kw-name { font-size: 15px; font-weight: 700; }
    .kw-count { background: var(--primary); color: white; border-radius: 20px; padding: 1px 8px; font-size: 11px; font-weight: 700; }
    .cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(270px, 1fr)); gap: 9px; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 13px 14px; }
    .card-title { font-size: 13.5px; font-weight: 600; line-height: 1.5; }
    .card-title a { color: var(--text); text-decoration: none; }
    .card-title a:hover { color: var(--primary); text-decoration: underline; }
    .card-meta { margin-top: 8px; display: flex; gap: 6px; align-items: center; font-size: 11px; color: var(--sub); }
    .loading { text-align: center; padding: 60px 20px; color: var(--sub); }
    .spinner {
      width: 34px; height: 34px; border: 3px solid var(--border);
      border-top-color: var(--primary); border-radius: 50%;
      animation: spin 0.75s linear infinite; margin: 0 auto 14px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    .loading-text { font-size: 13px; }
    .empty {
      text-align: center; padding: 40px 20px; color: var(--sub);
      font-size: 13px; background: white; border-radius: 10px;
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
    const CAT_CLASS = { 0: 'c1', 1: 'c2', 2: 'c3' };
    const LABEL = { today: '오늘', week: '최근 7일', month: '최근 30일' };
    const PROMPT_GUIDE = { week: '최근 7일', month: '최근 30일' };

    function switchTab(tab) {
      document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
      document.getElementById('tab-' + tab).classList.add('active');
      currentTab = tab;
      if (clientCache[tab]) render(clientCache[tab], tab);
      else loadData(tab);
    }

    async function loadData(range) {
      showLoading();
      try {
        const res = await fetch('/api/news?range=' + range);
        if (!res.ok) throw new Error('서버 오류 ' + res.status);
        const data = await res.json();
        clientCache[range] = data;

        // 임시 디버그: 데이터 구조 화면 출력
        document.getElementById('loading').style.display = 'none';
        const app = document.getElementById('app');
        app.style.display = 'block';
        app.innerHTML = '<div style="padding:16px;font-size:12px;background:white;border-radius:8px;">'
          + '<b>수신 데이터 키:</b> ' + JSON.stringify(Object.keys(data)) + '<br><br>'
          + '<b>keywords 수:</b> ' + (data.keywords?.length || 'UNDEFINED') + '<br>'
          + '<b>categories 키:</b> ' + JSON.stringify(Object.keys(data.categories||{})) + '<br>'
          + '<b>errors:</b> ' + JSON.stringify(data.errors)
          + '</div>';

      } catch (e) { showFetchError(e.message + ' / ' + e.stack); }
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
      return (d.getMonth()+1) + '.' + String(d.getDate()).padStart(2,'0');
    }

    function esc(s) {
      return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;')
                          .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    }

    function toggleKw(id) {
      const el  = document.getElementById('al-' + id);
      const row = document.getElementById('kr-' + id);
      if (!el) return;
      const open = el.classList.toggle('open');
      row.querySelector('.kw-toggle').textContent = open ? '▲' : '▼';
    }

    function buildPrompt(data, range) {
      const period = PROMPT_GUIDE[range];
      const today  = new Date().toLocaleDateString('ko-KR',
        {year:'numeric', month:'2-digit', day:'2-digit'});
      let txt  = `아래는 ${today} 기준 ${period} 제약 업계 키워드별 뉴스입니다.\n`;
      txt += `CE기획팀 관점에서 분류별 핵심 내용을 분석해주세요.\n\n`;
      txt += `[분석 기준]\n`;
      txt += `- 자사 직결: 보령 관련 사업 영향도 중심으로 서술\n`;
      txt += `- 시장 영향: 정책·급여·경쟁사 동향, 대응 필요 여부 중심\n`;
      txt += `- 업계 동향: 중장기 시사점 중심\n\n`;
      txt += `[출력 형식] 주간 뉴스레터 메일 바디 / 우선순위 높은 항목부터\n`;
      txt += `기사가 0건인 키워드는 생략합니다.\n`;
      txt += `\n${'='.repeat(40)}\n\n`;

      for (const [cat, kws] of Object.entries(data.categories)) {
        const lines = [];
        for (const kw of kws) {
          const items = data.data[kw] || [];
          if (!items.length) continue;
          lines.push(`[${kw}] ${items.length}건`);
          items.forEach(a => lines.push(`  - ${a.title} (${a.site})`));
        }
        if (!lines.length) continue;
        txt += `=== ${cat} ===\n\n` + lines.join('\n') + '\n\n';
      }
      return txt.trim();
    }

    async function copyPrompt(data, range) {
      const btn = document.getElementById('copy-btn');
      try {
        await navigator.clipboard.writeText(buildPrompt(data, range));
        btn.textContent = '✅ 복사됨';
        btn.classList.add('copied');
        setTimeout(() => { btn.textContent = '📋 프롬프트 복사'; btn.classList.remove('copied'); }, 2000);
      } catch {
        btn.textContent = '❌ 복사 실패';
        setTimeout(() => { btn.textContent = '📋 프롬프트 복사'; }, 2000);
      }
    }

    function render(data, range) {
      document.getElementById('loading').style.display = 'none';
      const app = document.getElementById('app');
      app.style.display = 'block';

      const total = data.keywords.reduce((s,k) => s + (data.data[k]?.length||0), 0);

      let html = '<div class="status-bar"><div class="status-left">';
      html += '<span class="badge">📅 ' + LABEL[range] + '</span>';
      html += '<span class="badge">📰 ' + total + '건</span>';
      if (data.errors?.length)
        html += '<span class="badge badge-error">⚠️ ' + data.errors.length + '개 소스 오류</span>';
      html += '</div><button class="refresh-btn" onclick="refresh()">🔄 새로고침</button></div>';

      if (data.errors?.length)
        html += '<div class="error-banner">수집 실패: ' + esc(data.errors.join(', ')) + '</div>';

      if (range === 'today') {
        let hasAny = false;
        for (const kw of data.keywords) {
          const items = data.data[kw];
          if (!items?.length) continue;
          hasAny = true;
          html += '<div class="kw-section"><div class="kw-section-header">'
                + '<span class="kw-name">' + esc(kw) + '</span>'
                + '<span class="kw-count">' + items.length + '</span>'
                + '</div><div class="cards">';
          for (const item of items) {
            html += '<div class="card"><div class="card-title">'
                  + '<a href="' + esc(item.link) + '" target="_blank" rel="noopener">'
                  + esc(item.title||'(제목 없음)') + '</a></div>'
                  + '<div class="card-meta"><span class="src-tag">' + esc(item.site) + '</span>'
                  + '<span>' + fmtDate(item.date) + '</span></div></div>';
          }
          html += '</div></div>';
        }
        if (!hasAny)
          html += '<div class="empty">📭 오늘 기간 내 해당 키워드 뉴스가 없습니다.</div>';

      } else {
        html += '<div class="prompt-bar">'
              + '<div class="prompt-bar-txt"><strong>📋 AI 요약 프롬프트</strong>'
              + LABEL[range] + ' 뉴스 전체를 Claude 분석용 프롬프트로 추출합니다.</div>'
              + '<button class="copy-btn" id="copy-btn" '
              + 'onclick="copyPrompt(clientCache[currentTab], currentTab)">'
              + '📋 프롬프트 복사</button></div>';

        let hasAny = false;
        let catIdx = 0;

        for (const [cat, kws] of Object.entries(data.categories)) {
          const catTotal = kws.reduce((s,k) => s + (data.data[k]?.length||0), 0);
          const cc = CAT_CLASS[catIdx] || 'c1';
          const maxCount = Math.max(...kws.map(k => data.data[k]?.length||0), 1);

          html += '<div class="cat-section">';
          html += '<div class="cat-header ' + cc + '">' + esc(cat)
                + '<span class="cat-total">' + catTotal + '건</span></div>';
          html += '<div class="kw-list">';

          for (const kw of kws) {
            const items = data.data[kw] || [];
            const cnt  = items.length;
            const uid  = esc(kw).replace(/\s/g,'_');
            const barW = cnt ? Math.round((cnt / maxCount) * 100) : 0;
            const empty = cnt === 0;

            html += '<div class="kw-row' + (empty ? ' empty' : '') + '" id="kr-' + uid + '" '
                  + (!empty ? 'onclick="toggleKw(\'' + uid + '\')"' : '') + '>';
            html += '<span class="kw-label">' + esc(kw) + '</span>';
            html += '<div class="kw-bar-wrap"><div class="kw-bar" style="width:' + barW + '%"></div></div>';
            html += '<span class="kw-num">' + (cnt||'-') + '</span>';
            if (!empty) html += '<span class="kw-toggle">▼</span>';
            html += '</div>';

            if (!empty) {
              hasAny = true;
              html += '<div class="article-list" id="al-' + uid + '">';
              for (const item of items) {
                html += '<div class="article-item">'
                      + '<a href="' + esc(item.link) + '" target="_blank" rel="noopener">'
                      + esc(item.title||'(제목 없음)') + '</a>'
                      + '<div class="article-meta">'
                      + '<span class="src-tag">' + esc(item.site) + '</span>'
                      + '<span>' + fmtDate(item.date) + '</span></div></div>';
              }
              html += '</div>';
            }
          }
          html += '</div></div>';
          catIdx++;
        }
        if (!hasAny)
          html += '<div class="empty">📭 ' + LABEL[range] + ' 기간 내 해당 키워드 뉴스가 없습니다.</div>';
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
      app.innerHTML = '<div class="error-banner">⚠️ 데이터를 불러오지 못했습니다: ' + esc(msg) + '</div>';
    }

    loadData('today');
  </script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def home():
    return HTML
