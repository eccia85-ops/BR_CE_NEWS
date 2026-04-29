from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <head>
        <title>CE News Monitor</title>
      </head>
      <body>
        <h1>📊 CE 키워드 뉴스</h1>
        <div id="app"></div>
        <script>
          fetch('/api/news')
            .then(r => r.json())
            .then(data => {
              const app = document.getElementById('app');
              for (const k of data.keywords) {
                const items = data.data[k];
                if (items.length === 0) continue;
                app.innerHTML += `<h2>${k} (${items.length})</h2>`;
                items.forEach(i => {
                  app.innerHTML += `<div>- ${i.title}</div>`;
                });
              }
            });
        </script>
      </body>
    </html>
    """
