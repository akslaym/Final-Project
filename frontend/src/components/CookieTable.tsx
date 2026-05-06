import { useState } from "react";
import type { CategorizedCookie, DomainConsent } from "../types";

interface Props {
  cookies: CategorizedCookie[];
  consent: DomainConsent[];
}

function formatAge(unixStr: string): string {
  const ts = parseInt(unixStr, 10);
  if (isNaN(ts)) return "unknown";
  const diff = Math.floor(Date.now() / 1000) - ts;
  if (diff < 0) return "future";
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`;
  if (diff < 2592000) return `${Math.floor(diff / 604800)}w ago`;
  return `${Math.floor(diff / 2592000)}mo ago`;
}

const CONSENT_BADGE: Record<string, string> = {
  tacit: "bg-red-900/60 text-red-300 border-red-800",
  implied: "bg-yellow-900/60 text-yellow-300 border-yellow-800",
  explicit: "bg-green-900/60 text-green-300 border-green-800",
  unknown: "bg-gray-800 text-gray-500 border-gray-700",
};

const CATEGORY_COLOR: Record<string, string> = {
  advertising: "text-red-400",
  analytics: "text-yellow-400",
  social_media: "text-purple-400",
  authentication: "text-blue-400",
  session: "text-cyan-400",
  functional: "text-gray-400",
  personalization: "text-green-400",
  unknown: "text-gray-500",
};

interface DomainGroup {
  domain: string;
  cookies: CategorizedCookie[];
  consent: DomainConsent | undefined;
  topCategory: string;
}

function groupByDomain(
  cookies: CategorizedCookie[],
  consentList: DomainConsent[]
): DomainGroup[] {
  const map = new Map<string, CategorizedCookie[]>();

  cookies.forEach((c) => {
    const d = c.raw.domain.replace(/^\./, "");
    const entry = map.get(d) ?? [];
    entry.push(c);
    map.set(d, entry);
  });

  return Array.from(map.entries())
    .map(([domain, cc]) => {
      const cats = cc.reduce<Record<string, number>>((a, c) => {
        a[c.category] = (a[c.category] || 0) + 1;
        return a;
      }, {});
      const topCat = Object.entries(cats).sort(([, a], [, b]) => b - a)[0]?.[0] ?? "unknown";
      const consent = consentList.find(
        (cn) => domain === cn.domain || domain.endsWith("." + cn.domain) || cn.domain.endsWith(domain)
      );
      return { domain, cookies: cc, consent, topCategory: topCat };
    })
    .sort((a, b) => b.cookies.length - a.cookies.length);
}

function DomainRow({ group }: { group: DomainGroup }) {
  const [open, setOpen] = useState(false);
  const consentType = group.consent?.consent_type ?? "unknown";

  return (
    <>
      <tr
        onClick={() => setOpen(!open)}
        className="cursor-pointer border-b border-gray-800 hover:bg-gray-900/70"
      >
        <td className="px-3 py-2.5 sm:px-4">
          <div className="flex items-center gap-2">
            <span className="text-[10px] text-gray-600">{open ? "\u25BC" : "\u25B6"}</span>
            <div className="min-w-0">
              <span className="block truncate font-mono text-xs text-gray-200 sm:text-sm">
                {group.domain}
              </span>
              <span className="block text-[10px] text-gray-500 sm:text-xs">
                {group.cookies.length} cookie{group.cookies.length !== 1 ? "s" : ""}
                {group.cookies[0]?.vendor && ` \u00B7 ${group.cookies[0].vendor}`}
              </span>
            </div>
          </div>
        </td>
        <td className="hidden px-3 py-2.5 sm:table-cell sm:px-4">
          <span className={`text-xs font-medium capitalize ${CATEGORY_COLOR[group.topCategory]}`}>
            {group.topCategory.replace("_", " ")}
          </span>
        </td>
        <td className="px-3 py-2.5 sm:px-4">
          <span
            className={`inline-block rounded border px-1.5 py-0.5 text-[10px] font-medium capitalize sm:text-xs ${CONSENT_BADGE[consentType]}`}
            title={group.consent?.evidence}
          >
            {consentType}
          </span>
        </td>
      </tr>
      {open &&
        group.cookies.map((cookie, j) => (
          <tr key={j} className="border-b border-gray-800/50 bg-gray-900/30">
            <td colSpan={3} className="px-3 py-2 pl-8 sm:px-4 sm:pl-10">
              <div className="flex flex-col gap-0.5">
                <span className="font-mono text-xs text-gray-300">{cookie.raw.name}</span>
                <span className="text-[10px] leading-snug text-gray-500 sm:text-xs">
                  {cookie.purpose}
                </span>
                <div className="mt-0.5 flex flex-wrap gap-2 text-[10px] text-gray-600">
                  {cookie.raw.secure && <span>Secure</span>}
                  {cookie.raw.http_only && <span>HttpOnly</span>}
                  {cookie.raw.same_site && <span>SameSite={cookie.raw.same_site}</span>}
                  {!cookie.raw.is_persistent && <span className="text-cyan-500">Session-only</span>}
                  {cookie.raw.top_frame_site && (
                    <span>Set on: {cookie.raw.top_frame_site}</span>
                  )}
                  {cookie.raw.created_at && (
                    <span>Created: {formatAge(cookie.raw.created_at)}</span>
                  )}
                  {cookie.raw.last_accessed && (
                    <span>Last used: {formatAge(cookie.raw.last_accessed)}</span>
                  )}
                </div>
              </div>
            </td>
          </tr>
        ))}
    </>
  );
}

export default function CookieTable({ cookies, consent }: Props) {
  const groups = groupByDomain(cookies, consent);

  return (
    <div className="overflow-hidden rounded-lg border border-gray-800">
      <div className="border-b border-gray-800 bg-gray-900 px-3 py-3 sm:px-4">
        <h2 className="font-mono text-xs font-semibold tracking-wider text-gray-300 sm:text-sm">
          {groups.length} DOMAINS \u00B7 {cookies.length} COOKIES
        </h2>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-gray-800 bg-gray-900/50 text-[10px] uppercase text-gray-500 sm:text-xs">
            <tr>
              <th className="px-3 py-2.5 sm:px-4">Domain</th>
              <th className="hidden px-3 py-2.5 sm:table-cell sm:px-4">Category</th>
              <th className="px-3 py-2.5 sm:px-4">Consent</th>
            </tr>
          </thead>
          <tbody>
            {groups.map((g) => (
              <DomainRow key={g.domain} group={g} />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
