import type { AnalysisResult } from "../types";
import CookieTable from "./CookieTable";
import ConsentBreakdown from "./ConsentBreakdown";
import StoryCard from "./StoryCard";
import CompanyStories from "./CompanyStories";
import ProfileReconstruction from "./ProfileReconstruction";

interface Props {
  result: AnalysisResult;
  polling?: boolean;
  lastPollInfo?: string;
}

export default function Dashboard({ result, polling, lastPollInfo }: Props) {
  return (
    <div className="space-y-6">
      {polling && (
        <div className="flex items-center gap-2 text-[10px] text-gray-500 sm:text-xs">
          <span className="inline-block h-2 w-2 animate-pulse rounded-full bg-green-500" />
          Live monitoring
          {lastPollInfo && (
            <span className="text-gray-600">&mdash; {lastPollInfo}</span>
          )}
        </div>
      )}

      <div className="grid gap-4 sm:grid-cols-2">
        <ConsentBreakdown consent={result.consent} />
        <StoryCard story={result.story} />
      </div>

      {result.story.profile && (
        <ProfileReconstruction profile={result.story.profile} />
      )}

      {result.story.company_stories.length > 0 && (
        <CompanyStories stories={result.story.company_stories} />
      )}

      <CookieTable
        cookies={result.cookies}
        consent={result.consent}
      />
    </div>
  );
}
