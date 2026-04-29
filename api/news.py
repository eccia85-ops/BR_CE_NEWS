from fastapi import FastAPI

app = FastAPI()

@app.get("/api/news")
def news():
    return {
        "message": "news api alive"
    }
