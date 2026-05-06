# Cookie Conscious
A local web dashboard that reads your browser's cookie metadata, classifies each cookie's consent type, and reconstructs the behavioral profile a third party could build from your data. All analysis runs locally — no data leaves your machine.

## Quick Start

You need **Python 3.10+** and **Node 22+** (use `nvm use 22` if needed).

**1. Start the backend**

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at http://localhost:8000.

**2. Start the frontend** (in a second terminal)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173.

**3. Use the app**

- **Scan browser cookies**: Close Chrome, then click a profile button on the landing page. The app reads cookie metadata directly from Chrome's SQLite database (names, domains, flags — never values).
- **Upload cookie JSON**: Click "Or upload/paste cookie JSON manually" to use an exported `cookies.json` from tools like Cookie-Editor.

## What It Shows

- **Consent classification**: Each domain is classified as tacit (no prompt shown), implied ("by using this site..."), or explicit (user opted in). Shown as a distribution chart and per-row badges in the cookie table.
- **Story reconstruction**: 15 behavioral archetypes (job seeker, student, traveler, etc.) activate when 3+ independent domain signals converge. Composite inferences emerge when multiple archetypes combine. Every conclusion links back to the specific cookies that produced it.
- **Per-company insights**: What each tracker company (Google, Meta, etc.) can learn from their cookies on your machine.
- **Live monitoring**: After a scan, the app polls every 60 seconds and shows new/removed cookies as you browse.

## Project Structure

```
backend/
  main.py # FastAPI app
  cookies/ # Parsing, categorization, browser DB reading
  consent/ # Tacit / implied / explicit classification
  stories/ # Archetype detection, company stories, composites

frontend/
  src/
    App.tsx # Scan/upload flow
    components/ # Dashboard, CookieTable, ProfileReconstruction, etc.
    api/client.ts # API client
    types/index.ts # TypeScript types mirroring backend models
```

## Notes

- Chrome must be closed during a scan (the cookie DB is locked while Chrome is running).
- Only Chrome is supported. The `backend/cookies/browser.py` module reads from Chrome's default profile paths on macOS.
- Cookie values are never read — they are encrypted by Chrome and are not needed for analysis.
