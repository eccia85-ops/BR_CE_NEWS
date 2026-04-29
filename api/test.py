from fastapi import FastAPI, Request

app = FastAPI()

@app.api_route("/{path:path}", methods=["GET", "POST"])
async def catch_all(request: Request, path: str):
    return {
        "received_path": request.url.path,
        "matched_path_param": path
    }
