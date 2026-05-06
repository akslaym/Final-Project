"""Archetype detection: accumulate domain signals, activate at 3+, stack into composites."""

from __future__ import annotations

from dataclasses import dataclass, field

from cookies.models import CategorizedCookie, CookieCategory


@dataclass
class Signal:
    """A single piece of evidence toward an archetype."""
    cookie_name: str
    cookie_domain: str
    reason: str  # human-readable why this cookie counts


@dataclass
class ArchetypeResult:
    """An archetype that has been evaluated (may or may not be activated)."""
    id: str
    label: str
    description: str
    confidence: str  # "possible", "likely", "very_likely"
    confidence_score: float  # 0.0-1.0 for sorting
    signals: list[Signal]
    threshold: int  # how many signals needed to activate
    activated: bool


@dataclass
class CompositeInference:
    """Emerges when two or more archetypes are both activated."""
    inference: str
    archetype_ids: list[str]
    explanation: str  # why this combination is meaningful


@dataclass
class ProfileReconstruction:
    """Top-level output: all archetypes + composites + the summary."""
    archetypes: list[ArchetypeResult]
    composites: list[CompositeInference]
    summary: str
    disclaimer: str


@dataclass
class ArchetypeDefinition:
    id: str
    label: str
    description: str
    domain_patterns: list[str] = field(default_factory=list)
    cookie_patterns: list[str] = field(default_factory=list)
    category_signals: list[CookieCategory] = field(default_factory=list)
    vendor_signals: list[str] = field(default_factory=list)
    threshold: int = 3


