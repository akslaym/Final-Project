"""Three-tier cookie categorization: known name, known domain, name heuristics."""

import json
from pathlib import Path

from .domain_db import lookup_domain
from .models import CategorizedCookie, CookieCategory, RawCookie

_KNOWN_COOKIES: list[dict] | None = None


def _load_known_cookies() -> list[dict]:
    global _KNOWN_COOKIES
    if _KNOWN_COOKIES is None:
        db_path = Path(__file__).parent.parent / "data" / "known_cookies.json"
        with open(db_path) as f:
            _KNOWN_COOKIES = json.load(f)
    return _KNOWN_COOKIES


def _match_known_cookie(cookie: RawCookie) -> dict | None:
    for known in _load_known_cookies():
        name_match = (
            cookie.name == known["name_pattern"]
            or cookie.name.startswith(known["name_pattern"])
        )
        domain_match = (
            known["domain_pattern"] == "*"
            or cookie.domain.endswith(known["domain_pattern"].lstrip("."))
        )
        if name_match and domain_match:
            return known
    return None


def _heuristic_category(cookie: RawCookie) -> tuple[CookieCategory, str, str | None]:
    name = cookie.name.lower()

    # Advertising signals
    ad_signals = [
        "ad", "ads", "adid", "track", "pixel", "campaign", "utm",
        "click", "conv", "retarget", "dsp", "bid", "imp", "rtb",
        "targeting", "remarketing", "sponsor",
    ]
    if any(s in name for s in ad_signals):
        return CookieCategory.ADVERTISING, "Likely advertising/tracking based on name pattern", None

    # Analytics signals
    analytics_signals = [
        "analytics", "_ga", "_gid", "_gat", "stat", "metric", "_hj",
        "visitor", "pageview", "segment", "amplitude", "mixpanel",
        "heap", "pendo", "measure", "collect",
    ]
    if any(s in name for s in analytics_signals):
        return CookieCategory.ANALYTICS, "Likely analytics based on name pattern", None

    # Session signals
    session_signals = [
        "sess", "sid", "session", "jsessionid", "phpsessid",
        "asp.net_sessionid", "connect.sid", "laravel_session",
    ]
    if any(s in name for s in session_signals):
        return CookieCategory.SESSION, "Session management cookie", None

    # Auth signals
    auth_signals = [
        "auth", "token", "login", "csrf", "xsrf", "shib",
        "saml", "oauth", "jwt", "sso", "credential",
    ]
    if any(s in name for s in auth_signals):
        return CookieCategory.AUTHENTICATION, "Authentication or security cookie", None

    # Preference signals
    pref_signals = [
        "pref", "lang", "locale", "theme", "consent", "opt",
        "cookie_notice", "gdpr", "ccpa", "notice", "accepted",
    ]
    if any(s in name for s in pref_signals):
        return CookieCategory.PERSONALIZATION, "User preferences or consent choice", None

    # Social signals
    social_signals = ["fb", "tw", "li_", "pin_", "ig_", "snap", "share"]
    if any(s in name for s in social_signals):
        return CookieCategory.SOCIAL_MEDIA, "Likely social media related based on name pattern", None

    if "deprecation" in name or "receive-cookie" in name:
        return CookieCategory.FUNCTIONAL, "Chrome Privacy Sandbox origin trial marker", None

    return CookieCategory.UNKNOWN, "Purpose could not be determined automatically", None


def categorize(cookie: RawCookie) -> CategorizedCookie:
    known = _match_known_cookie(cookie)
    if known:
        return CategorizedCookie(
            raw=cookie,
            category=CookieCategory(known["category"]),
            purpose=known["purpose"],
            vendor=known.get("vendor"),
        )

    domain_info = lookup_domain(cookie.domain)
    if domain_info:
        return CategorizedCookie(
            raw=cookie,
            category=domain_info.category,
            purpose=f"{domain_info.vendor} \u2014 {domain_info.description}",
            vendor=domain_info.vendor,
        )

    category, purpose, vendor = _heuristic_category(cookie)
    return CategorizedCookie(raw=cookie, category=category, purpose=purpose, vendor=vendor)


def categorize_all(cookies: list[RawCookie]) -> list[CategorizedCookie]:
    return [categorize(c) for c in cookies]
