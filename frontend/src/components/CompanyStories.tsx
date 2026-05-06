import { useState } from "react";
import type { CompanyStory } from "../types";

interface Props {
  stories: CompanyStory[];
}

const RISK_BADGE: Record<string, string> = {
  high: "border-red-800/60 bg-red-950/40 text-red-300",
  medium: "border-yellow-800/60 bg-yellow-950/40 text-yellow-300",
  low: "border-gray-700 bg-gray-800/40 text-gray-400",
};

export default function CompanyStories({ stories }: Props) {
  const [showAll, setShowAll] = useState(false);
  const visible = showAll ? stories : stories.slice(0, 6);

  if (stories.length === 0) return null;

  return (
    <div className="rounded-lg border border-gray-800 bg-gray-900 p-4">
      <h2 className="mb-3 font-mono text-[10px] font-semibold uppercase tracking-wider text-gray-500 sm:text-xs">
        Per-Company Insights ({stories.length})
      </h2>

      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        {visible.map((s) => (
          <CompanyCard key={s.company} story={s} />
        ))}
      </div>

      {stories.length > 6 && (
        <button
          onClick={() => setShowAll(!showAll)}
          className="mt-3 text-[10px] text-gray-500 underline decoration-gray-700 hover:text-gray-300 sm:text-xs"
        >
          {showAll ? "Show fewer" : `+${stories.length - 6} more companies`}
        </button>
      )}
    </div>
  );
}

function CompanyCard({ story }: { story: CompanyStory }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div
      className="cursor-pointer rounded border border-gray-800 bg-gray-950/50 p-3 transition hover:border-gray-700"
      onClick={() => setExpanded(!expanded)}
    >
      <div className="mb-1.5 flex items-start justify-between gap-2">
        <div className="min-w-0">
          <span className="block truncate text-sm font-medium text-gray-200">
            {story.company}
          </span>
          <span className="text-[10px] text-gray-500">
            {story.cookie_count} cookie{story.cookie_count !== 1 ? "s" : ""}
            {story.domains.length > 1 &&
              ` across ${story.domains.length} domains`}
          </span>
        </div>
        <span
          className={`shrink-0 rounded border px-1.5 py-0.5 text-[10px] font-medium ${
            RISK_BADGE[story.risk_level] ?? RISK_BADGE.low
          }`}
        >
          {story.risk_level}
        </span>
      </div>

      <p className="text-xs leading-relaxed text-gray-400">{story.insight}</p>

      {expanded && story.data_points.length > 0 && (
        <ul className="mt-2 space-y-1">
          {story.data_points.map((dp, i) => (
            <li key={i} className="text-[10px] leading-snug text-gray-500 sm:text-xs">
              <span className="mr-1 text-gray-600">&bull;</span>
              {dp}
            </li>
          ))}
        </ul>
      )}

      {story.data_points.length > 0 && (
        <span className="mt-1.5 block text-[10px] text-gray-600">
          {expanded ? "Click to collapse" : "Click for details"}
        </span>
      )}
    </div>
  );
}