ARCHETYPES: list[ArchetypeDefinition] = [
    ArchetypeDefinition(
        id="job_seeker",
        label="Job Seeker",
        description="Actively searching for employment or exploring career moves",
        domain_patterns=[
            "indeed", "glassdoor", "linkedin", "monster", "ziprecruiter",
            "careerbuilder", "hired", "angel.co", "wellfound", "lever.co",
            "greenhouse", "workday", "dice.com", "simplyhired",
        ],
        cookie_patterns=["li_sugr", "_li_ss", "lidc"],
        threshold=3,
    ),
    ArchetypeDefinition(
        id="student",
        label="Student",
        description="Enrolled in education or actively pursuing coursework",
        domain_patterns=[
            ".edu", "canvas", "blackboard", "coursera", "edx", "chegg",
            "quizlet", "khanacademy", "udemy", "studocu", "grammarly",
            "turnitin", "piazza", "gradescope",
        ],
        cookie_patterns=[],
        threshold=3,
    ),
    ArchetypeDefinition(
        id="home_hunter",
        label="Home Hunter",
        description="Researching real estate — buying, renting, or relocating",
        domain_patterns=[
            "zillow", "realtor", "redfin", "trulia", "apartments.com",
            "hotpads", "rent.com", "streeteasy", "compass.com",
            "bankrate.com/mortgages", "rocket", "loandepot",
        ],
        cookie_patterns=[],
        threshold=3,
    ),
    ArchetypeDefinition(
        id="traveler",
        label="Traveler",
        description="Planning travel — flights, hotels, or experiences",
        domain_patterns=[
            "expedia", "booking.com", "kayak", "airbnb", "tripadvisor",
            "skyscanner", "hopper", "google.com/travel", "southwest",
            "united.com", "delta.com", "aa.com", "marriott", "hilton",
            "hostelworld", "vrbo",
        ],
        cookie_patterns=[],
        threshold=3,
    ),
    ArchetypeDefinition(
        id="health_researcher",
        label="Health Researcher",
        description="Actively looking up medical or wellness information",
        domain_patterns=[
            "webmd", "healthline", "mayoclinic", "nih.gov", "medlineplus",
            "clevelandclinic", "drugs.com", "goodrx", "zocdoc",
            "myfitnesspal", "calorieking",
        ],
        cookie_patterns=[],
        threshold=3,
    ),
    ArchetypeDefinition(
        id="finance_focused",
        label="Finance Focused",
        description="Actively managing money, credit, or investments",
        domain_patterns=[
            "bankrate", "creditkarma", "nerdwallet", "mint.com",
            "robinhood", "fidelity", "vanguard", "schwab", "etrade",
            "coinbase", "turbotax", "irs.gov", "personalcapital",
        ],
        cookie_patterns=[],
        threshold=3,
    ),
    ArchetypeDefinition(
        id="online_shopper",
        label="Active Online Shopper",
        description="Frequent e-commerce activity across multiple platforms",
        domain_patterns=[
            "amazon", "ebay", "etsy", "wayfair", "target.com",
            "walmart.com", "bestbuy", "shopify", "aliexpress",
            "shein", "nordstrom", "macys",
        ],
        cookie_patterns=["_shopify", "cart_", "checkout_"],
        category_signals=[CookieCategory.ADVERTISING],
        threshold=4,  # higher threshold — shopping cookies are very common
    ),
    ArchetypeDefinition(
        id="tech_professional",
        label="Tech Professional",
        description="Software development or IT-related activity",
        domain_patterns=[
            "github", "stackoverflow", "gitlab", "npm", "pypi",
            "docker", "aws.amazon", "cloud.google", "azure",
            "vercel", "netlify", "digitalocean", "heroku",
        ],
        cookie_patterns=[],
        threshold=3,
    ),
    ArchetypeDefinition(
        id="social_media_active",
        label="Social Media Active",
        description="Heavy presence across multiple social platforms",
        domain_patterns=[
            "facebook", "instagram", "tiktok", "twitter", "x.com",
            "snapchat", "reddit", "tumblr", "threads.net",
        ],
        cookie_patterns=["_fbp", "_fbc", "fr", "tt_webid", "_ttp"],
        vendor_signals=["Meta", "TikTok"],
        threshold=4,  # higher — social trackers are everywhere even if you don't use them
    ),
    ArchetypeDefinition(
        id="gamer",
        label="Gamer",
        description="Active gaming across platforms",
        domain_patterns=[
            "steam", "twitch", "epicgames", "discord", "xbox",
            "playstation", "ign.com", "kotaku", "polygon",
            "riotgames", "blizzard", "ea.com",
        ],
        cookie_patterns=[],
        threshold=3,
    ),
    ArchetypeDefinition(
        id="fitness_enthusiast",
        label="Fitness Enthusiast",
        description="Regular engagement with fitness and wellness platforms",
        domain_patterns=[
            "strava", "peloton", "myfitnesspal", "fitbit", "garmin",
            "nike.com/run", "underarmour", "bodybuilding.com",
            "lululemon", "gymshark",
        ],
        cookie_patterns=[],
        threshold=3,
    ),
    ArchetypeDefinition(
        id="parent",
        label="Parent",
        description="Browsing patterns suggest parenting responsibilities",
        domain_patterns=[
            "babycenter", "whattoexpect", "pampers", "huggies",
            "target.com/baby", "amazon.com/baby", "parenthood",
            "commonsensemedia", "pbskids", "nickjr", "disney",
        ],
        cookie_patterns=[],
        threshold=3,
    ),
    ArchetypeDefinition(
        id="dating",
        label="Dating",
        description="Active on dating or relationship platforms",
        domain_patterns=[
            "tinder", "bumble", "hinge", "okcupid", "match.com",
            "eharmony", "coffee-meets-bagel", "zoosk", "plenty",
        ],
        cookie_patterns=[],
        threshold=3,
    ),
    ArchetypeDefinition(
        id="news_consumer",
        label="News Consumer",
        description="Regular engagement with news and current events",
        domain_patterns=[
            "nytimes", "washingtonpost", "cnn", "bbc", "reuters",
            "apnews", "theguardian", "wsj", "bloomberg",
            "politico", "theatlantic", "npr.org",
        ],
        cookie_patterns=[],
        threshold=3,
    ),
    ArchetypeDefinition(
        id="content_creator",
        label="Content Creator",
        description="Using creative or publishing tools",
        domain_patterns=[
            "canva", "figma", "adobe", "linktree", "substack",
            "medium.com", "wordpress", "squarespace", "wix",
            "studio.youtube", "anchor.fm", "buzzsprout",
        ],
        cookie_patterns=[],
        threshold=3,
    ),
]


