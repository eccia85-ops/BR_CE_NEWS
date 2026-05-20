from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"/>
  <title>CE 뉴스 관리</title>
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
      display: flex; align-items: center; gap: 12px;
    }
    .header h1  { font-size: 17px; font-weight: 700; letter-spacing: -0.3px; }
    .header .sub { font-size: 11px; opacity: 0.75; margin-top: 2px; }
    .back-btn {
      background: rgba(255,255,255,0.15); border: none; color: white;
      border-radius: 6px; padding: 6px 12px; font-size: 13px;
      cursor: pointer; white-space: nowrap;
    }
    .back-btn:active { transform: scale(0.97); }
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
    .content { padding: 16px 14px 40px; max-width: 720px; margin: 0 auto; }
    .section {
      background: white; border: 1px solid var(--border);
      border-radius: 12px; padding: 18px 16px; margin-bottom: 16px;
    }
    .section-title {
      font-size: 15px; font-weight: 700; margin-bottom: 14px;
      padding-bottom: 10px; border-bottom: 1px solid var(--border);
    }
    .cat-block { margin-bottom: 14px; }
    .cat-label {
      font-size: 12px; font-weight: 700; padding: 3px 10px;
      border-radius: 20px; display: inline-block; margin-bottom: 8px;
    }
    .cat-label.c1 { background: var(--cat1-bg); color: var(--cat1-txt); }
    .cat-label.c2 { background: var(--cat2-bg); color: var(--cat2-txt); }
    .cat-label.c3 { background: var(--cat3-bg); color: var(--cat3-txt); }
    .kw-tags { display: flex; flex-wrap: wrap; gap: 6px; }
    .kw-tag {
      background: var(--badge-bg); color: var(--text);
      border-radius: 6px; padding: 4px 10px; font-size: 13px;
    }
    .search-row {
      display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap;
    }
    .search-input {
      flex: 1; min-width: 160px; padding: 9px 12px;
      border: 1px solid var(--border); border-radius: 8px;
      font-size: 14px; outline: none;
    }
    .search-input:focus { border-color: var(--primary); }
    .range-tabs {
      display: flex; gap: 6px; margin-bottom: 12px;
    }
    .range-tab {
      padding: 6px 14px; border: 1px solid var(--border);
      border-radius: 20px; font-size: 13px; cursor: pointer;
      background: white; color: var(--sub);
    }
    .range-tab.active {
      background: var(--primary); color: white; border-color: var(--primary);
      font-weight: 600;
    }
    .search-btn {
      background: var(--primary); color: white; border: none;
      border-radius: 8px; padding: 9px 18px; font-size: 14px;
      font-weight: 600; cursor: pointer; white-space: nowrap;
    }
    .search-btn:active { transform: scale(0.97); }
    .result-count {
      font-size: 12px; color: var(--sub); margin-bottom: 10px;
    }
    .result-item {
      padding: 9px 0; border-bottom: 1px solid var(--border); font-size: 13px;
    }
    .result-item:last-child { border-bottom: none; }
    .result-item a { color: var(--text); text-decoration: none; line-height: 1.5; }
    .result-item a:hover { color: var(--primary); text-decoration: underline; }
    .result-meta {
      font-size: 11px; color: var(--sub); margin-top: 3px; display: flex; gap: 6px; flex-wrap: wrap;
    }
    .src-tag {
      background: var(--badge-bg); border-radius: 4px;
      padding: 1px 6px; font-size: 11px; color: #374151;
    }
    .contact-box {
      background: var(--badge-bg); border-radius: 8px;
      padding: 14px 16px; font-size: 13px; line-height: 1.8;
    }
    .contact-box a { color: var(--primary); text-decoration: none; }
    .notice {
      font-size: 12px; color: var(--sub); margin-top: 10px; line-height: 1.6;
    }
    .loading-inline {
      font-size: 13px; color: var(--sub); padding: 16px 0; text-align: center;
    }
    .empty-result {
      text-align: center; padding: 24px; color: var(--sub); font-size: 13px;
    }
    .pane { display: none; }
    .pane.active { display: block; }
  </style>
