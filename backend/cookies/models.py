from enum import Enum
from pydantic import BaseModel


class CookieCategory(str, Enum):
    ADVERTISING = "advertising"
    ANALYTICS = "analytics"
    FUNCTIONAL = "functional"
    SESSION = "session"
    AUTHENTICATION = "authentication"
    PERSONALIZATION = "personalization"
    SOCIAL_MEDIA = "social_media"
    UNKNOWN = "unknown"


class RawCookie(BaseModel):
    name: str
    value: str
    domain: str
    path: str = "/"
    expires: str | None = None
    secure: bool = False
    http_only: bool = False
    same_site: str | None = None
    created_at: str | None = None       # Unix timestamp when cookie was first set
    last_accessed: str | None = None    # Unix timestamp of last access
    top_frame_site: str | None = None   # Site user was visiting when cookie was set
    is_persistent: bool = True          # False = session cookie


class CategorizedCookie(BaseModel):
    raw: RawCookie
    category: CookieCategory
    purpose: str
    vendor: str | None = None
