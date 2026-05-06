"""Privacy risk scoring based on data-type sensitivity and cookie properties."""

import time
from enum import Enum

from cookies.models import CategorizedCookie, CookieCategory

from .models import AggregateRisk, CookieRisk


class DataType(str, Enum):
    ID = "id"
    SESSION = "session"
    AUTH = "auth"
    COUNTRY = "country"
    CITY = "city"
    LOGIN = "login"
    NAME = "name"
    EMAIL = "email"
    PASSWORD = "password"
    PHONE = "phone"
    CARD = "card"
    GENDER = "gender"
    ORIENTATION = "orientation"
    BIRTH = "birth"
    BROWSING = "browsing"
    INTERESTS = "interests"
    SOCIAL = "social"
    DEVICE = "device"


DATA_SENSITIVITY: dict[DataType, int] = {
    DataType.PASSWORD: 100,
    DataType.CARD: 98,
    DataType.ORIENTATION: 95,
    DataType.PHONE: 85,
    DataType.EMAIL: 80,
    DataType.BIRTH: 78,
    DataType.GENDER: 70,
    DataType.NAME: 75,
    DataType.LOGIN: 72,
    DataType.AUTH: 65,
    DataType.CITY: 60,
    DataType.COUNTRY: 50,
    DataType.SOCIAL: 55,
    DataType.INTERESTS: 50,
    DataType.BROWSING: 45,
    DataType.ID: 40,
    DataType.DEVICE: 35,
    DataType.SESSION: 30,
}


CATEGORY_DATA_EXPOSURE: dict[CookieCategory, list[DataType]] = {
    CookieCategory.ADVERTISING: [
        DataType.ID, DataType.BROWSING, DataType.INTERESTS,
        DataType.DEVICE, DataType.COUNTRY, DataType.CITY,
    ],
    CookieCategory.ANALYTICS: [
        DataType.ID, DataType.BROWSING, DataType.DEVICE,
        DataType.COUNTRY, DataType.CITY,
    ],
    CookieCategory.SOCIAL_MEDIA: [
        DataType.ID, DataType.SOCIAL, DataType.INTERESTS,
        DataType.NAME, DataType.BROWSING,
    ],
    CookieCategory.AUTHENTICATION: [
        DataType.AUTH, DataType.LOGIN, DataType.ID,
    ],
    CookieCategory.SESSION: [
        DataType.SESSION, DataType.ID,
    ],
    CookieCategory.PERSONALIZATION: [
        DataType.COUNTRY, DataType.DEVICE,
    ],
    CookieCategory.FUNCTIONAL: [
        DataType.SESSION,
    ],
    CookieCategory.UNKNOWN: [
        DataType.ID,
    ],
}

VENDOR_EXTRA_EXPOSURE: dict[str, list[DataType]] = {
    "Google": [DataType.INTERESTS, DataType.COUNTRY, DataType.CITY],
    "Meta": [DataType.SOCIAL, DataType.INTERESTS, DataType.NAME],
    "LinkedIn": [DataType.SOCIAL, DataType.NAME, DataType.EMAIL],
    "TikTok": [DataType.INTERESTS, DataType.DEVICE],
    "Amazon": [DataType.INTERESTS, DataType.CARD],
    "HubSpot": [DataType.EMAIL, DataType.NAME],
}


def _data_exposure(cookie: CategorizedCookie) -> list[DataType]:
    types = list(CATEGORY_DATA_EXPOSURE.get(cookie.category, [DataType.ID]))
    if cookie.vendor and cookie.vendor in VENDOR_EXTRA_EXPOSURE:
        for dt in VENDOR_EXTRA_EXPOSURE[cookie.vendor]:
            if dt not in types:
                types.append(dt)
    return types