</head>
<body>
  <div class="header">
    <button class="back-btn" onclick="location.href='/'">← 뉴스</button>
    <div>
      <h1>⚙️ 관리 페이지</h1>
      <div class="sub">CE기획팀 · 키워드 관리 및 탐색</div>
    </div>
  </div>

  <div class="tabs">
    <button class="tab active" id="tab-kw"     onclick="switchTab('kw')">키워드 현황</button>
    <button class="tab"        id="tab-search" onclick="switchTab('search')">검색</button>
    <button class="tab"        id="tab-req"    onclick="switchTab('req')">요청</button>
  </div>

  <div class="content">

    <!-- 키워드 현황 -->
    <div class="pane active" id="pane-kw">
      <div class="section">
        <div class="section-title">📋 등록 키워드 현황</div>
        <div id="kw-list"><div class="loading-inline">로딩 중…</div></div>
      </div>

      <div class="section">
        <div class="section-title">📡 수집 소스 현황</div>
        <div id="src-list"><div class="loading-inline">로딩 중…</div></div>
        <div style="margin-top:12px;padding-top:12px;border-top:1px solid var(--border);">
          <div style="font-size:12px;color:var(--sub);margin-bottom:8px;">비활성 소스</div>
          <div style="font-size:13px;opacity:0.5;margin-bottom:6px;">
            <span style="color:#991b1b;font-weight:700;">❌</span> 데일리팜 (수집 실패)
          </div>
          <div style="font-size:13px;opacity:0.5;">
            <span style="color:#991b1b;font-weight:700;">❌</span> 메디칼타임즈 (수집 실패)
          </div>
        </div>
      </div>

    </div>

    <!-- 검색 -->
    <div class="pane" id="pane-search">
      <div class="section">
        <div class="section-title">🔍 키워드 탐색</div>
        <div class="range-tabs">
          <button class="range-tab active" id="rt-today" onclick="setRange('today')">오늘</button>
          <button class="range-tab"        id="rt-week"  onclick="setRange('week')">주간</button>
          <button class="range-tab"        id="rt-month" onclick="setRange('month')">월간</button>
        </div>
        <div class="search-row">
          <input class="search-input" id="search-input" type="text"
                 placeholder="검색어 입력 (예: 비만, GLP-1)"/>
          <button class="search-btn" onclick="doSearch()">검색</button>
        </div>
        <div id="search-result"></div>
      </div>
    </div>

    <!-- 요청 -->
    <div class="pane" id="pane-req">
      <div class="section">
        <div class="section-title">📬 수정 · 배포 요청</div>
        <div class="contact-box">
          <b>CE기획팀 최재성</b><br>
          E-mail: <a href="mailto:jschoi1206@boryung.co.kr">jschoi1206@boryung.co.kr</a>
        </div>
        <div class="notice">
          키워드 추가/삭제, 소스 변경, 기능 개선 요청은 위 이메일로 문의해 주세요.<br>
          알림 기능은 추후 업데이트 예정입니다.
        </div>
      </div>
    </div>

  </div>

  <script>
    var currentRange = 'today';
    var CAT_CLASS = ['c1', 'c2', 'c3'];

    function switchTab(tab) {
      var tabs = document.querySelectorAll('.tab');
      for (var i = 0; i < tabs.length; i++) tabs[i].classList.remove('active');
      document.getElementById('tab-' + tab).classList.add('active');
      var panes = document.querySelectorAll('.pane');
      for (var i = 0; i < panes.length; i++) panes[i].classList.remove('active');
      document.getElementById('pane-' + tab).classList.add('active');
    }

    function setRange(range) {
      currentRange = range;
      var rtabs = document.querySelectorAll('.range-tab');
      for (var i = 0; i < rtabs.length; i++) rtabs[i].classList.remove('active');
      document.getElementById('rt-' + range).classList.add('active');
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

    function loadKeywords() {
      fetch('/api/news?range=today')
        .then(function(res) { return res.json(); })
        .then(function(data) {
          var cats    = data.categories;
          var catKeys = Object.keys(cats);
          var html    = '';
          for (var ci = 0; ci < catKeys.length; ci++) {
            var cat = catKeys[ci];
            var kws = cats[cat];
            var cc  = CAT_CLASS[ci] || 'c1';
            html += '<div class="cat-block">';
            html += '<span class="cat-label ' + cc + '">' + esc(cat) + '</span>';
            html += '<div class="kw-tags">';
            for (var ki = 0; ki < kws.length; ki++) {
              html += '<span class="kw-tag">' + esc(kws[ki]) + '</span>';
            }
            html += '</div></div>';
          }
          document.getElementById('kw-list').innerHTML = html;

          var sources  = data.sources || [];
          var srcHtml  = '<div style="display:flex;flex-direction:column;gap:8px;">';
          for (var si = 0; si < sources.length; si++) {
            srcHtml += '<div style="font-size:13px;">'
                     + '<span style="color:#166534;font-weight:700;">✅</span> '
                     + esc(sources[si]) + '</div>';
          }
          srcHtml += '</div>';
          document.getElementById('src-list').innerHTML = srcHtml;
        })
        .catch(function() {
          document.getElementById('kw-list').innerHTML =
            '<div class="empty-result">키워드 목록을 불러오지 못했습니다.</div>';
          document.getElementById('src-list').innerHTML = '';
        });
    }

    function doSearch() {
      var query = document.getElementById('search-input').value.trim();
      if (!query) return;

      var resultEl = document.getElementById('search-result');
      resultEl.innerHTML = '<div class="loading-inline">검색 중…</div>';

      fetch('/api/articles?range=' + currentRange)
        .then(function(res) { return res.json(); })
        .then(function(data) {
          var all     = data.articles || [];
          var results = [];
          for (var i = 0; i < all.length; i++) {
            if (all[i].title && all[i].title.indexOf(query) !== -1) {
              results.push(all[i]);
            }
          }
          if (!results.length) {
            resultEl.innerHTML = '<div class="empty-result">📭 검색 결과가 없습니다.</div>';
            return;
          }
          var html = '<div class="result-count">' + results.length + '건 검색됨</div>';
          for (var i = 0; i < results.length; i++) {
            var art = results[i];
            html += '<div class="result-item">'
                  + '<a href="' + esc(art.link) + '" target="_blank" rel="noopener">'
                  + esc(art.title || '(제목 없음)') + '</a>'
                  + '<div class="result-meta">'
                  + '<span class="src-tag">' + esc(art.site) + '</span>'
                  + '<span>' + fmtDate(art.date) + '</span>'
                  + '</div></div>';
          }
          resultEl.innerHTML = html;
        })
        .catch(function() {
          resultEl.innerHTML = '<div class="empty-result">검색 중 오류가 발생했습니다.</div>';
        });
    }

    document.getElementById('search-input').addEventListener('keydown', function(e) {
      if (e.key === 'Enter') doSearch();
    });

    loadKeywords();
  </script>
</body>
</html>"""


@app.get("/manage")
def manage():
    return HTMLResponse(HTML)
