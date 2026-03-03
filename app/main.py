import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.matcher import search_ads
from app.models import SearchRequest

app = FastAPI(title="Car Matcher MVP")

CSV_PATH = "data/car_ads.csv"
TEMPLATES = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

allowed_origins = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return TEMPLATES.TemplateResponse("index.html", {"request": request})


@app.post("/search")
def search(req: SearchRequest) -> dict:
    try:
        results = search_ads(CSV_PATH, req)
        return {"count": len(results), "results": results}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=f"CSV not found at {CSV_PATH}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {exc}") from exc
