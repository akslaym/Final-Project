from enum import Enum

from pydantic import BaseModel


class ConsentType(str, Enum):
    TACIT = "tacit"
    IMPLIED = "implied"
    EXPLICIT = "explicit"
    UNKNOWN = "unknown"


class DomainConsent(BaseModel):
    domain: str
    consent_type: ConsentType
    confidence: float
    evidence: str
