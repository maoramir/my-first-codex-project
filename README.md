# my-first-codex-project

Car deal checker MVP with FastAPI + CSV data source.

## Run locally (backend app)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` for the web app.
Open `http://127.0.0.1:8000/docs` for API docs.

## GitHub Pages (No Backend)

The GitHub Pages app is fully static and runs from:
- `docs/index.html`
- `docs/data/car_ads.csv`

To publish:
1. Push this repo to GitHub.
2. Open repository settings -> **Pages**.
3. Source: deploy from branch `main`, folder `/docs`.
4. Open:
   `https://maoramir.github.io/my-first-codex-project/`