def score_cookie(cookie: CategorizedCookie) -> CookieRisk:
    exposed = _data_exposure(cookie)
    factors: list[str] = []

    if exposed:
        sensitivities = [DATA_SENSITIVITY[dt] for dt in exposed]
        base = max(sensitivities)
        exposed_labels = [dt.value for dt in exposed]
        factors.append(f"Exposes data types: {', '.join(exposed_labels)}")
    else:
        base = 10

    adj = 0

    is_first_party = not cookie.raw.domain.startswith(".")
    if is_first_party:
        adj -= 15
        factors.append("First-party cookie (limited to origin site)")

    if not cookie.raw.is_persistent:
        adj -= 10
        factors.append("Session-only cookie (deleted when browser closes)")

    if cookie.category in (CookieCategory.FUNCTIONAL, CookieCategory.SESSION):
        adj -= 12
        factors.append(f"Benign category: {cookie.category.value}")
    elif cookie.category == CookieCategory.PERSONALIZATION:
        adj -= 8
        factors.append("Preference cookie (stores user settings)")
    elif cookie.category == CookieCategory.AUTHENTICATION:
        adj -= 5
        factors.append("Authentication cookie (user-initiated)")

    if not is_first_party:
        adj += 8
        factors.append("Third-party cookie (cross-site tracking potential)")

    if cookie.raw.expires and cookie.raw.expires not in ("", "None"):
        try:
            remaining = float(cookie.raw.expires) - time.time()
            if remaining > 365 * 86400:
                adj += 8
                factors.append("Long-lived (expires > 1 year)")
            elif remaining > 90 * 86400:
                adj += 4
                factors.append("Moderately long-lived (expires > 90 days)")
        except (ValueError, TypeError):
            pass

    if not cookie.raw.secure and not is_first_party:
        adj += 4
        factors.append("Not marked Secure (transmittable over HTTP)")

    if not cookie.raw.same_site or cookie.raw.same_site.lower() == "none":
        if not is_first_party:
            adj += 4
            factors.append("SameSite=None or missing (cross-site requests allowed)")

    if not factors:
        factors.append(f"Baseline risk from category: {cookie.category.value}")

    return CookieRisk(
        cookie_name=cookie.raw.name,
        cookie_domain=cookie.raw.domain,
        score=min(100, max(0, base + adj)),
        factors=factors,
    )


def aggregate_risk(
    risks: list[CookieRisk], cookies: list[CategorizedCookie]
) -> AggregateRisk:
    if not risks:
        return AggregateRisk(
            score=0, label="None", summary="No cookies to analyze.",
            category_breakdown={}, top_factors=[],
        )

    avg = sum(r.score for r in risks) / len(risks)
    top5 = sorted((r.score for r in risks), reverse=True)[:5]
    weighted = avg * 0.4 + (sum(top5) / len(top5)) * 0.6

    buckets: dict[str, list[float]] = {}
    for cookie, risk in zip(cookies, risks):
        buckets.setdefault(cookie.category.value, []).append(risk.score)
    category_breakdown = {k: round(sum(v) / len(v), 1) for k, v in buckets.items()}

    seen: set[str] = set()
    top_factors: list[str] = []
    for r in sorted(risks, key=lambda x: x.score, reverse=True):
        for f in r.factors:
            if f not in seen:
                seen.add(f)
                top_factors.append(f)
            if len(top_factors) >= 5:
                break
        if len(top_factors) >= 5:
            break

    label = (
        "Low" if weighted < 25 else
        "Medium" if weighted < 50 else
        "High" if weighted < 75 else
        "Critical"
    )

    domains = set(r.cookie_domain for r in risks)
    high_count = sum(1 for r in risks if r.score >= 70)
    summary = (
        f"Aggregate risk {weighted:.0f}/100. "
        f"{high_count} high-risk cookie{'s' if high_count != 1 else ''} "
        f"across {len(domains)} domain{'s' if len(domains) != 1 else ''}."
    )

    return AggregateRisk(
        score=round(weighted, 1),
        label=label,
        summary=summary,
        category_breakdown=category_breakdown,
        top_factors=top_factors,
    )
