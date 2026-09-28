from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.routes import router

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    version="1.0.0",
    description="Generate personalized comic stories and illustrations using Gemini and Stable Diffusion."
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok", "application": "ComicCraft"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
