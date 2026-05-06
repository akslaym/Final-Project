from pydantic import BaseModel


class CookieRisk(BaseModel):
    cookie_name: str
    cookie_domain: str
    score: float
    factors: list[str]


class AggregateRisk(BaseModel):
    score: float
    label: str
    summary: str
    category_breakdown: dict[str, float]
    top_factors: list[str]
