from pydantic import BaseModel


class InferredTrait(BaseModel):
    trait: str
    confidence: str
    sources: list[str]


class CompanyStory(BaseModel):
    company: str
    domains: list[str]
    cookie_count: int
    insight: str
    data_points: list[str]
    risk_level: str


class ArchetypeSignal(BaseModel):
    cookie_name: str
    cookie_domain: str
    reason: str


class ArchetypeEntry(BaseModel):
    id: str
    label: str
    description: str
    confidence: str
    confidence_score: float
    signals: list[ArchetypeSignal]
    threshold: int
    activated: bool


class CompositeInferenceEntry(BaseModel):
    inference: str
    archetype_ids: list[str]
    explanation: str


class ProfileReconstructionResponse(BaseModel):
    archetypes: list[ArchetypeEntry]
    composites: list[CompositeInferenceEntry]
    summary: str
    disclaimer: str


class Story(BaseModel):
    narrative: str
    traits: list[InferredTrait]
    company_stories: list[CompanyStory]
    profile: ProfileReconstructionResponse | None = None
    cookie_count: int
    domain_count: int