COMPOSITE_RULES: list[dict] = [
    {
        "requires": ["job_seeker", "student"],
        "inference": "Likely a graduating student or career-transitioning learner",
        "explanation": "The combination of active coursework and job search activity suggests someone approaching a career transition — possibly graduating or reskilling.",
    },
    {
        "requires": ["home_hunter", "job_seeker"],
        "inference": "Possibly relocating for a new job opportunity",
        "explanation": "Simultaneous job searching and real estate browsing often indicates someone planning to move for work.",
    },
    {
        "requires": ["home_hunter", "finance_focused"],
        "inference": "Preparing financially for a property purchase",
        "explanation": "Pairing mortgage/property research with active financial management suggests preparation for a major purchase.",
    },
    {
        "requires": ["student", "finance_focused"],
        "inference": "Managing student finances or planning post-graduation money",
        "explanation": "Financial tool usage alongside educational activity suggests budgeting around tuition, loans, or early career planning.",
    },
    {
        "requires": ["traveler", "job_seeker"],
        "inference": "May be interviewing at companies in other cities",
        "explanation": "Travel research combined with job searching could indicate out-of-town interview trips or relocation scouting.",
    },
    {
        "requires": ["fitness_enthusiast", "health_researcher"],
        "inference": "Health-conscious individual actively optimizing wellness",
        "explanation": "Combining fitness tracking with medical research suggests someone taking a proactive, data-driven approach to their health.",
    },
    {
        "requires": ["tech_professional", "content_creator"],
        "inference": "Likely a developer who also creates technical content",
        "explanation": "Development tools alongside publishing platforms suggest someone who writes, records, or teaches about technology.",
    },
    {
        "requires": ["online_shopper", "parent"],
        "inference": "Purchasing products for family or children",
        "explanation": "Active shopping behavior paired with parenting sites suggests someone buying for their household and kids.",
    },
    {
        "requires": ["social_media_active", "content_creator"],
        "inference": "Building an online presence or personal brand",
        "explanation": "Heavy social media use alongside creative tools suggests someone actively cultivating an audience.",
    },
    {
        "requires": ["traveler", "dating"],
        "inference": "Planning travel possibly related to a relationship",
        "explanation": "Travel research alongside dating activity may indicate planning trips with or to see a partner.",
    },
]


def _match_domain(pattern: str, domain: str) -> bool:
    """Check if a domain matches a pattern (substring or suffix match)."""
    domain_lower = domain.lower().lstrip(".")
    pattern_lower = pattern.lower()
    if pattern_lower.startswith("."):
        return domain_lower.endswith(pattern_lower) or domain_lower.endswith(pattern_lower[1:])
    return pattern_lower in domain_lower


def _match_cookie_name(pattern: str, name: str) -> bool:
    """Check if a cookie name matches a pattern (prefix or exact)."""
    return name.lower().startswith(pattern.lower()) or name.lower() == pattern.lower()


