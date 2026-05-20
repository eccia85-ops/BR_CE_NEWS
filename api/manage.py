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
      overflow-x: hidden;
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
    .content { padding: 16px 14px 40px; max-width: 720px; margin: 0 auto; }
    .section {
      background: white; border: 1px solid var(--border);
      border-radius: 12px; padding: 18px 16px; margin-bottom: 16px;
    }
    .section-title {
      font-size: 15px; font-weight: 700; margin-bottom: 14px;
      padding-bottom: 10px; border-bottom: 1px solid var(--border);
      display: flex; align-items: center; gap: 8px;
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
    .range-select {
      padding: 9px 12px; border: 1px solid var(--border);
      border-radius: 8px; font-size: 14px; background: white;
      color: var(--text); outline: none; cursor: pointer;
    }
    .search-btn {
      background: var(--primary); color: white; border: none;
      border-radius: 8px; padding: 9px 18px; font-size: 14px;
      font-weight: 600; cursor: pointer; white-space: nowrap;
    }
    .search-btn:active { transform: scale(0.97); }
    .search-result { margin-top: 4px; }
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
      font-size: 11px; color: var(--sub); margin-top: 3px; display: flex; gap: 6px;
    }
    .src-tag {
      background: var(--badge-bg); border-radius: 4px;
      padding: 1px 6px; font-size: 11px; color: #374151;
    }
    .empty-result {
      text-align: center; padding: 24px; color: var(--sub); font-size: 13px;
    }
    .contact-box {
      background: var(--badge-bg); border-radius: 8px;
      padding: 14px 16px; font-size: 13px; line-height: 1.8;
    }
    .contact-box b { color: var(--text); }
    .contact-box a { color: var(--primary); text-decoration: none; }
    .notice {
      font-size: 12px; color: var(--sub); margin-top: 10px; line-height: 1.6;
    }
    .loading-inline {
      font-size: 13px; color: var(--sub); padding: 16px 0; text-align: center;
    }
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

  <div class="content">

    <!-- 현재 키워드 목록 -->
    <div class="section">
      <div class="section-title">📋 등록 키워드 현황</div>
      <div id="kw-list"><div class="loading-inline">로딩 중…</div></div>
    </div>

    <!-- 키워드 탐색 -->
    <div class="section">
      <div class="section-title">🔍 키워드 탐색</div>
      <div class="search-row">
        <input class="search-input" id="search-input" type="text"
               placeholder="검색어 입력 (예: 비만, GLP-1)"/>
        <select class="range-select" id="range-select">
          <option value="week">최근 7일</option>
          <option value="month">최근 30일</option>
        </select>
        <button class="search-btn" onclick="doSearch()">검색</button>
      </div>
      <div class="search-result" id="search-result"></div>
    </div>

    <!-- 수정/배포 요청 -->
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

  <script>
    var CAT_CLASS = ['c1', 'c2', 'c3'];
    var cachedData = null;

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
          cachedData = data;
          renderKeywords(data);
        })
        .catch(function() {
          document.getElementById('kw-list').innerHTML =
            '<div class="empty-result">키워드 목록을 불러오지 못했습니다.</div>';
        });
    }

    function renderKeywords(data) {
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
    }

    function doSearch() {
      var query = document.getElementById('search-input').value.trim();
      var range = document.getElementById('range-select').value;
      if (!query) return;

      var resultEl = document.getElementById('search-result');
      resultEl.innerHTML = '<div class="loading-inline">검색 중…</div>';

      fetch('/api/news?range=' + range)
        .then(function(res) { return res.json(); })
        .then(function(data) {
          var allArticles = {};
          var catKeys = Object.keys(data.cat_data || {});
          for (var ci = 0; ci < catKeys.length; ci++) {
            var arts = data.cat_data[catKeys[ci]] || [];
            for (var ai = 0; ai < arts.length; ai++) {
              allArticles[arts[ai].link] = arts[ai];
            }
          }
          var results = [];
          var links   = Object.keys(allArticles);
          for (var li = 0; li < links.length; li++) {
            var art = allArticles[links[li]];
            if (art.title && art.title.indexOf(query) !== -1) {
              results.push(art);
            }
          }
          results.sort(function(a, b) {
            return (b.date || '') > (a.date || '') ? 1 : -1;
          });
          renderResults(results, query);
        })
        .catch(function() {
          resultEl.innerHTML = '<div class="empty-result">검색 중 오류가 발생했습니다.</div>';
        });
    }

    function renderResults(results, query) {
      var resultEl = document.getElementById('search-result');
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
