import { useState } from "react";
import type { Story } from "../types";

interface Props {
  story: Story;
}

const CONFIDENCE_STYLE: Record<string, string> = {
  high: "border-red-800/60 bg-red-950/40 text-red-300",
  medium: "border-yellow-800/60 bg-yellow-950/40 text-yellow-300",
  low: "border-gray-700 bg-gray-800/40 text-gray-300",
};

export default function StoryCard({ story }: Props) {
  const [expanded, setExpanded] = useState(false);
  const visibleTraits = expanded ? story.traits : story.traits.slice(0, 4);

  return (
    <div className="rounded-lg border border-gray-800 bg-gray-900 p-4 sm:col-span-2 xl:col-span-1">
      <h2 className="mb-2 font-mono text-[10px] font-semibold uppercase tracking-wider text-gray-500 sm:text-xs">
        Story Reconstruction
      </h2>

      <p className="mb-3 text-xs leading-relaxed text-gray-300">
        {story.narrative}
      </p>

      {story.traits.length > 0 && (
        <div className="space-y-1.5">
          {visibleTraits.map((trait, i) => (
            <div
              key={i}
              className={`rounded border px-2.5 py-1.5 text-xs ${
                CONFIDENCE_STYLE[trait.confidence] ?? CONFIDENCE_STYLE.low
              }`}
            >
              <span className="font-medium">{trait.trait}</span>
              <span className="ml-1.5 text-[10px] opacity-60">
                ({trait.confidence})
              </span>
            </div>
          ))}
          {story.traits.length > 4 && (
            <button
              onClick={() => setExpanded(!expanded)}
              className="text-[10px] text-gray-500 underline decoration-gray-700 hover:text-gray-300 sm:text-xs"
            >
              {expanded
                ? "Show fewer"
                : `+${story.traits.length - 4} more traits`}
            </button>
          )}
        </div>
      )}

      <p className="mt-3 text-[10px] text-gray-600">
        Inferred from {story.cookie_count.toLocaleString()} cookies across{" "}
        {story.domain_count.toLocaleString()} domain{story.domain_count !== 1 ? "s" : ""}.
      </p>
    </div>
  );
}
