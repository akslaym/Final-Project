"""Extract feature vectors from cookie sessions for archetype classification.

Produces a fixed-length numeric vector from a list of CategorizedCookies
and DomainConsent results. The vector captures category distributions,
domain keyword presence, vendor counts, consent ratios, and aggregate
statistics — everything the Random Forest needs to classify archetypes.
"""

import json
from pathlib import Path
from dataclasses import dataclass, field

from cookies.models import CategorizedCookie, CookieCategory
from consent.models import ConsentType, DomainConsent


_ARCHETYPES_PATH = Path(__file__).resolve().parent.parent / "data" / "archetypes.json"

def _load_keyword_groups() -> dict[str, list[str]]:
    with open(_ARCHETYPES_PATH) as f:
        data = json.load(f)
    return data["feature_definitions"]["domain_keyword_groups"]

KEYWORD_GROUPS: dict[str, list[str]] = _load_keyword_groups()

CATEGORY_ORDER = [
    CookieCategory.ADVERTISING,
    CookieCategory.ANALYTICS,
    CookieCategory.SOCIAL_MEDIA,
    CookieCategory.FUNCTIONAL,
    CookieCategory.SESSION,
    CookieCategory.AUTHENTICATION,
    CookieCategory.PERSONALIZATION,
    CookieCategory.UNKNOWN,
]

KEYWORD_GROUP_ORDER = sorted(KEYWORD_GROUPS.keys())

FEATURE_NAMES: list[str] = (
    [f"pct_{c.value}" for c in CATEGORY_ORDER]
    + [f"kw_{group}_count" for group in KEYWORD_GROUP_ORDER]
    + [f"kw_{group}_ratio" for group in KEYWORD_GROUP_ORDER]
    + [
        "total_cookies",
        "total_domains",
        "unique_vendors",
        "ad_cookie_count",
        "ad_vendor_count",
        "social_vendor_count",
        "third_party_count",
        "edu_domain_count",
        "gov_domain_count",
        "tacit_ratio",
        "implied_ratio",
        "explicit_ratio",
        "persistent_ratio",
        "avg_cookies_per_domain",
    ]
)


@dataclass
class FeatureVector:
    values: list[float] = field(default_factory=list)
    names: list[str] = field(default_factory=list)
    evidence: dict[str, list[str]] = field(default_factory=dict)


def _count_keyword_matches(
    domains: set[str], keywords: list[str],
) -> tuple[int, list[str]]:
    """Count how many domains match any keyword. Return count and matched domains."""
    matched = []
    for domain in domains:
        domain_lower = domain.lower()
        for kw in keywords:
            if kw in domain_lower:
                matched.append(domain)
                break
    return len(matched), matched


def extract_features(
    cookies: list[CategorizedCookie],
    consent: list[DomainConsent] | None = None,
) -> FeatureVector:
    """Extract a feature vector from a cookie session.

    Returns a FeatureVector with numeric values, feature names, and
    an evidence dict mapping keyword groups to the domains that matched.
    """
    if consent is None:
        consent = []

    total = len(cookies) or 1
    domains = set(c.raw.domain.lstrip(".") for c in cookies)
    total_domains = len(domains) or 1
    vendors = set(c.vendor for c in cookies if c.vendor)

    values: list[float] = []
    evidence: dict[str, list[str]] = {}

    # Category distribution (8 features)
    cat_counts: dict[CookieCategory, int] = {c: 0 for c in CATEGORY_ORDER}
    for cookie in cookies:
        cat_counts[cookie.category] = cat_counts.get(cookie.category, 0) + 1
    for cat in CATEGORY_ORDER:
        values.append(cat_counts[cat] / total)

    # Domain keyword group counts and ratios (2 * N features)
    for group in KEYWORD_GROUP_ORDER:
        keywords = KEYWORD_GROUPS[group]
        count, matched = _count_keyword_matches(domains, keywords)
        values.append(float(count))
        values.append(count / total_domains)
        if matched:
            evidence[group] = matched

    # Aggregate features
    ad_cookies = [c for c in cookies if c.category == CookieCategory.ADVERTISING]
    ad_vendors = set(c.vendor for c in ad_cookies if c.vendor)
    social_cookies = [c for c in cookies if c.category == CookieCategory.SOCIAL_MEDIA]
    social_vendors = set(c.vendor for c in social_cookies if c.vendor)

    functional_cats = {CookieCategory.FUNCTIONAL, CookieCategory.SESSION, CookieCategory.AUTHENTICATION}
    third_party = [c for c in cookies if c.category not in functional_cats]

    edu_domains = sum(1 for d in domains if ".edu" in d.lower() or d.lower().endswith("edu"))
    gov_domains = sum(1 for d in domains if ".gov" in d.lower())

    consent_total = len(consent) or 1
    tacit_count = sum(1 for c in consent if c.consent_type == ConsentType.TACIT)
    implied_count = sum(1 for c in consent if c.consent_type == ConsentType.IMPLIED)
    explicit_count = sum(1 for c in consent if c.consent_type == ConsentType.EXPLICIT)

    persistent_count = sum(1 for c in cookies if c.raw.is_persistent)

    values.extend([
        float(len(cookies)),
        float(len(domains)),
        float(len(vendors)),
        float(len(ad_cookies)),
        float(len(ad_vendors)),
        float(len(social_vendors)),
        float(len(third_party)),
        float(edu_domains),
        float(gov_domains),
        tacit_count / consent_total,
        implied_count / consent_total,
        explicit_count / consent_total,
        persistent_count / total,
        len(cookies) / total_domains,
    ])

    return FeatureVector(
        values=values,
        names=list(FEATURE_NAMES),
        evidence=evidence,
    )
