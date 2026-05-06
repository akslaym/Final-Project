"""Template-based story generation from aggregated cookie data."""

from typing import Protocol

from consent.models import ConsentType, DomainConsent
from cookies.models import CategorizedCookie, CookieCategory

from .archetypes import detect_archetypes
from .models import (
    ArchetypeEntry,
    ArchetypeSignal,
    CompanyStory,
    CompositeInferenceEntry,
    InferredTrait,
    ProfileReconstructionResponse,
    Story,
)


class StoryEngine(Protocol):
    def build(
        self,
        cookies: list[CategorizedCookie],
        consent: list[DomainConsent],
    ) -> Story: ...


CATEGORY_INFERENCES: dict[CookieCategory, list[str]] = {
    CookieCategory.ADVERTISING: [
        "Shopping interests and purchase intent",
        "Browsing habits across the web",
        "Ad interaction history",
    ],
    CookieCategory.ANALYTICS: [
        "Pages visited and time spent on each",
        "Device type and browser fingerprint",
        "Geographic region (via IP geolocation)",
    ],
    CookieCategory.SOCIAL_MEDIA: [
        "Social media profile linkage",
        "Content sharing behavior",
        "Social graph connections",
    ],
    CookieCategory.PERSONALIZATION: [
        "Language and locale preferences",
        "UI customization choices",
    ],
    CookieCategory.AUTHENTICATION: [
        "Account existence on specific platforms",
    ],
    CookieCategory.SESSION: [],
    CookieCategory.FUNCTIONAL: [],
    CookieCategory.UNKNOWN: [],
}

VENDOR_INFERENCES: dict[str, list[str]] = {
    "Google": ["Search interest profile", "Location history patterns", "YouTube watch history"],
    "Meta": ["Social connections graph", "Political interest signals", "Cross-app activity"],
    "Amazon": ["Purchase history patterns", "Product interest categories"],
    "TikTok": ["Content preference profile", "Engagement behavior patterns"],
    "LinkedIn": ["Professional profile data", "Career interest signals"],
}

COOKIE_DECODINGS: dict[str, str] = {
    "_ga": "Google Analytics client ID -- unique visitor identifier",
    "_gid": "Google Analytics session ID -- tracks your current browsing session",
    "_gat": "Google Analytics throttle -- rate-limits data collection",
    "_gcl_au": "Google Conversion Linker -- ties ad clicks to site actions",
    "_fbp": "Meta Pixel browser ID -- tracks you across Meta's ad network",
    "_fbc": "Meta click ID -- records which Facebook ad brought you here",
    "fr": "Meta ad tracking -- builds an interest profile from your browsing",
    "NID": "Google preferences -- stores search settings and ad personalization",
    "SID": "Google session -- keeps you signed in to Google services",
    "APISID": "Google API authentication -- links browsing to your Google account",
    "SAPISID": "Google secure API -- used for YouTube and Google+ integration",
    "IDE": "DoubleClick ad serving -- tracks ad impressions across sites",
    "_uetsid": "Microsoft Bing Ads session -- tracks conversions from Bing ads",
    "_uetvid": "Microsoft Bing Ads visitor -- persistent cross-session ad tracking",
    "li_sugr": "LinkedIn ad tracking -- matches you to your LinkedIn profile",
    "_li_ss": "LinkedIn session -- tracks LinkedIn share button interactions",
    "lidc": "LinkedIn data center routing -- also used for analytics",
    "tt_webid": "TikTok visitor ID -- identifies you in TikTok's pixel network",
    "_ttp": "TikTok tracking pixel -- measures ad performance across sites",
    "hubspotutk": "HubSpot visitor tracking -- builds a browsing profile for sales",
    "_hjid": "Hotjar visitor ID -- records mouse movements and page interactions",
    "_hjSession": "Hotjar session -- groups your page visits for replay analysis",
    "mp_": "Mixpanel analytics -- tracks custom events and user flows",
    "ajs_anonymous_id": "Segment anonymous ID -- unified tracking across analytics tools",
    "__cf_bm": "Cloudflare bot detection -- distinguishes humans from bots",
    "cf_clearance": "Cloudflare challenge passed -- proves you solved a CAPTCHA",
    "__stripe_mid": "Stripe merchant ID -- fraud detection for payments",
    "_pin_unauth": "Pinterest unauthenticated tracking -- tracks you before login",
    "csrf_token": "CSRF protection -- security token, prevents cross-site attacks",
    "receive-cookie-deprecation": "Chrome Privacy Sandbox -- origin trial marker",
}

