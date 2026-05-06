"""Comprehensive domain-to-category database."""

from .models import CookieCategory


class DomainInfo:
    __slots__ = ("category", "vendor", "description")

    def __init__(self, category: CookieCategory, vendor: str, description: str):
        self.category = category
        self.vendor = vendor
        self.description = description


# Keys are domain suffixes — matched via str.endswith()
DOMAIN_DB: dict[str, DomainInfo] = {

    # ── Google Advertising ──────────────────────────────────────
    "doubleclick.net": DomainInfo(
        CookieCategory.ADVERTISING, "Google",
        "Google's ad-serving and tracking infrastructure"),
    "googlesyndication.com": DomainInfo(
        CookieCategory.ADVERTISING, "Google",
        "Google AdSense ad syndication network"),
    "googleadservices.com": DomainInfo(
        CookieCategory.ADVERTISING, "Google",
        "Google Ads conversion tracking and remarketing"),
    "googleads.g.doubleclick.net": DomainInfo(
        CookieCategory.ADVERTISING, "Google",
        "Google Ads campaign measurement"),
    "adservice.google.com": DomainInfo(
        CookieCategory.ADVERTISING, "Google",
        "Google ad delivery service"),
    "pagead2.googlesyndication.com": DomainInfo(
        CookieCategory.ADVERTISING, "Google",
        "Google AdSense page-level ad serving"),

    # ── Google Analytics ────────────────────────────────────────
    "google-analytics.com": DomainInfo(
        CookieCategory.ANALYTICS, "Google",
        "Google Analytics web traffic measurement"),
    "googletagmanager.com": DomainInfo(
        CookieCategory.ANALYTICS, "Google",
        "Google Tag Manager — deploys analytics and marketing tags"),
    "googleoptimize.com": DomainInfo(
        CookieCategory.ANALYTICS, "Google",
        "Google Optimize A/B testing platform"),

    # ── Google Functional ───────────────────────────────────────
    "gstatic.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "Google",
        "Google static content delivery (fonts, images)"),
    "googleapis.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "Google",
        "Google API services (Maps, Fonts, etc.)"),
    "accounts.google.com": DomainInfo(
        CookieCategory.AUTHENTICATION, "Google",
        "Google account authentication"),

    # ── Meta / Facebook ─────────────────────────────────────────
    "facebook.com": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "Meta",
        "Facebook social platform — tracks activity across the web via embedded widgets"),
    "facebook.net": DomainInfo(
        CookieCategory.ADVERTISING, "Meta",
        "Facebook SDK and pixel tracking infrastructure"),
    "fbcdn.net": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "Meta",
        "Facebook content delivery network"),
    "instagram.com": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "Meta",
        "Instagram social platform"),
    "fb.com": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "Meta",
        "Facebook short domain"),

    # ── Microsoft / LinkedIn ────────────────────────────────────
    "linkedin.com": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "LinkedIn",
        "LinkedIn professional network — tracks browsing for ad targeting"),
    "ads.linkedin.com": DomainInfo(
        CookieCategory.ADVERTISING, "LinkedIn",
        "LinkedIn advertising platform"),
    "bing.com": DomainInfo(
        CookieCategory.ADVERTISING, "Microsoft",
        "Microsoft Bing search and advertising"),
    "bat.bing.com": DomainInfo(
        CookieCategory.ADVERTISING, "Microsoft",
        "Microsoft Bing Ads universal event tracking"),
    "clarity.ms": DomainInfo(
        CookieCategory.ANALYTICS, "Microsoft",
        "Microsoft Clarity session recording and heatmaps"),

    # ── Twitter / X ─────────────────────────────────────────────
    "twitter.com": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "X (Twitter)",
        "Twitter/X social platform"),
    "t.co": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "X (Twitter)",
        "Twitter/X link shortener and click tracking"),
    "ads-twitter.com": DomainInfo(
        CookieCategory.ADVERTISING, "X (Twitter)",
        "Twitter/X advertising platform"),

    # ── TikTok / ByteDance ──────────────────────────────────────
    "tiktok.com": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "TikTok",
        "TikTok social video platform"),
    "byteoversea.com": DomainInfo(
        CookieCategory.ADVERTISING, "TikTok",
        "TikTok/ByteDance overseas advertising infrastructure"),
    "tiktokcdn.com": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "TikTok",
        "TikTok content delivery"),

    # ── Snap ────────────────────────────────────────────────────
    "snapchat.com": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "Snap",
        "Snapchat social platform"),
    "sc-static.net": DomainInfo(
        CookieCategory.ADVERTISING, "Snap",
        "Snapchat pixel and ad tracking"),

    # ── Pinterest ───────────────────────────────────────────────
    "pinterest.com": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "Pinterest",
        "Pinterest visual discovery platform"),
    "pinimg.com": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "Pinterest",
        "Pinterest image CDN"),

    # ── Reddit ──────────────────────────────────────────────────
    "reddit.com": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "Reddit",
        "Reddit discussion platform"),
    "redditmedia.com": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "Reddit",
        "Reddit media and embed delivery"),
    "redditstatic.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "Reddit",
        "Reddit static assets"),

    # ── Ad-tech (programmatic) ──────────────────────────────────
    "criteo.com": DomainInfo(
        CookieCategory.ADVERTISING, "Criteo",
        "Criteo retargeting — tracks browsing to serve personalized ads across sites"),
    "adroll.com": DomainInfo(
        CookieCategory.ADVERTISING, "AdRoll",
        "AdRoll retargeting and prospecting ad platform"),
    "d.adroll.com": DomainInfo(
        CookieCategory.ADVERTISING, "AdRoll",
        "AdRoll data collection endpoint"),
    "adsrvr.org": DomainInfo(
        CookieCategory.ADVERTISING, "The Trade Desk",
        "The Trade Desk demand-side ad platform"),
    "adnxs.com": DomainInfo(
        CookieCategory.ADVERTISING, "Xandr (Microsoft)",
        "Xandr/AppNexus programmatic ad exchange"),
    "rubiconproject.com": DomainInfo(
        CookieCategory.ADVERTISING, "Magnite (Rubicon)",
        "Magnite (formerly Rubicon Project) programmatic ad exchange"),
    "pubmatic.com": DomainInfo(
        CookieCategory.ADVERTISING, "PubMatic",
        "PubMatic programmatic advertising supply-side platform"),
    "openx.net": DomainInfo(
        CookieCategory.ADVERTISING, "OpenX",
        "OpenX programmatic ad exchange"),
    "indexexchange.com": DomainInfo(
        CookieCategory.ADVERTISING, "Index Exchange",
        "Index Exchange programmatic ad marketplace"),
    "casalemedia.com": DomainInfo(
        CookieCategory.ADVERTISING, "Index Exchange",
        "Index Exchange (formerly Casale Media) ad exchange"),
    "bidswitch.net": DomainInfo(
        CookieCategory.ADVERTISING, "IPONWEB",
        "BidSwitch cross-platform ad exchange bridge"),
    "smartadserver.com": DomainInfo(
        CookieCategory.ADVERTISING, "Equativ (Smart)",
        "Equativ (formerly Smart AdServer) ad serving platform"),
    "media.net": DomainInfo(
        CookieCategory.ADVERTISING, "Media.net",
        "Media.net contextual advertising (Yahoo/Bing network)"),
    "serving-sys.com": DomainInfo(
        CookieCategory.ADVERTISING, "Sizmek",
        "Sizmek ad serving and rich media delivery"),
    "taboola.com": DomainInfo(
        CookieCategory.ADVERTISING, "Taboola",
        "Taboola content recommendation and native advertising"),
    "outbrain.com": DomainInfo(
        CookieCategory.ADVERTISING, "Outbrain",
        "Outbrain content discovery and native advertising"),
    "amazon-adsystem.com": DomainInfo(
        CookieCategory.ADVERTISING, "Amazon",
        "Amazon advertising platform"),
    "sharethrough.com": DomainInfo(
        CookieCategory.ADVERTISING, "Sharethrough",
        "Sharethrough native ad exchange"),
    "simpli.fi": DomainInfo(
        CookieCategory.ADVERTISING, "Simpli.fi",
        "Simpli.fi programmatic ad platform"),
    "demdex.net": DomainInfo(
        CookieCategory.ADVERTISING, "Adobe",
        "Adobe Audience Manager data management platform"),
    "everesttech.net": DomainInfo(
        CookieCategory.ADVERTISING, "Adobe",
        "Adobe Advertising Cloud tracking"),
    "rfihub.com": DomainInfo(
        CookieCategory.ADVERTISING, "Rocket Fuel (Zeta)",
        "Rocket Fuel/Zeta programmatic advertising"),
    "mathtag.com": DomainInfo(
        CookieCategory.ADVERTISING, "MediaMath",
        "MediaMath programmatic ad platform"),
    "mookie1.com": DomainInfo(
        CookieCategory.ADVERTISING, "MediaMath",
        "MediaMath cookie syncing and ad delivery"),
    "rlcdn.com": DomainInfo(
        CookieCategory.ADVERTISING, "LiveRamp",
        "LiveRamp identity resolution for ad targeting"),
    "liadm.com": DomainInfo(
        CookieCategory.ADVERTISING, "LiveIntent",
        "LiveIntent identity-based ad targeting"),
    "eyeota.net": DomainInfo(
        CookieCategory.ADVERTISING, "Eyeota",
        "Eyeota audience data marketplace"),
    "exelator.com": DomainInfo(
        CookieCategory.ADVERTISING, "Nielsen",
        "Nielsen eXelate data management platform"),
    "bluekai.com": DomainInfo(
        CookieCategory.ADVERTISING, "Oracle",
        "Oracle BlueKai data management platform"),
    "addthis.com": DomainInfo(
        CookieCategory.ADVERTISING, "Oracle",
        "AddThis social sharing with cross-site tracking"),
    "3lift.com": DomainInfo(
        CookieCategory.ADVERTISING, "TripleLift",
        "TripleLift native programmatic ad exchange"),
    "id5-sync.com": DomainInfo(
        CookieCategory.ADVERTISING, "ID5",
        "ID5 universal identifier for ad targeting"),
    "liveramp.com": DomainInfo(
        CookieCategory.ADVERTISING, "LiveRamp",
        "LiveRamp identity infrastructure for advertising"),
    "intentiq.com": DomainInfo(
        CookieCategory.ADVERTISING, "IntentIQ",
        "IntentIQ identity resolution for advertising"),
    "yieldmo.com": DomainInfo(
        CookieCategory.ADVERTISING, "YieldMo",
        "YieldMo ad format and exchange platform"),
    "dotomi.com": DomainInfo(
        CookieCategory.ADVERTISING, "Conversant",
        "Conversant (formerly Dotomi) personalized advertising"),
    "contextweb.com": DomainInfo(
        CookieCategory.ADVERTISING, "PulsePoint",
        "PulsePoint programmatic advertising"),

    # ── Ad verification / measurement ───────────────────────────
    "moatads.com": DomainInfo(
        CookieCategory.ADVERTISING, "Oracle (Moat)",
        "Moat ad verification — measures viewability and attention"),
    "doubleverify.com": DomainInfo(
        CookieCategory.ADVERTISING, "DoubleVerify",
        "DoubleVerify ad verification and brand safety"),
    "adsafeprotected.com": DomainInfo(
        CookieCategory.ADVERTISING, "Integral Ad Science",
        "IAS ad verification and fraud prevention"),
    "imrworldwide.com": DomainInfo(
        CookieCategory.ANALYTICS, "Nielsen",
        "Nielsen Digital Ad Ratings audience measurement"),
    "scorecardresearch.com": DomainInfo(
        CookieCategory.ANALYTICS, "comScore",
        "comScore ScorecardResearch web audience measurement"),
    "quantserve.com": DomainInfo(
        CookieCategory.ANALYTICS, "Quantcast",
        "Quantcast audience measurement and targeting"),
    "quantcast.com": DomainInfo(
        CookieCategory.ANALYTICS, "Quantcast",
        "Quantcast audience insights platform"),
    "comscore.com": DomainInfo(
        CookieCategory.ANALYTICS, "comScore",
        "comScore digital analytics and audience measurement"),
    "insightexpressai.com": DomainInfo(
        CookieCategory.ANALYTICS, "Kantar",
        "Kantar (InsightExpress) digital ad effectiveness measurement"),

    # ── Analytics platforms ─────────────────────────────────────
    "hotjar.com": DomainInfo(
        CookieCategory.ANALYTICS, "Hotjar",
        "Hotjar behavior analytics — heatmaps, session recordings, surveys"),
    "mixpanel.com": DomainInfo(
        CookieCategory.ANALYTICS, "Mixpanel",
        "Mixpanel product analytics and user behavior tracking"),
    "segment.io": DomainInfo(
        CookieCategory.ANALYTICS, "Twilio Segment",
        "Segment customer data platform — routes data to analytics tools"),
    "segment.com": DomainInfo(
        CookieCategory.ANALYTICS, "Twilio Segment",
        "Segment customer data platform"),
    "amplitude.com": DomainInfo(
        CookieCategory.ANALYTICS, "Amplitude",
        "Amplitude product analytics platform"),
    "heapanalytics.com": DomainInfo(
        CookieCategory.ANALYTICS, "Heap",
        "Heap auto-capture analytics platform"),
    "heap.io": DomainInfo(
        CookieCategory.ANALYTICS, "Heap",
        "Heap analytics"),
    "fullstory.com": DomainInfo(
        CookieCategory.ANALYTICS, "FullStory",
        "FullStory digital experience analytics and session replay"),
    "pendo.io": DomainInfo(
        CookieCategory.ANALYTICS, "Pendo",
        "Pendo product analytics and in-app guidance"),
    "mouseflow.com": DomainInfo(
        CookieCategory.ANALYTICS, "Mouseflow",
        "Mouseflow session replay and behavior analytics"),
    "crazyegg.com": DomainInfo(
        CookieCategory.ANALYTICS, "Crazy Egg",
        "Crazy Egg heatmap and scroll-tracking analytics"),
    "chartbeat.com": DomainInfo(
        CookieCategory.ANALYTICS, "Chartbeat",
        "Chartbeat real-time content analytics for publishers"),
    "chartbeat.net": DomainInfo(
        CookieCategory.ANALYTICS, "Chartbeat",
        "Chartbeat analytics data collection"),
    "parsely.com": DomainInfo(
        CookieCategory.ANALYTICS, "Parse.ly (WordPress)",
        "Parse.ly content analytics for publishers"),
    "optimizely.com": DomainInfo(
        CookieCategory.ANALYTICS, "Optimizely",
        "Optimizely experimentation and A/B testing platform"),
    "newrelic.com": DomainInfo(
        CookieCategory.ANALYTICS, "New Relic",
        "New Relic application performance monitoring"),
    "nr-data.net": DomainInfo(
        CookieCategory.ANALYTICS, "New Relic",
        "New Relic browser monitoring data collection"),
    "sentry.io": DomainInfo(
        CookieCategory.ANALYTICS, "Sentry",
        "Sentry error tracking and performance monitoring"),
    "bugsnag.com": DomainInfo(
        CookieCategory.ANALYTICS, "Bugsnag",
        "Bugsnag error monitoring platform"),
    "hubspot.com": DomainInfo(
        CookieCategory.ANALYTICS, "HubSpot",
        "HubSpot marketing analytics and CRM platform"),
    "hs-analytics.net": DomainInfo(
        CookieCategory.ANALYTICS, "HubSpot",
        "HubSpot analytics data collection"),
    "hsforms.com": DomainInfo(
        CookieCategory.ANALYTICS, "HubSpot",
        "HubSpot form tracking"),
    "marketo.net": DomainInfo(
        CookieCategory.ANALYTICS, "Adobe (Marketo)",
        "Marketo marketing automation and lead tracking"),
    "marketo.com": DomainInfo(
        CookieCategory.ANALYTICS, "Adobe (Marketo)",
        "Marketo marketing automation platform"),
    "pardot.com": DomainInfo(
        CookieCategory.ANALYTICS, "Salesforce",
        "Pardot B2B marketing automation and tracking"),
    "salesforceliveagent.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "Salesforce",
        "Salesforce live chat agent"),
    "omtrdc.net": DomainInfo(
        CookieCategory.ANALYTICS, "Adobe",
        "Adobe Analytics (Omniture) data collection"),
    "2o7.net": DomainInfo(
        CookieCategory.ANALYTICS, "Adobe",
        "Adobe Analytics (legacy Omniture) tracking"),
    "demdex.net": DomainInfo(
        CookieCategory.ADVERTISING, "Adobe",
        "Adobe Audience Manager DMP"),
    "e-planning.net": DomainInfo(
        CookieCategory.ADVERTISING, "e-Planning",
        "e-Planning digital advertising platform"),
    "trustedstack.com": DomainInfo(
        CookieCategory.ADVERTISING, "TrustedStack",
        "TrustedStack advertising technology"),

    # ── Customer engagement / chat ──────────────────────────────
    "intercom.io": DomainInfo(
        CookieCategory.FUNCTIONAL, "Intercom",
        "Intercom customer messaging platform"),
    "intercomcdn.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "Intercom",
        "Intercom content delivery"),
    "drift.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "Drift",
        "Drift conversational marketing platform"),
    "zendesk.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "Zendesk",
        "Zendesk customer support platform"),
    "zopim.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "Zendesk",
        "Zendesk (Zopim) live chat widget"),
    "tawk.to": DomainInfo(
        CookieCategory.FUNCTIONAL, "Tawk.to",
        "Tawk.to free live chat widget"),
    "livechatinc.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "LiveChat",
        "LiveChat customer support platform"),
    "crisp.chat": DomainInfo(
        CookieCategory.FUNCTIONAL, "Crisp",
        "Crisp customer messaging platform"),

    # ── CDN / Infrastructure ────────────────────────────────────
    "cloudflare.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "Cloudflare",
        "Cloudflare CDN and security (bot protection, DDoS mitigation)"),
    "cloudfront.net": DomainInfo(
        CookieCategory.FUNCTIONAL, "Amazon (CloudFront)",
        "Amazon CloudFront content delivery network"),
    "akamai.net": DomainInfo(
        CookieCategory.FUNCTIONAL, "Akamai",
        "Akamai CDN and web performance"),
    "akamaihd.net": DomainInfo(
        CookieCategory.FUNCTIONAL, "Akamai",
        "Akamai HD content delivery"),
    "fastly.net": DomainInfo(
        CookieCategory.FUNCTIONAL, "Fastly",
        "Fastly edge cloud delivery"),
    "edgecastcdn.net": DomainInfo(
        CookieCategory.FUNCTIONAL, "Edgecast (Verizon)",
        "Edgecast content delivery network"),
    "jsdelivr.net": DomainInfo(
        CookieCategory.FUNCTIONAL, "jsDelivr",
        "jsDelivr open-source CDN for npm and GitHub"),
    "unpkg.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "Unpkg",
        "Unpkg CDN for npm packages"),

    # ── Authentication / Identity ───────────────────────────────
    "auth0.com": DomainInfo(
        CookieCategory.AUTHENTICATION, "Auth0 (Okta)",
        "Auth0 identity and authentication platform"),
    "okta.com": DomainInfo(
        CookieCategory.AUTHENTICATION, "Okta",
        "Okta enterprise identity and access management"),
    "duosecurity.com": DomainInfo(
        CookieCategory.AUTHENTICATION, "Cisco (Duo)",
        "Duo Security multi-factor authentication"),
    "onelogin.com": DomainInfo(
        CookieCategory.AUTHENTICATION, "OneLogin",
        "OneLogin identity and access management"),

    # ── Payment / E-commerce ────────────────────────────────────
    "stripe.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "Stripe",
        "Stripe payment processing and fraud prevention"),
    "paypal.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "PayPal",
        "PayPal payment processing"),
    "shopify.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "Shopify",
        "Shopify e-commerce platform"),

    # ── Consent management ──────────────────────────────────────
    "cookiebot.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "Cookiebot",
        "Cookiebot consent management platform"),
    "onetrust.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "OneTrust",
        "OneTrust privacy and consent management"),
    "cookielaw.org": DomainInfo(
        CookieCategory.FUNCTIONAL, "OneTrust",
        "OneTrust CookieLaw consent banner"),
    "trustarc.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "TrustArc",
        "TrustArc privacy compliance and consent management"),
    "osano.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "Osano",
        "Osano consent management platform"),

    # ── E-commerce / retail trackers ────────────────────────────
    "amazon.com": DomainInfo(
        CookieCategory.PERSONALIZATION, "Amazon",
        "Amazon e-commerce platform"),
    "ebay.com": DomainInfo(
        CookieCategory.PERSONALIZATION, "eBay",
        "eBay marketplace platform"),
    "wayfair.com": DomainInfo(
        CookieCategory.PERSONALIZATION, "Wayfair",
        "Wayfair home goods e-commerce"),
    "zillow.com": DomainInfo(
        CookieCategory.ANALYTICS, "Zillow",
        "Zillow real estate platform — tracks property searches and browsing"),

    # ── Video / media ───────────────────────────────────────────
    "youtube.com": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "Google (YouTube)",
        "YouTube video platform — tracks viewing history and preferences"),
    "ytimg.com": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "Google (YouTube)",
        "YouTube image/thumbnail delivery"),
    "vimeo.com": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "Vimeo",
        "Vimeo video hosting platform"),
    "jwpltx.com": DomainInfo(
        CookieCategory.ANALYTICS, "JW Player",
        "JW Player video analytics and performance tracking"),
    "spotify.com": DomainInfo(
        CookieCategory.SOCIAL_MEDIA, "Spotify",
        "Spotify music streaming platform"),

    # ── Email / marketing ───────────────────────────────────────
    "mailchimp.com": DomainInfo(
        CookieCategory.ANALYTICS, "Mailchimp",
        "Mailchimp email marketing platform"),
    "list-manage.com": DomainInfo(
        CookieCategory.ANALYTICS, "Mailchimp",
        "Mailchimp email campaign tracking"),
    "sendgrid.net": DomainInfo(
        CookieCategory.FUNCTIONAL, "Twilio (SendGrid)",
        "SendGrid email delivery service"),

    # ── Data brokers / identity graphs ──────────────────────────
    "tapad.com": DomainInfo(
        CookieCategory.ADVERTISING, "Tapad (Experian)",
        "Tapad cross-device identity graph for ad targeting"),
    "krxd.net": DomainInfo(
        CookieCategory.ADVERTISING, "Salesforce (Krux)",
        "Krux/Salesforce DMP data collection"),
    "agkn.com": DomainInfo(
        CookieCategory.ADVERTISING, "Neustar",
        "Neustar AdAdvisor audience targeting"),
    "ipredictive.com": DomainInfo(
        CookieCategory.ADVERTISING, "Alliant",
        "Alliant predictive audience data"),

    # ── Survey / feedback ───────────────────────────────────────
    "qualtrics.com": DomainInfo(
        CookieCategory.ANALYTICS, "Qualtrics",
        "Qualtrics experience management and surveys"),
    "surveymonkey.com": DomainInfo(
        CookieCategory.ANALYTICS, "SurveyMonkey",
        "SurveyMonkey survey platform"),
    "usabilla.com": DomainInfo(
        CookieCategory.ANALYTICS, "SurveyMonkey",
        "Usabilla user feedback and survey collection"),

    # ── A/B testing ─────────────────────────────────────────────
    "vwo.com": DomainInfo(
        CookieCategory.ANALYTICS, "VWO",
        "VWO (Visual Website Optimizer) A/B testing platform"),
    "abtasty.com": DomainInfo(
        CookieCategory.ANALYTICS, "AB Tasty",
        "AB Tasty experimentation and personalization"),
    "launchdarkly.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "LaunchDarkly",
        "LaunchDarkly feature flag and experimentation platform"),

    # ── Additional programmatic ad-tech ────────────────────────
    "a-mx.com": DomainInfo(
        CookieCategory.ADVERTISING, "Aniview",
        "Aniview video advertising platform"),
    "rtb.mx": DomainInfo(
        CookieCategory.ADVERTISING, "RTB.mx",
        "Real-time bidding ad exchange"),
    "a-mo.net": DomainInfo(
        CookieCategory.ADVERTISING, "Aniview",
        "Aniview ad-tech infrastructure"),
    "nexx360.io": DomainInfo(
        CookieCategory.ADVERTISING, "Nexx360",
        "Nexx360 server-side header bidding platform"),
    "nextmillmedia.com": DomainInfo(
        CookieCategory.ADVERTISING, "NextMillennium",
        "Next Millennium Media ad tech"),
    "sonobi.com": DomainInfo(
        CookieCategory.ADVERTISING, "Sonobi",
        "Sonobi programmatic advertising platform"),
    "smaato.net": DomainInfo(
        CookieCategory.ADVERTISING, "Smaato",
        "Smaato mobile programmatic ad platform"),
    "userreport.com": DomainInfo(
        CookieCategory.ANALYTICS, "UserReport",
        "UserReport audience measurement and survey tool"),
    "yieldlove.com": DomainInfo(
        CookieCategory.ADVERTISING, "Yieldlove",
        "Yieldlove programmatic ad optimization"),
    "gumgum.com": DomainInfo(
        CookieCategory.ADVERTISING, "GumGum",
        "GumGum contextual advertising platform"),
    "seedtag.com": DomainInfo(
        CookieCategory.ADVERTISING, "Seedtag",
        "Seedtag contextual advertising platform"),
    "justpremium.com": DomainInfo(
        CookieCategory.ADVERTISING, "JustPremium",
        "JustPremium high-impact ad formats"),
    "emxdgt.com": DomainInfo(
        CookieCategory.ADVERTISING, "EMX Digital",
        "EMX Digital programmatic ad exchange"),
    "connatix.com": DomainInfo(
        CookieCategory.ADVERTISING, "Connatix",
        "Connatix video advertising technology"),
    "outbrainimg.com": DomainInfo(
        CookieCategory.ADVERTISING, "Outbrain",
        "Outbrain content recommendation CDN"),
    "teads.tv": DomainInfo(
        CookieCategory.ADVERTISING, "Teads",
        "Teads outstream video advertising"),
    "33across.com": DomainInfo(
        CookieCategory.ADVERTISING, "33Across",
        "33Across attention-based ad exchange"),
    "undertone.com": DomainInfo(
        CookieCategory.ADVERTISING, "Undertone",
        "Undertone high-impact digital advertising"),
    "kargo.com": DomainInfo(
        CookieCategory.ADVERTISING, "Kargo",
        "Kargo mobile advertising platform"),
    "triplelift.com": DomainInfo(
        CookieCategory.ADVERTISING, "TripleLift",
        "TripleLift native programmatic exchange"),
    "richaudience.com": DomainInfo(
        CookieCategory.ADVERTISING, "Rich Audience",
        "Rich Audience programmatic ad platform"),
    "adform.net": DomainInfo(
        CookieCategory.ADVERTISING, "Adform",
        "Adform full-stack ad tech platform"),
    "adtelligent.com": DomainInfo(
        CookieCategory.ADVERTISING, "Adtelligent",
        "Adtelligent header bidding platform"),
    "connectad.io": DomainInfo(
        CookieCategory.ADVERTISING, "ConnectAd",
        "ConnectAd demand-side platform"),
    "freewheel.tv": DomainInfo(
        CookieCategory.ADVERTISING, "Comcast (FreeWheel)",
        "FreeWheel premium video ad management"),
    "spotxchange.com": DomainInfo(
        CookieCategory.ADVERTISING, "SpotX (Magnite)",
        "SpotX/Magnite video ad exchange"),
    "bfmio.com": DomainInfo(
        CookieCategory.ADVERTISING, "Beachfront",
        "Beachfront video ad platform"),
    "springserve.com": DomainInfo(
        CookieCategory.ADVERTISING, "SpringServe (Magnite)",
        "SpringServe video ad server"),
    "prebid.org": DomainInfo(
        CookieCategory.ADVERTISING, "Prebid",
        "Prebid open-source header bidding framework"),

    # ── Education ───────────────────────────────────────────────
    "brown.edu": DomainInfo(
        CookieCategory.FUNCTIONAL, "Brown University",
        "Brown University institutional services"),
    "instructure.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "Instructure (Canvas)",
        "Canvas learning management system"),
    "canvaslms.com": DomainInfo(
        CookieCategory.FUNCTIONAL, "Instructure (Canvas)",
        "Canvas LMS"),
}

# Domain name patterns that indicate ad-tech even without an exact DB match.
# Checked via substring in the domain string.
_ADTECH_DOMAIN_SIGNALS = [
    "rtb", "prebid", "bid", "adx", "adsrv", "adserv", "adtech",
    "tracker", "tracking", "pixel", "sync", "dsp", "ssp",
    "exchange", "programmatic", "yield", "demand", "supply",
]


def lookup_domain(domain: str) -> DomainInfo | None:
    """Look up a domain (or any of its parent domains) in the database."""
    clean = domain.lstrip(".")

    # Exact / suffix match against the curated DB
    parts = clean.split(".")
    for i in range(len(parts) - 1):
        candidate = ".".join(parts[i:])
        if candidate in DOMAIN_DB:
            return DOMAIN_DB[candidate]

    # Heuristic: domain name itself contains ad-tech signals
    domain_lower = clean.lower()
    for signal in _ADTECH_DOMAIN_SIGNALS:
        if signal in domain_lower:
            return DomainInfo(
                CookieCategory.ADVERTISING,
                clean.split(".")[-2].title() if len(parts) >= 2 else clean,
                f"Likely advertising infrastructure (domain contains '{signal}')",
            )

    return None
