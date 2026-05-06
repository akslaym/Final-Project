import { useState } from "react";
import type {
  ProfileReconstruction as ProfileData,
  ArchetypeEntry,
  CompositeInference,
} from "../types";

interface Props {
  profile: ProfileData;
}

const CONFIDENCE_STYLES: Record<string, string> = {
  very_likely: "border-purple-700/70 bg-purple-950/50 text-purple-200",
  likely: "border-violet-700/70 bg-violet-950/50 text-violet-200",
  possible: "border-yellow-700/60 bg-yellow-950/40 text-yellow-200",
  insufficient: "border-gray-700/40 bg-gray-900/30 text-gray-500",
};

const CONFIDENCE_LABELS: Record<string, string> = {
  very_likely: "Very Likely",
  likely: "Likely",
  possible: "Possible",
  insufficient: "Insufficient Evidence",
};

const CONFIDENCE_BAR: Record<string, string> = {
  very_likely: "bg-purple-500",
  likely: "bg-violet-500",
  possible: "bg-yellow-500",
  insufficient: "bg-gray-600",
};

export default function ProfileReconstruction({ profile }: Props) {
  const [showMethodology, setShowMethodology] = useState(false);
  const activated = profile.archetypes.filter((a) => a.activated);
  const nearMisses = profile.archetypes.filter(
    (a) => !a.activated && a.signals.length > 0
  );

  return (
    <div className="rounded-lg border border-gray-800 bg-gray-900 p-4 sm:p-5">
      <div className="mb-4 flex items-start justify-between gap-3">
        <div>
          <h2 className="font-mono text-[10px] font-semibold uppercase tracking-wider text-gray-500 sm:text-xs">
            Profile Reconstruction
          </h2>
          <p className="mt-1 text-[10px] text-gray-600 sm:text-xs">
            What a third party could infer by combining your cookies
          </p>
        </div>
        <button
          onClick={() => setShowMethodology(!showMethodology)}
          className="shrink-0 rounded border border-gray-700 px-2 py-1 text-[10px] text-gray-400 transition hover:border-gray-500 hover:text-gray-200"
        >
          {showMethodology ? "Hide" : "How this works"}
        </button>
      </div>

      {showMethodology && <MethodologyPanel disclaimer={profile.disclaimer} />}

      <p className="mb-4 text-sm leading-relaxed text-gray-300">
        {profile.summary}
      </p>

      {profile.composites.length > 0 && (
        <div className="mb-4 space-y-2">
          {profile.composites.map((c, i) => (
            <CompositeCard key={i} composite={c} archetypes={activated} />
          ))}
        </div>
      )}

      {activated.length > 0 && (
        <div className="mb-4">
          <h3 className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-gray-500">
            Detected Archetypes ({activated.length})
          </h3>
          <div className="space-y-2">
            {activated.map((a) => (
              <ArchetypeCard key={a.id} archetype={a} />
            ))}
          </div>
        </div>
      )}

      {nearMisses.length > 0 && <NearMisses archetypes={nearMisses} />}
    </div>
  );
}

function MethodologyPanel({ disclaimer }: { disclaimer: string }) {
  return (
    <div className="mb-4 rounded border border-blue-900/40 bg-blue-950/20 p-3 text-xs leading-relaxed text-blue-300/80">
      <p className="mb-2 font-medium text-blue-200">Methodology</p>
      <p className="mb-2">{disclaimer}</p>
      <ul className="space-y-1 text-[11px] text-blue-300/60">
        <li>
          <span className="text-blue-400">•</span> Each archetype requires{" "}
          <strong>3+ independent domain signals</strong> to activate
        </li>
        <li>
          <span className="text-blue-400">•</span> Confidence scales with
          signal count: 3 = possible, 5+ = likely, 7+ = very likely
        </li>
        <li>
          <span className="text-blue-400">•</span> Composite inferences emerge
          only when multiple archetypes are independently confirmed
        </li>
        <li>
          <span className="text-blue-400">•</span> Click any archetype to see
          exactly which cookies contributed
        </li>
      </ul>
    </div>
  );
}