COMPANY_INSIGHTS: dict[str, dict] = {
    "Google": {
        "insight": "Google's cookies create a comprehensive profile of your search behavior, "
                   "browsing patterns, and ad interactions across millions of sites.",
        "data_points": [
            "Search queries and click patterns",
            "Sites visited via Google Ads network",
            "YouTube viewing history and preferences",
            "Location via IP geolocation",
            "Device and browser fingerprint",
        ],
    },
    "Meta": {
        "insight": "Meta's tracking pixels follow you across the web, linking your browsing "
                   "to your Facebook/Instagram identity to serve targeted ads.",
        "data_points": [
            "Sites visited with Meta Pixel installed",
            "Products viewed and purchase behavior",
            "Social connections and interests",
            "Ad interactions and conversions",
        ],
    },
    "Amazon": {
        "insight": "Amazon cookies track your product interests and shopping behavior, "
                   "building a detailed consumer profile.",
        "data_points": [
            "Product categories browsed",
            "Purchase intent signals",
            "Price sensitivity patterns",
        ],
    },
    "LinkedIn": {
        "insight": "LinkedIn cookies can link your browsing to your professional identity, "
                   "revealing career interests and professional network.",
        "data_points": [
            "Professional profile linkage",
            "Job search and career interest signals",
            "Industry and company interests",
        ],
    },
    "TikTok": {
        "insight": "TikTok's tracking follows you across the web, building a content preference "
                   "profile that extends beyond the app.",
        "data_points": [
            "Content preference profile",
            "Browsing behavior on sites with TikTok pixel",
            "Ad engagement patterns",
        ],
    },
    "Microsoft": {
        "insight": "Microsoft cookies track your activity across Bing, Outlook, and partner sites "
                   "to personalize ads and services.",
        "data_points": [
            "Bing search and ad interactions",
            "Cross-site browsing via ad network",
            "Outlook and productivity tool usage",
        ],
    },
    "Adobe": {
        "insight": "Adobe Experience Cloud cookies power enterprise-grade analytics and "
                   "personalization across major brand websites.",
        "data_points": [
            "Cross-site visitor identification",
            "Content engagement patterns",
            "A/B test variant assignments",
        ],
    },
    "HubSpot": {
        "insight": "HubSpot cookies track your engagement with business websites, building "
                   "a lead profile for sales teams.",
        "data_points": [
            "Pages visited and content consumed",
            "Form submissions and email opens",
            "Return visit frequency and engagement depth",
        ],
    },
}

DOMAIN_INTENT_SIGNALS: dict[str, str] = {
    "zillow": "You may be researching real estate -- possibly looking to move or invest",
    "realtor": "Real estate browsing suggests you're exploring housing options",
    "trulia": "Property search behavior indicates housing market interest",
    "apartments": "Apartment hunting activity detected",
    "indeed": "Job search activity -- you may be considering a career change",
    "glassdoor": "Researching companies and salaries -- possibly job hunting",
    "linkedin": "Professional networking -- career development or job search",
    "webmd": "Health information research detected",
    "healthline": "Health and wellness content consumption",
    "mayoclinic": "Medical information research",
    "bankrate": "Financial product research -- comparing rates and options",
    "creditkarma": "Credit monitoring -- financial health awareness",
    "nerdwallet": "Financial product comparison -- researching money decisions",
    "expedia": "Travel planning activity detected",
    "booking": "Hotel and accommodation research",
    "kayak": "Travel search behavior -- comparing flights and hotels",
    "airbnb": "Accommodation browsing -- possible travel plans",
    "coursera": "Online learning -- skill development in progress",
    "udemy": "Course browsing -- self-improvement or career skills",
    "edx": "Educational content -- academic or professional development",
    "amazon": "Shopping patterns reveal product interests and purchase intent",
    "ebay": "Marketplace browsing reveals product interests",
    "etsy": "Artisan/craft shopping suggests personal style preferences",
    "wayfair": "Home furnishing interest -- possibly decorating or moving",
    "homedepot": "Home improvement research",
    "lowes": "Home improvement activity suggests homeowner or renovation plans",
    "netflix": "Entertainment preferences and viewing habits",
    "spotify": "Music taste and listening patterns",
    "youtube": "Video consumption reveals interests and information-seeking behavior",
    "tinder": "Dating app usage",
    "bumble": "Dating activity detected",
    "hinge": "Dating app presence",
    "reddit": "Community interests based on subreddit browsing",
    "twitter": "Social media engagement patterns and political interests",
    "instagram": "Visual content preferences and social connections",
    "facebook": "Social connections, interests, and demographic data",
    "pinterest": "Visual inspiration and aspiration tracking",
    "github": "Developer activity and technology interests",
    "stackoverflow": "Technical problem-solving patterns",
}