def detect_archetypes(cookies: list[CategorizedCookie]) -> ProfileReconstruction:
    """Run all archetype detections and return the full transparent result."""

    results: list[ArchetypeResult] = []

    for archetype in ARCHETYPES:
        signals: list[Signal] = []
        seen_reasons: set[str] = set()  # deduplicate signals from same source

        for cookie in cookies:
            domain = cookie.raw.domain.lstrip(".").lower()
            top_frame = (cookie.raw.top_frame_site or "").lower()

            # Domain pattern match
            for pattern in archetype.domain_patterns:
                matched_on = None
                if _match_domain(pattern, domain):
                    matched_on = domain
                elif top_frame and _match_domain(pattern, top_frame):
                    matched_on = top_frame

                if matched_on:
                    reason = f"Domain '{matched_on}' matches pattern '{pattern}'"
                    if reason not in seen_reasons:
                        seen_reasons.add(reason)
                        signals.append(Signal(
                            cookie_name=cookie.raw.name,
                            cookie_domain=cookie.raw.domain,
                            reason=reason,
                        ))
                    break  # one match per cookie per archetype is enough

            # Cookie name pattern match
            for pattern in archetype.cookie_patterns:
                if _match_cookie_name(pattern, cookie.raw.name):
                    reason = f"Cookie '{cookie.raw.name}' matches known pattern '{pattern}'"
                    if reason not in seen_reasons:
                        seen_reasons.add(reason)
                        signals.append(Signal(
                            cookie_name=cookie.raw.name,
                            cookie_domain=cookie.raw.domain,
                            reason=reason,
                        ))
                    break

            # Vendor match
            if cookie.vendor and cookie.vendor in archetype.vendor_signals:
                reason = f"Cookie belongs to vendor '{cookie.vendor}'"
                if reason not in seen_reasons:
                    seen_reasons.add(reason)
                    signals.append(Signal(
                        cookie_name=cookie.raw.name,
                        cookie_domain=cookie.raw.domain,
                        reason=reason,
                    ))

        # Deduplicate: one signal per unique domain source
        # Multiple cookies from the same domain don't increase confidence
        unique_sources: dict[str, Signal] = {}
        for s in signals:
            source_key = s.cookie_domain.lstrip(".").lower()
            if source_key not in unique_sources:
                unique_sources[source_key] = s

        deduped_signals = list(unique_sources.values())
        signal_count = len(deduped_signals)
        activated = signal_count >= archetype.threshold

        # Confidence gradient
        if signal_count >= archetype.threshold + 4:
            confidence = "very_likely"
            confidence_score = 0.9
        elif signal_count >= archetype.threshold + 2:
            confidence = "likely"
            confidence_score = 0.7
        elif signal_count >= archetype.threshold:
            confidence = "possible"
            confidence_score = 0.5
        else:
            confidence = "insufficient"
            confidence_score = signal_count / archetype.threshold * 0.4

        results.append(ArchetypeResult(
            id=archetype.id,
            label=archetype.label,
            description=archetype.description,
            confidence=confidence,
            confidence_score=confidence_score,
            signals=deduped_signals,
            threshold=archetype.threshold,
            activated=activated,
        ))

    activated_ids = set(r.id for r in results if r.activated)
    composites: list[CompositeInference] = []

    for rule in COMPOSITE_RULES:
        required = set(rule["requires"])
        if required.issubset(activated_ids):
            composites.append(CompositeInference(
                inference=rule["inference"],
                archetype_ids=rule["requires"],
                explanation=rule["explanation"],
            ))

    activated_results = [r for r in results if r.activated]
    activated_results.sort(key=lambda r: -r.confidence_score)

    summary = _build_summary(activated_results, composites, len(cookies))

    disclaimer = (
        "This profile is reconstructed entirely from cookie metadata "
        "(names, domains, timestamps) — never from cookie values or browsing content. "
        "Archetypes activate only when 3+ independent domain signals converge. "
        "This represents what a third party could plausibly infer, not confirmed facts about you. "
        "All analysis runs locally — no data leaves your machine."
    )

    return ProfileReconstruction(
        archetypes=results,
        composites=composites,
        summary=summary,
        disclaimer=disclaimer,
    )


def _build_summary(
    activated: list[ArchetypeResult],
    composites: list[CompositeInference],
    total_cookies: int,
) -> str:
    """Build a natural-language summary paragraph from activated archetypes."""
    if not activated:
        return (
            f"From {total_cookies} cookies analyzed, there isn't enough convergent "
            f"evidence to confidently reconstruct a behavioral profile. "
            f"This could mean your browsing is diverse, or that most cookies "
            f"are functional rather than behavioral."
        )

    parts: list[str] = []

    labels = [a.label.lower() for a in activated]
    if len(labels) == 1:
        parts.append(
            f"From {total_cookies} cookies, your browsing pattern most "
            f"strongly suggests: {activated[0].label.lower()}."
        )
    elif len(labels) <= 3:
        joined = ", ".join(labels[:-1]) + f", and {labels[-1]}"
        parts.append(
            f"From {total_cookies} cookies, a third party could reconstruct "
            f"this profile: {joined}."
        )
    else:
        top_3 = ", ".join(labels[:3])
        parts.append(
            f"From {total_cookies} cookies across multiple behavioral signals, "
            f"a detailed profile emerges. Primary archetypes: {top_3} "
            f"(plus {len(labels) - 3} more)."
        )

    if composites:
        top_composite = composites[0]
        parts.append(f"Notably: {top_composite.inference.lower()}.")

    very_likely = [a for a in activated if a.confidence == "very_likely"]
    if very_likely:
        parts.append(
            f"The strongest signal is '{very_likely[0].label}' "
            f"with {len(very_likely[0].signals)} supporting cookies."
        )

    return " ".join(parts)
