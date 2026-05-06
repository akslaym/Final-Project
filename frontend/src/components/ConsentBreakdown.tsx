import type { DomainConsent, ConsentType } from "../types";

interface Props {
  consent: DomainConsent[];
}

const COLORS: Record<ConsentType, { bar: string; text: string; label: string }> = {
  tacit: { bar: "bg-red-500", text: "text-red-400", label: "Silent \u2014 no prompt shown" },
  implied: { bar: "bg-yellow-500", text: "text-yellow-400", label: "Inferred from continued usage" },
  explicit: { bar: "bg-green-500", text: "text-green-400", label: "User actively opted in" },
  unknown: { bar: "bg-gray-600", text: "text-gray-400", label: "Could not determine" },
};

export default function ConsentBreakdown({ consent }: Props) {
  const counts: Record<string, number> = {};
  for (const c of consent) {
    counts[c.consent_type] = (counts[c.consent_type] || 0) + 1;
  }
  const total = consent.length || 1;

  return (
    <div className="rounded-lg border border-gray-800 bg-gray-900 p-4">
      <h2 className="mb-2 font-mono text-[10px] font-semibold uppercase tracking-wider text-gray-500 sm:text-xs">
        Consent Types
      </h2>

      <div className="space-y-2.5">
        {(["tacit", "implied", "explicit", "unknown"] as ConsentType[]).map((type) => {
          const count = counts[type] || 0;
          if (count === 0) return null;
          const pct = (count / total) * 100;
          const info = COLORS[type];
          return (
            <div key={type}>
              <div className="mb-0.5 flex items-baseline justify-between">
                <span className={`text-xs font-medium capitalize ${info.text}`}>
                  {type}
                </span>
                <span className="text-[10px] text-gray-500">
                  {count} domain{count !== 1 ? "s" : ""} ({Math.round(pct)}%)
                </span>
              </div>
              <div className="h-1.5 overflow-hidden rounded-full bg-gray-800">
                <div className={`h-full rounded-full ${info.bar}`} style={{ width: `${pct}%` }} />
              </div>
              <p className="mt-0.5 text-[10px] text-gray-600">{info.label}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