def _decode_cookie_name(name: str) -> str | None:
    if name in COOKIE_DECODINGS:
        return COOKIE_DECODINGS[name]
    for prefix, desc in COOKIE_DECODINGS.items():
        if name.startswith(prefix):
            return desc
    return None


def _group_by_company(
    cookies: list[CategorizedCookie],
) -> dict[str, list[CategorizedCookie]]:
    groups: dict[str, list[CategorizedCookie]] = {}
    for c in cookies:
        key = c.vendor or c.raw.domain.lstrip(".")
        groups.setdefault(key, []).append(c)
    return groups


def _infer_domain_intent(domains: set[str]) -> list[str]:
    intents: list[str] = []
    for domain in domains:
        domain_lower = domain.lower()
        for signal_key, signal_desc in DOMAIN_INTENT_SIGNALS.items():
            if signal_key in domain_lower:
                intents.append(signal_desc)
                break
    return intents


def _build_company_story(
    company: str,
    cookies: list[CategorizedCookie],
) -> CompanyStory:
    domains = list(set(c.raw.domain.lstrip(".") for c in cookies))
    categories = set(c.category for c in cookies)

    known = COMPANY_INSIGHTS.get(company)
    if known:
        insight = known["insight"]
        data_points = list(known["data_points"])
    else:
        decoded = []
        for c in cookies:
            d = _decode_cookie_name(c.raw.name)
            if d:
                decoded.append(d.split(" -- ")[0] if " -- " in d else d)

        if decoded:
            unique_decoded = list(dict.fromkeys(decoded))[:3]
            insight = f"{company} uses cookies for: {'; '.join(unique_decoded)}."
        elif CookieCategory.ADVERTISING in categories:
            insight = f"{company} places advertising cookies that track your browsing across sites."
        elif CookieCategory.ANALYTICS in categories:
            insight = f"{company} uses analytics cookies to monitor your site interactions."
        elif CookieCategory.AUTHENTICATION in categories:
            insight = f"{company} stores authentication state -- you have an account here."
        else:
            insight = f"{company} sets {len(cookies)} cookie{'s' if len(cookies) != 1 else ''} on your browser."

        data_points = []
        for c in cookies:
            d = _decode_cookie_name(c.raw.name)
            if d:
                data_points.append(d)
            elif c.purpose and c.purpose != "Purpose could not be determined automatically":
                data_points.append(f"{c.raw.name}: {c.purpose}")

        data_points = list(dict.fromkeys(data_points))[:5]

    domain_set = set(domains)
    intents = _infer_domain_intent(domain_set)
    if intents:
        data_points = intents[:2] + data_points

    has_tracking = CookieCategory.ADVERTISING in categories or CookieCategory.SOCIAL_MEDIA in categories
    has_many = len(cookies) > 5
    if has_tracking and has_many:
        risk_level = "high"
    elif has_tracking or has_many:
        risk_level = "medium"
    else:
        risk_level = "low"

    return CompanyStory(
        company=company,
        domains=domains,
        cookie_count=len(cookies),
        insight=insight,
        data_points=data_points[:6],
        risk_level=risk_level,
    )


