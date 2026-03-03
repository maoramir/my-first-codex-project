# my-first-codex-project

Car matching MVP with FastAPI + CSV data source.

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` for the web app.
Open `http://127.0.0.1:8000/docs` for API docs.

## Publish a shareable link (GitHub domain + backend)

### 1) Backend deploy (Render)
1. Push this repo to GitHub.
2. In Render, create a **Web Service** from this repo.
3. Use `render.yaml` (or set manually):
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Copy the API URL, for example: `https://car-matcher-api.onrender.com`

### 2) Frontend deploy (GitHub Pages)
1. In GitHub repo settings → **Pages**.
2. Source: deploy from branch `main`, folder `/docs`.
3. Your public URL will look like:
   - `https://maoramir.github.io/my-first-codex-project/`
4. Open the site. When loaded from GitHub Pages, it calls the Render backend automatically.

### 3) CORS
Set backend env var `ALLOWED_ORIGINS` to your GitHub Pages domain, e.g.:
`https://maoramir.github.io`

