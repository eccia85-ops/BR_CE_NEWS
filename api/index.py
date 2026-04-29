from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>CE 키워드 뉴스</title>
<style>
body { font-family: Arial; margin: 20px; }
h1 { margin-bottom: 10px; }
.tabs button {
  margin-right: 8px; padding: 6px 12px; cursor: pointer;
}
.keyword { margin-top: 30px; }
.cards { display: flex; flex-wrap: wrap; gap: 10px; }
.card {
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 10px;
  width: 280px;
  font-size: 14px;
}
.card a { text-decoration: none; color: #000; }
.site { font-size: 12px; color: #666; margin-top: 4px; }
</style>
</head>

<body>
<h1>📊 CE 키워드 뉴스</h1>

<div class="tabs">
  <button onclick="loadView('today')">오늘</button>
  <button onclick="loadView('week')">주간</button>
  <button onclick="loadView('month')">월간</button>
</div>

<div id="app"></div>

<script>
let rawData = null;

async function loadData() {
  const res = await fetch('/api/news');
  rawData = await res.json();
  loadView('today');
}

function loadView(mode) {
  const app = document.getElementById('app');
  app.innerHTML = '';

  for (const keyword of rawData.keywords) {
    const items = rawData.data[keyword];
    if (!items || items.length === 0) continue;

    app.innerHTML += `<div class="keyword"><h2>${keyword}</h2><div class="cards" id="${keyword}"></div></div>`;
    const container = document.getElementById(keyword);

    items.forEach(i => {
      // 날짜 필터는 여기서 확장 가능 (today/week/month)
      container.innerHTML += `
        <div class="card">
          <a href="${i.link}" target="_     <div class="site">${i.site}</div>
        </div>`;
    });
  }
}

loadData();
</script>
</body>
</html>
"""
