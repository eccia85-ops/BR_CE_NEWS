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
      --cat1-bg: #fff1f2; --cat1-txt: #be123c; --cat1-bd: #fda4af;
      --cat2-bg: #fffbeb; --cat2-txt: #b45309; --cat2-bd: #fcd34d;
      --cat3-bg: #f0fdf4; --cat3-txt: #166534; --cat3-bd: #86efac;
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
    .status-left { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
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
      background: #1e293b; border-radius: 10px; padding: 12px 16px;
      margin-bottom: 16px; display: flex; justify-content: space-between;
      align-items: center; gap: 12px;
    }
    .prompt-bar-txt { font-size: 12px; color: #94a3b8; line-height: 1.5; }
    .prompt-bar-txt b { color: #e2e8f0; display: block; margin-bottom: 2px; }
    .copy-btn {
      background: var(--primary); color: white; border: none;
      border-radius: 7px; padding: 8px 16px; font-size: 13px;
      font-weight: 600; cursor: pointer; white-space: nowrap;
    }
    .copy-btn:active { transform: scale(0.97); }
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
      border-bottom: 1px solid var(--border);
      gap: 10px; cursor: pointer;
    }
    .kw-row:last-child { border-bottom: none; }
    .kw-row:hover { background: var(--badge-bg); }
    .kw-row.empty { cursor: default; opacity: 0.4; padding-top: 6px; padding-bottom: 6px; }
    .kw-row.empty:hover { background: white; }
    .kw-row.empty .kw-bar-wrap { display: none; }
    .kw-row.empty .kw-num { display: none; }
    .kw-label { font-size: 14px; font-weight: 600; min-width: 80px; }
    .kw-bar-wrap { flex: 1; height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; }
    .kw-bar { height: 100%; border-radius: 3px; background: var(--primary); }
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
    .kw-name { font-size: 15px; font-weight: 700; color: var(--text); }
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
    <div style="position:absolute;top:14px;right:16px;">
      <button onclick="location.href='/manage'"
        style="background:rgba(255,255,255,0.15);border:none;color:white;
               border-radius:6px;padding:6px 12px;font-size:13px;cursor:pointer;">
        ⚙️ 관리
      </button>
    </div>
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
    var NL = String.fromCharCode(10);
    var currentTab = 'today';
    var clientCache = {};
    var LABEL = { today: '오늘', week: '최근 7일', month: '최근 30일' };
    var CAT_CLASS = ['c1', 'c2', 'c3'];

    function switchTab(tab) {
      var tabs = document.querySelectorAll('.tab');
      for (var i = 0; i < tabs.length; i++) tabs[i].classList.remove('active');
      document.getElementById('tab-' + tab).classList.add('active');
      currentTab = tab;
      if (clientCache[tab]) render(clientCache[tab], tab);
      else loadData(tab);
    }

    function loadData(range) {
      showLoading();
      fetch('/api/news?range=' + range)
        .then(function(res) {
          if (!res.ok) throw new Error('서버 오류 ' + res.status);
          return res.json();
        })
        .then(function(data) {
          clientCache[range] = data;
          render(data, range);
        })
        .catch(function(e) {
          showFetchError(e.message);
        });
    }

    function refresh() {
      delete clientCache[currentTab];
      loadData(currentTab);
    }

    function toggleKw(el) {
      var uid  = el.getAttribute('data-uid');
      var alEl = document.getElementById('al-' + uid);
      var tog  = el.querySelector('.kw-toggle');
      if (!alEl) return;
      var isOpen = alEl.classList.contains('open');
      alEl.classList.toggle('open');
      if (tog) tog.textContent = isOpen ? '▼' : '▲';
    }

    function buildPrompt(data, range) {
      var period = range === 'week' ? '최근 7일' : '최근 30일';
      var today  = new Date().toLocaleDateString('ko-KR',
        { year: 'numeric', month: '2-digit', day: '2-digit' });
      var lines = [];
      lines.push('아래는 ' + today + ' 기준 ' + period + ' 제약 업계 키워드별 뉴스입니다.');
      lines.push('CE기획팀 관점에서 분류별 핵심 내용을 분석해주세요.');
      lines.push('');
      lines.push('[분석 기준]');
      lines.push('- 자사 직결: 보령 관련 사업 영향도 중심으로 서술');
      lines.push('- 시장 영향: 정책, 급여, 경쟁사 동향 및 대응 필요 여부 중심');
      lines.push('- 업계 동향: 중장기 시사점 중심');
      lines.push('');
      lines.push('[출력 형식] 주간 뉴스레터 메일 바디 / 우선순위 높은 항목부터');
      lines.push('기사가 0건인 키워드는 생략합니다.');
      lines.push('');
      lines.push('========================================');
      lines.push('');
      var catKeys = Object.keys(data.categories);
      for (var ci = 0; ci < catKeys.length; ci++) {
        var cat      = catKeys[ci];
        var articles = data.cat_data[cat] || [];
        if (!articles.length) continue;
        lines.push('=== ' + cat + ' === (' + articles.length + '건)');
        lines.push('');
        for (var ai = 0; ai < articles.length; ai++) {
          var art  = articles[ai];
          var tags = art.tags ? art.tags.join(', ') : '';
          lines.push('- ' + art.title + ' (' + art.site + ')');
          if (tags) lines.push('  키워드: ' + tags);
        }
        lines.push('');
      }
      return lines.join(NL);
    }

    function copyPrompt() {
      var btn  = document.getElementById('copy-btn');
      var data = clientCache[currentTab];
      if (!data || !btn) return;
      var txt = buildPrompt(data, currentTab);
      navigator.clipboard.writeText(txt)
        .then(function() {
          btn.textContent = '✅ 복사됨';
          btn.style.background = '#166534';
          setTimeout(function() {
            btn.textContent = '📋 프롬프트 복사';
            btn.style.background = '';
          }, 2000);
        })
        .catch(function() {
          btn.textContent = '❌ 실패';
          setTimeout(function() {
            btn.textContent = '📋 프롬프트 복사';
          }, 2000);
        });
    }

    function fmtDate(raw) {
      if (!raw) return '';
      var d = new Date(raw);
      if (isNaN(d)) return '';
      var now  = new Date();
      var diff = Math.floor((now - d) / 60000);
      if (diff < 1)    return '방금';
      if (diff < 60)   return diff + '분 전';
      if (diff < 1440) return Math.floor(diff / 60) + '시간 전';
      return (d.getMonth() + 1) + '.' + String(d.getDate()).padStart(2, '0');
    }

    function esc(s) {
      return String(s || '')
        .replace(/&/g, '&amp;').replace(/</g, '&lt;')
        .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    function renderToday(data) {
      var html    = '';
      var hasAny  = false;
      var catKeys = Object.keys(data.categories);

      for (var ci = 0; ci < catKeys.length; ci++) {
        var cat      = catKeys[ci];
        var cc       = CAT_CLASS[ci] || 'c1';
        var articles = data.cat_data[cat] || [];
        if (!articles.length) continue;
        hasAny = true;

        html += '<div class="cat-section">';
        html += '<div class="cat-header ' + cc + '">'
              + esc(cat)
              + '<span class="cat-total">' + articles.length + '건</span>'
              + '</div>';
        html += '<div class="kw-list">';

        for (var ai = 0; ai < articles.length; ai++) {
          var art = articles[ai];
          html += '<div class="article-item" style="padding:10px 14px;">'
                + '<a href="' + esc(art.link) + '" target="_blank" rel="noopener">'
                + esc(art.title || '(제목 없음)') + '</a>'
                + '<div class="article-meta">'
                + '<span class="src-tag">' + esc(art.site) + '</span>'
                + '<span>' + fmtDate(art.date) + '</span>';
          for (var ti = 0; ti < art.tags.length; ti++) {
            html += '<span style="background:#e8eefb;color:#1a56db;border-radius:4px;'
                  + 'padding:1px 6px;font-size:11px;">＃' + esc(art.tags[ti]) + '</span>';
          }
          html += '</div></div>';
        }
        html += '</div></div>';
      }

      if (!hasAny)
        html += '<div class="empty">📭 오늘 기간 내 해당 키워드 뉴스가 없습니다.</div>';
      return html;
    }

    function renderCat(data, range) {
      var html = '';
      html += '<div class="prompt-bar">';
      html += '<div class="prompt-bar-txt">'
            + '<b>📋 AI 요약 프롬프트</b>'
            + LABEL[range] + ' 뉴스를 Claude 분석용 프롬프트로 추출합니다.'
            + '</div>';
      html += '<button id="copy-btn" class="copy-btn" onclick="copyPrompt()">'
            + '📋 프롬프트 복사</button>';
      html += '</div>';

      var cats    = data.categories;
      var catKeys = Object.keys(cats);
      var hasAny  = false;

      for (var ci = 0; ci < catKeys.length; ci++) {
        var cat      = catKeys[ci];
        var cc       = CAT_CLASS[ci] || 'c1';
        var articles = data.cat_data[cat] || [];
        if (!articles.length) continue;
        hasAny = true;

        html += '<div class="cat-section">';
        html += '<div class="cat-header ' + cc + '">'
              + esc(cat)
              + '<span class="cat-total">' + articles.length + '건</span>'
              + '</div>';
        html += '<div class="kw-list">';

        for (var ai = 0; ai < articles.length; ai++) {
          var art = articles[ai];
          html += '<div class="article-item" style="padding:10px 14px;">'
                + '<a href="' + esc(art.link) + '" target="_blank" rel="noopener">'
                + esc(art.title || '(제목 없음)') + '</a>'
                + '<div class="article-meta">'
                + '<span class="src-tag">' + esc(art.site) + '</span>'
                + '<span>' + fmtDate(art.date) + '</span>';
          for (var ti = 0; ti < art.tags.length; ti++) {
            html += '<span style="background:#e8eefb;color:#1a56db;border-radius:4px;'
                  + 'padding:1px 6px;font-size:11px;">＃' + esc(art.tags[ti]) + '</span>';
          }
          html += '</div></div>';
        }
        html += '</div></div>';
      }

      if (!hasAny)
        html += '<div class="empty">📭 ' + LABEL[range] + ' 기간 내 해당 키워드 뉴스가 없습니다.</div>';
      return html;
    }

    function render(data, range) {
      document.getElementById('loading').style.display = 'none';
      var app = document.getElementById('app');
      app.style.display = 'block';

      var total = 0;
      var catKeys = Object.keys(data.cat_data || {});
      for (var ci = 0; ci < catKeys.length; ci++) {
        var arr = data.cat_data[catKeys[ci]];
        if (arr) total += arr.length;
      }

      var html = '<div class="status-bar"><div class="status-left">';
      html += '<span class="badge">📅 ' + LABEL[range] + '</span>';
      html += '<span class="badge">📰 ' + total + '건</span>';
      if (data.errors && data.errors.length)
        html += '<span class="badge badge-error">⚠️ ' + data.errors.length + '개 소스 오류</span>';
      html += '</div>';
      html += '<button class="refresh-btn" onclick="refresh()">🔄 새로고침</button>';
      html += '</div>';

      if (data.errors && data.errors.length)
        html += '<div class="error-banner">수집 실패: ' + esc(data.errors.join(', ')) + '</div>';

      if (range === 'today') {
        html += renderToday(data);
      } else {
        html += renderCat(data, range);
      }

      app.innerHTML = html;
    }

    function showLoading() {
      document.getElementById('loading').style.display = 'block';
      document.getElementById('app').style.display = 'none';
    }

    function showFetchError(msg) {
      document.getElementById('loading').style.display = 'none';
      var app = document.getElementById('app');
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