class TemplateStoryBuilder:
    def build(
        self,
        cookies: list[CategorizedCookie],
        consent: list[DomainConsent],
    ) -> Story:
        if not cookies:
            return Story(
                narrative="No cookies were provided for analysis.",
                traits=[], company_stories=[],
                cookie_count=0, domain_count=0,
            )

        domains = set(c.raw.domain.lstrip(".") for c in cookies)
        categories = set(c.category for c in cookies)
        vendors = set(c.vendor for c in cookies if c.vendor)
        tacit_count = sum(1 for d in consent if d.consent_type == ConsentType.TACIT)

        traits: list[InferredTrait] = []
        for category in categories:
            for inference in CATEGORY_INFERENCES.get(category, []):
                sources = [
                    f"{c.raw.name} ({c.raw.domain})"
                    for c in cookies if c.category == category
                ]
                traits.append(InferredTrait(
                    trait=inference, confidence="medium",
                    sources=sources[:3],
                ))

        for vendor in vendors:
            for inference in VENDOR_INFERENCES.get(vendor, []):
                sources = [
                    f"{c.raw.name} ({c.raw.domain})"
                    for c in cookies if c.vendor == vendor
                ]
                traits.append(InferredTrait(
                    trait=inference, confidence="low",
                    sources=sources[:3],
                ))

        intents = _infer_domain_intent(domains)
        for intent in intents[:5]:
            traits.append(InferredTrait(
                trait=intent, confidence="medium", sources=[],
            ))

        company_groups = _group_by_company(cookies)
        company_stories: list[CompanyStory] = []
        for company, company_cookies in company_groups.items():
            story = _build_company_story(company, company_cookies)
            company_stories.append(story)

        risk_order = {"high": 0, "medium": 1, "low": 2}
        company_stories.sort(
            key=lambda s: (risk_order.get(s.risk_level, 3), -s.cookie_count)
        )

        parts: list[str] = []
        parts.append(
            f"From {len(cookies)} cookies across {len(domains)} "
            f"domain{'s' if len(domains) != 1 else ''}, "
            f"a third party could piece together the following profile:"
        )

        if CookieCategory.ANALYTICS in categories:
            parts.append(
                "Analytics trackers reveal which pages you visit, "
                "how long you stay, and what device you're using."
            )

        if CookieCategory.ADVERTISING in categories:
            ad_domains = set(
                c.raw.domain for c in cookies
                if c.category == CookieCategory.ADVERTISING
            )
            parts.append(
                f"Advertising cookies from {len(ad_domains)} "
                f"domain{'s' if len(ad_domains) != 1 else ''} "
                f"track your browsing to build a profile of your "
                f"interests and purchase intent."
            )

        if CookieCategory.SOCIAL_MEDIA in categories:
            parts.append(
                "Social media trackers can link your browsing "
                "activity to your social identity."
            )

        if tacit_count > 0:
            parts.append(
                f"{tacit_count} domain{'s' if tacit_count != 1 else ''} "
                f"collected data under tacit consent — you were never asked."
            )

        if vendors:
            parts.append(f"Data flows to: {', '.join(sorted(vendors))}.")

        profile_data = detect_archetypes(cookies)
        profile = ProfileReconstructionResponse(
            archetypes=[
                ArchetypeEntry(
                    id=a.id,
                    label=a.label,
                    description=a.description,
                    confidence=a.confidence,
                    confidence_score=a.confidence_score,
                    signals=[
                        ArchetypeSignal(
                            cookie_name=s.cookie_name,
                            cookie_domain=s.cookie_domain,
                            reason=s.reason,
                        )
                        for s in a.signals
                    ],
                    threshold=a.threshold,
                    activated=a.activated,
                )
                for a in profile_data.archetypes
            ],
            composites=[
                CompositeInferenceEntry(
                    inference=c.inference,
                    archetype_ids=c.archetype_ids,
                    explanation=c.explanation,
                )
                for c in profile_data.composites
            ],
            summary=profile_data.summary,
            disclaimer=profile_data.disclaimer,
        )

        return Story(
            narrative=" ".join(parts),
            traits=traits,
            company_stories=company_stories,
            profile=profile,
            cookie_count=len(cookies),
            domain_count=len(domains),
        )


default_engine: StoryEngine = TemplateStoryBuilder()
