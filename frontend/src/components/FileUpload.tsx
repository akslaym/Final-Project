import { useEffect, useRef, useState } from "react";
import {
  discoverProfiles,
  scanBrowser,
  type BrowserProfile,
} from "../api/client";
import type { AnalysisResult } from "../types";

interface Props {
  onResult: (result: AnalysisResult, profile: string) => void;
  onUpload: (cookies: Record<string, unknown>[]) => void;
  loading: boolean;
}

export default function FileUpload({ onResult, onUpload, loading }: Props) {
  const [profiles, setProfiles] = useState<BrowserProfile[] | null>(null);
  const [profileError, setProfileError] = useState<string | null>(null);
  const [scanning, setScanning] = useState(false);
  const [text, setText] = useState("");
  const [showManual, setShowManual] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    discoverProfiles()
      .then(setProfiles)
      .catch(() => setProfileError("Could not connect to backend. Is it running on localhost:8000?"));
  }, []);

  async function handleScan(profile: string) {
    setScanning(true);
    try {
      const result = await scanBrowser("chrome", profile);
      onResult(result, profile);
    } catch (e) {
      setProfileError(e instanceof Error ? e.message : "Scan failed");
    } finally {
      setScanning(false);
    }
  }

  function handleFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const parsed = JSON.parse(reader.result as string);
        onUpload(Array.isArray(parsed) ? parsed : [parsed]);
      } catch {
        setText("Invalid JSON file");
      }
    };
    reader.readAsText(file);
  }

  function handlePaste() {
    try {
      const parsed = JSON.parse(text);
      onUpload(Array.isArray(parsed) ? parsed : [parsed]);
    } catch {
      setText("Invalid JSON \u2014 paste a JSON array of cookie objects");
    }
  }

  const isLoading = loading || scanning;

  return (
    <div className="flex flex-col items-center gap-8 pt-12">
      <div className="text-center">
        <h2 className="mb-2 font-mono text-3xl font-bold tracking-tight">
          What do your cookies say about you?
        </h2>
        <p className="text-gray-400">
          Scan your browser's cookies directly, or upload exported cookie data.
        </p>
      </div>

      <div className="w-full max-w-2xl rounded-lg border border-gray-800 bg-gray-900 p-6">
        <h3 className="mb-4 font-mono text-sm font-semibold uppercase tracking-wider text-gray-400">
          Scan browser cookies
        </h3>

        {profileError && (
          <p className="mb-3 text-sm text-red-400">{profileError}</p>
        )}

        {profiles === null && !profileError && (
          <p className="text-sm text-gray-500">Detecting browser profiles...</p>
        )}

        {profiles && profiles.length === 0 && (
          <p className="text-sm text-gray-500">
            No Chrome profiles found. Use the manual upload below.
          </p>
        )}

        {profiles && profiles.length > 0 && (
          <div className="space-y-2">
            {profiles.map((p) => (
              <button
                key={`${p.browser}-${p.profile_name}`}
                onClick={() => handleScan(p.profile_name)}
                disabled={isLoading}
                className="flex w-full items-center justify-between rounded-lg border border-gray-700 px-4 py-3 text-left transition hover:border-gray-500 hover:bg-gray-800 disabled:opacity-50"
              >
                <div>
                  <span className="text-sm font-medium text-gray-200">
                    Chrome / {p.profile_name}
                  </span>
                  <span className="ml-3 text-xs text-gray-500">
                    {p.cookie_count.toLocaleString()} cookies
                  </span>
                </div>
                <span className="text-xs text-gray-500">
                  {isLoading ? "Scanning..." : "Scan"}
                </span>
              </button>
            ))}
          </div>
        )}

        <p className="mt-3 text-xs text-gray-600">
          Reads cookie metadata (name, domain, flags) from Chrome's local
          database. No values are read. No data leaves your machine.
        </p>
      </div>

      <button
        onClick={() => setShowManual(!showManual)}
        className="text-sm text-gray-500 underline decoration-gray-700 hover:text-gray-300"
      >
        {showManual ? "Hide manual upload" : "Or upload/paste cookie JSON manually"}
      </button>

      {showManual && (
        <div className="w-full max-w-2xl space-y-4">
          <input
            ref={fileRef}
            type="file"
            accept=".json"
            onChange={handleFile}
            className="hidden"
          />
          <button
            onClick={() => fileRef.current?.click()}
            disabled={isLoading}
            className="w-full cursor-pointer rounded-lg border-2 border-dashed border-gray-700 px-6 py-8 text-center transition hover:border-gray-500 hover:bg-gray-900 disabled:opacity-50"
          >
            <span className="block text-gray-300">
              Drop or click to upload cookies.json
            </span>
            <span className="mt-1 block text-xs text-gray-500">
              JSON exports from Cookie-Editor, EditThisCookie, etc.
            </span>
          </button>

          <div className="flex items-center gap-4">
            <div className="h-px flex-1 bg-gray-800" />
            <span className="text-xs text-gray-600">or paste JSON</span>
            <div className="h-px flex-1 bg-gray-800" />
          </div>

          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder='[{"name": "_ga", "value": "...", "domain": ".example.com", ...}]'
            rows={5}
            className="w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-3 font-mono text-sm text-gray-200 placeholder-gray-600 focus:border-gray-500 focus:outline-none"
          />
          <button
            onClick={handlePaste}
            disabled={isLoading || !text.trim()}
            className="rounded bg-white px-4 py-2 text-sm font-medium text-gray-900 hover:bg-gray-200 disabled:opacity-40"
          >
            {isLoading ? "Analyzing..." : "Analyze"}
          </button>
        </div>
      )}
    </div>
  );
}
