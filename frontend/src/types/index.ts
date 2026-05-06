export type CookieCategory =
  | "advertising"
  | "analytics"
  | "functional"
  | "session"
  | "authentication"
  | "personalization"
  | "social_media"
  | "unknown";

export type ConsentType = "tacit" | "implied" | "explicit" | "unknown";

export interface RawCookie {
  name: string;
  value: string;
  domain: string;
  path: string;
  expires: string | null;
  secure: boolean;
  http_only: boolean;
  same_site: string | null;
  created_at: string | null;
  last_accessed: string | null;
  top_frame_site: string | null;
  is_persistent: boolean;
}

export interface CategorizedCookie {
  raw: RawCookie;
  category: CookieCategory;
  purpose: string;
  vendor: string | null;
}

export interface DomainConsent {
  domain: string;
  consent_type: ConsentType;
  confidence: number;
  evidence: string;
}

export interface InferredTrait {
  trait: string;
  confidence: string;
  sources: string[];
}

export interface CompanyStory {
  company: string;
  domains: string[];
  cookie_count: number;
  insight: string;
  data_points: string[];
  risk_level: string;
}

export interface ArchetypeSignal {
  cookie_name: string;
  cookie_domain: string;
  reason: string;
}

export interface ArchetypeEntry {
  id: string;
  label: string;
  description: string;
  confidence: string;
  confidence_score: number;
  signals: ArchetypeSignal[];
  threshold: number;
  activated: boolean;
}

export interface CompositeInference {
  inference: string;
  archetype_ids: string[];
  explanation: string;
}

export interface ProfileReconstruction {
  archetypes: ArchetypeEntry[];
  composites: CompositeInference[];
  summary: string;
  disclaimer: string;
}

export interface Story {
  narrative: string;
  traits: InferredTrait[];
  company_stories: CompanyStory[];
  profile: ProfileReconstruction | null;
  cookie_count: number;
  domain_count: number;
}

export interface AnalysisResult {
  cookies: CategorizedCookie[];
  consent: DomainConsent[];
  story: Story;
  scan_timestamp: number | null;
}

export interface PollResult {
  changed: boolean;
  new_cookie_count: number;
  removed_cookie_count: number;
  total_cookie_count: number;
  result: AnalysisResult | null;
}
