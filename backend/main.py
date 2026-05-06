"""Cookie Conscious API."""

import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from cookies.browser import discover_profiles, scan_browser
from cookies.categorizer import categorize_all
from cookies.models import CategorizedCookie
from cookies.parser import parse_json_export
from consent.classifier import classify_consent
from consent.models import DomainConsent
from stories.builder import default_engine
from stories.models import Story

app = FastAPI(title="Cookie Conscious", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)



class AnalyzeRequest(BaseModel):
    cookies: list[dict]


class ScanRequest(BaseModel):
    browser: str = "chrome"
    profile: str = "all"


class ProfileInfo(BaseModel):
    browser: str
    profile_name: str
    cookie_count: int


class AnalyzeResponse(BaseModel):
    cookies: list[CategorizedCookie]
    consent: list[DomainConsent]
    story: Story
    scan_timestamp: float | None = None


_last_scan: dict[str, set[tuple[str, str]]] = {}


def _build_response(categorized: list[CategorizedCookie]) -> AnalyzeResponse:
    consent = classify_consent(categorized)
    story = default_engine.build(categorized, consent)
    return AnalyzeResponse(
        cookies=categorized, consent=consent, story=story,
        scan_timestamp=time.time(),
    )


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/browser/profiles", response_model=list[ProfileInfo])
def list_profiles():
    return [
        ProfileInfo(
            browser=p.browser,
            profile_name=p.profile_name,
            cookie_count=p.cookie_count,
        )
        for p in discover_profiles()
    ]


@app.post("/api/browser/scan", response_model=AnalyzeResponse)
def scan(req: ScanRequest):
    raw = scan_browser(browser=req.browser, profile=req.profile)
    categorized = categorize_all(raw)

    key = f"{req.browser}:{req.profile}"
    _last_scan[key] = {(c.raw.name, c.raw.domain) for c in categorized}

    return _build_response(categorized)


class PollResponse(BaseModel):
    changed: bool
    new_cookie_count: int
    removed_cookie_count: int
    total_cookie_count: int
    result: AnalyzeResponse | None = None


@app.post("/api/browser/poll", response_model=PollResponse)
def poll(req: ScanRequest):
    raw = scan_browser(browser=req.browser, profile=req.profile)
    categorized = categorize_all(raw)

    key = f"{req.browser}:{req.profile}"
    current = {(c.raw.name, c.raw.domain) for c in categorized}
    prev = _last_scan.get(key, set())

    new_cookies = current - prev
    removed_cookies = prev - current
    changed = bool(new_cookies or removed_cookies)

    _last_scan[key] = current

    result = _build_response(categorized) if changed else None
    return PollResponse(
        changed=changed,
        new_cookie_count=len(new_cookies),
        removed_cookie_count=len(removed_cookies),
        total_cookie_count=len(current),
        result=result,
    )


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    raw = parse_json_export(req.cookies)
    categorized = categorize_all(raw)
    return _build_response(categorized)
