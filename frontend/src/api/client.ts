import type { AnalysisResult, PollResult } from "../types";

const API_BASE = "http://localhost:8000";

export interface BrowserProfile {
  browser: string;
  profile_name: string;
  cookie_count: number;
}

export async function discoverProfiles(): Promise<BrowserProfile[]> {
  const res = await fetch(`${API_BASE}/api/browser/profiles`);
  if (!res.ok) throw new Error("Could not discover browser profiles");
  return res.json();
}

export async function scanBrowser(
  browser: string = "chrome",
  profile: string = "all"
): Promise<AnalysisResult> {
  const res = await fetch(`${API_BASE}/api/browser/scan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ browser, profile }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Scan failed (${res.status}): ${text}`);
  }
  return res.json();
}

export async function pollBrowser(
  browser: string = "chrome",
  profile: string = "all"
): Promise<PollResult> {
  const res = await fetch(`${API_BASE}/api/browser/poll`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ browser, profile }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Poll failed (${res.status}): ${text}`);
  }
  return res.json();
}

export async function analyzeCookies(
  cookies: Record<string, unknown>[]
): Promise<AnalysisResult> {
  const res = await fetch(`${API_BASE}/api/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ cookies }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Analysis failed (${res.status}): ${text}`);
  }
  return res.json();
}