function ArchetypeCard({ archetype }: { archetype: ArchetypeEntry }) {
  const [expanded, setExpanded] = useState(false);
  const style = CONFIDENCE_STYLES[archetype.confidence] ?? CONFIDENCE_STYLES.insufficient;
  const bar = CONFIDENCE_BAR[archetype.confidence] ?? CONFIDENCE_BAR.insufficient;

  return (
    <div
      className={`cursor-pointer rounded border p-3 transition hover:brightness-110 ${style}`}
      onClick={() => setExpanded(!expanded)}
    >
      <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between sm:gap-2">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-sm font-medium">{archetype.label}</span>
            <span className="rounded bg-black/20 px-1.5 py-0.5 text-[10px] opacity-80">
              {CONFIDENCE_LABELS[archetype.confidence]}
            </span>
          </div>
          <p className="mt-0.5 text-[11px] opacity-70">
            {archetype.description}
          </p>
        </div>
        <span className="shrink-0 text-[10px] opacity-60">
          {archetype.signals.length} signal
          {archetype.signals.length !== 1 ? "s" : ""} (need{" "}
          {archetype.threshold})
        </span>
      </div>

      <div className="mt-2 h-1 w-full rounded-full bg-black/30">
        <div
          className={`h-full rounded-full transition-all ${bar}`}
          style={{
            width: `${Math.min(archetype.confidence_score * 100, 100)}%`,
          }}
        />
      </div>

      {expanded && (
        <div className="mt-3 border-t border-white/10 pt-2">
          <p className="mb-1.5 text-[10px] font-semibold uppercase tracking-wider opacity-60">
            Evidence ({archetype.signals.length} cookies)
          </p>
          <div className="space-y-1">
            {archetype.signals.map((s, i) => (
              <div
                key={i}
                className="flex items-start gap-2 text-[11px] opacity-70"
              >
                <span className="mt-0.5 shrink-0 opacity-50">&rsaquo;</span>
                <div className="min-w-0">
                  <span className="font-mono text-[10px]">
                    {s.cookie_name}
                  </span>
                  <span className="mx-1 opacity-40">from</span>
                  <span className="font-mono text-[10px] break-all">
                    {s.cookie_domain}
                  </span>
                  <p className="text-[10px] opacity-50">{s.reason}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <span className="mt-1 block text-[10px] opacity-40">
        {expanded ? "Click to collapse" : "Click to see evidence"}
      </span>
    </div>
  );
}

function CompositeCard({
  composite,
  archetypes,
}: {
  composite: CompositeInference;
  archetypes: ArchetypeEntry[];
}) {
  const [expanded, setExpanded] = useState(false);
  const contributing = archetypes.filter((a) =>
    composite.archetype_ids.includes(a.id)
  );

  return (
    <div
      className="cursor-pointer rounded border border-purple-800/50 bg-purple-950/30 p-3 transition hover:border-purple-700/60"
      onClick={() => setExpanded(!expanded)}
    >
      <div className="flex items-start gap-2">
        <span className="mt-0.5 shrink-0 text-purple-400">&Delta;</span>
        <div className="min-w-0">
          <p className="text-sm font-medium text-purple-200">
            {composite.inference}
          </p>
          <p className="mt-0.5 text-[11px] text-purple-300/60">
            Combined from: {contributing.map((a) => a.label).join(" + ")}
          </p>
          {expanded && (
            <p className="mt-2 text-xs leading-relaxed text-purple-300/50">
              {composite.explanation}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

function NearMisses({ archetypes }: { archetypes: ArchetypeEntry[] }) {
  const [expanded, setExpanded] = useState(false);
  const sorted = [...archetypes].sort(
    (a, b) => b.signals.length - a.signals.length
  );
  const visible = expanded ? sorted : sorted.slice(0, 3);

  return (
    <div className="border-t border-gray-800 pt-3">
      <h3 className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-gray-600">
        Near Threshold (not enough evidence to confirm)
      </h3>
      <div className="space-y-1.5">
        {visible.map((a) => (
          <div
            key={a.id}
            className="flex items-center justify-between gap-2 rounded border border-gray-800/50 bg-gray-950/30 px-2.5 py-1.5"
          >
            <div className="flex items-center gap-2 min-w-0">
              <span className="truncate text-xs text-gray-500">{a.label}</span>
              <span className="shrink-0 text-[10px] text-gray-600">
                {a.signals.length}/{a.threshold}
              </span>
            </div>
            <div className="h-1 w-16 shrink-0 rounded-full bg-gray-800">
              <div
                className="h-full rounded-full bg-gray-600"
                style={{
                  width: `${(a.signals.length / a.threshold) * 100}%`,
                }}
              />
            </div>
          </div>
        ))}
      </div>
      {sorted.length > 3 && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="mt-2 text-[10px] text-gray-600 underline decoration-gray-700 hover:text-gray-400"
        >
          {expanded ? "Show fewer" : `+${sorted.length - 3} more`}
        </button>
      )}
    </div>
  );
}
