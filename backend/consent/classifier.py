"""Classify consent type per domain: known database then heuristic fallback."""

from cookies.models import CategorizedCookie, CookieCategory

from .models import ConsentType, DomainConsent

KNOWN_CONSENT: dict[str, tuple[ConsentType, str]] = {
    # Ad-tech: typically tacit (fires before any prompt)
    "doubleclick.net": (ConsentType.TACIT, "DoubleClick sets tracking cookies without direct user consent"),
    "googlesyndication.com": (ConsentType.TACIT, "Google ad syndication fires automatically"),
    "googleadservices.com": (ConsentType.TACIT, "Google ad cookies set without explicit action"),
    "google-analytics.com": (ConsentType.TACIT, "Google Analytics cookies set automatically by site owners"),
    "facebook.com": (ConsentType.TACIT, "Facebook tracking fires via embedded scripts"),
    "facebook.net": (ConsentType.TACIT, "Facebook SDK sets cookies automatically"),
    "tiktok.com": (ConsentType.TACIT, "TikTok pixel fires automatically on embed"),
    "pinterest.com": (ConsentType.TACIT, "Pinterest tracking cookie set on page load"),

    # Platforms: implied (consent inferred from continued usage)
    "youtube.com": (ConsentType.IMPLIED, "YouTube sets cookies via embedded content with implied consent"),
    "twitter.com": (ConsentType.IMPLIED, "Twitter widgets set cookies through embedded content"),
    "linkedin.com": (ConsentType.IMPLIED, "LinkedIn infers consent through platform usage"),
    "amazon.com": (ConsentType.IMPLIED, "Amazon infers consent through continued shopping"),
    "zillow.com": (ConsentType.IMPLIED, "Zillow infers consent through continued property browsing"),

    # GDPR-compliant sites: explicit consent banners
    "bbc.co.uk": (ConsentType.EXPLICIT, "BBC implements granular cookie consent banner"),
    "theguardian.com": (ConsentType.EXPLICIT, "The Guardian uses explicit opt-in cookie consent"),
    "lemonde.fr": (ConsentType.EXPLICIT, "Le Monde uses GDPR-compliant explicit consent"),
}


def _heuristic(
    domain: str, cookies: list[CategorizedCookie]
) -> tuple[ConsentType, float, str]:
    categories = {c.category for c in cookies}

    if categories <= {
        CookieCategory.SESSION,
        CookieCategory.AUTHENTICATION,
        CookieCategory.FUNCTIONAL,
    }:
        return (
            ConsentType.IMPLIED, 0.6,
            "Only functional/session cookies detected — consent likely implied through usage",
        )

    if categories & {CookieCategory.ADVERTISING, CookieCategory.SOCIAL_MEDIA}:
        return (
            ConsentType.TACIT, 0.5,
            "Advertising/tracking cookies present — likely set without explicit consent",
        )

    return (
        ConsentType.UNKNOWN, 0.3,
        "Consent type could not be confidently determined",
    )


def classify_consent(cookies: list[CategorizedCookie]) -> list[DomainConsent]:
    by_domain: dict[str, list[CategorizedCookie]] = {}
    for cookie in cookies:
        domain = cookie.raw.domain.lstrip(".")
        by_domain.setdefault(domain, []).append(cookie)

    results: list[DomainConsent] = []
    for domain, domain_cookies in by_domain.items():
        # Check known database
        known = None
        for known_domain, info in KNOWN_CONSENT.items():
            if domain.endswith(known_domain):
                known = info
                break

        if known:
            consent_type, evidence = known
            results.append(DomainConsent(
                domain=domain, consent_type=consent_type,
                confidence=0.8, evidence=evidence,
            ))
        else:
            consent_type, confidence, evidence = _heuristic(domain, domain_cookies)
            results.append(DomainConsent(
                domain=domain, consent_type=consent_type,
                confidence=confidence, evidence=evidence,
            ))

    return results
