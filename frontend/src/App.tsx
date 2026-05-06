import { useCallback, useEffect, useRef, useState } from "react";
import type { AnalysisResult } from "./types";
import { analyzeCookies, pollBrowser } from "./api/client";
import FileUpload from "./components/FileUpload";
import Dashboard from "./components/Dashboard";

const POLL_INTERVAL = 60_000;

function App() {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [polling, setPolling] = useState(false);
  const [pollInfo, setPollInfo] = useState<string>("");
  const scanProfileRef = useRef<string | null>(null);
  const pollTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const doPoll = useCallback(async () => {
    if (!scanProfileRef.current) return;
    try {
      const res = await pollBrowser("chrome", scanProfileRef.current);
      if (res.changed && res.result) {
        setResult(res.result);
        const parts: string[] = [];
        if (res.new_cookie_count > 0) parts.push(`+${res.new_cookie_count} new`);
        if (res.removed_cookie_count > 0) parts.push(`-${res.removed_cookie_count} removed`);
        setPollInfo(parts.join(", ") + ` (${res.total_cookie_count} total)`);
      } else {
        setPollInfo(`No changes (${res.total_cookie_count} cookies)`);
      }
    } catch {
      setPollInfo("Poll failed");
    }
  }, []);

  function startPolling(profile: string) {
    scanProfileRef.current = profile;
    setPolling(true);
    if (pollTimerRef.current) clearInterval(pollTimerRef.current);
    pollTimerRef.current = setInterval(doPoll, POLL_INTERVAL);
  }

  function stopPolling() {
    setPolling(false);
    scanProfileRef.current = null;
    if (pollTimerRef.current) {
      clearInterval(pollTimerRef.current);
      pollTimerRef.current = null;
    }
  }

  useEffect(() => {
    return () => {
      if (pollTimerRef.current) clearInterval(pollTimerRef.current);
    };
  }, []);

  function handleScanResult(data: AnalysisResult, profile: string) {
    setResult(data);
    startPolling(profile);
  }

  async function handleUpload(cookies: Record<string, unknown>[]) {
    setLoading(true);
    setError(null);
    stopPolling();
    try {
      const data = await analyzeCookies(cookies);
      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Analysis failed");
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setResult(null);
    setError(null);
    stopPolling();
    setPollInfo("");
  }

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 px-6 py-4">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <h1 className="font-mono text-xl font-bold tracking-tight">
            COOKIE CONSCIOUS
          </h1>
          <div className="flex items-center gap-3">
            {polling && (
              <button
                onClick={stopPolling}
                className="rounded border border-gray-700 px-2 py-1 text-[10px] text-gray-500 hover:bg-gray-800 hover:text-gray-300 sm:text-xs"
              >
                Stop live
              </button>
            )}
            {result && (
              <button
                onClick={handleReset}
                className="rounded border border-gray-700 px-3 py-1 text-sm text-gray-400 hover:bg-gray-800 hover:text-gray-200"
              >
                New analysis
              </button>
            )}
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl p-6">
        {error && (
          <div className="mb-4 rounded border border-red-800 bg-red-950 px-4 py-3 text-red-300">
            {error}
          </div>
        )}

        {!result ? (
          <FileUpload
            onResult={handleScanResult}
            onUpload={handleUpload}
            loading={loading}
          />
        ) : (
          <Dashboard result={result} polling={polling} lastPollInfo={pollInfo} />
        )}
      </main>

      <footer className="border-t border-gray-800 px-6 py-4 text-center text-xs text-gray-600">
        Consent classifications are inferred and may not reflect a site's
        actual practices. All analysis runs locally — no data leaves your
        machine.
      </footer>
    </div>
  );
}

export default App;
