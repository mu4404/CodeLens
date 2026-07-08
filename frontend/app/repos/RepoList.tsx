"use client";

import { useState } from "react";

interface Repo {
  full_name: string;
  name: string;
  owner: string;
  private: boolean;
  description: string | null;
  language: string | null;
  updated_at: string;
  connected: boolean;
}

export default function RepoList({ initialRepos }: { initialRepos: Repo[] }) {
  const [repos, setRepos] = useState(initialRepos);
  const [loading, setLoading] = useState<string | null>(null);

  async function toggle(repo: Repo) {
    setLoading(repo.full_name);
    const method = repo.connected ? "DELETE" : "POST";
    const url = repo.connected ? "/api/repos/disconnect" : "/api/repos/connect";

    const res = await fetch(url, {
      method,
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repo_full_name: repo.full_name }),
    });

    if (res.ok) {
      setRepos((prev) =>
        prev.map((r) =>
          r.full_name === repo.full_name
            ? { ...r, connected: !r.connected }
            : r,
        ),
      );
    }
    setLoading(null);
  }

  return (
    <div className="bg-surface border border-border rounded-2xl shadow overflow-hidden">
      {repos.map((repo) => (
        <div
          key={repo.full_name}
          className="flex items-center justify-between gap-4 px-5 py-4 border-b border-border"
        >
          <div className="min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-[14.5px] font-semibold">
                <span className="text-muted font-normal">{repo.owner}/</span>
                {repo.name}
              </span>
              <span className="text-xs font-semibold text-muted border border-border rounded-full px-2 py-0.5">
                {repo.private ? "Private" : "Public"}
              </span>
            </div>
            {repo.description && (
              <div className="text-sm text-muted truncate">
                {repo.description}
              </div>
            )}
            <div className="text-xs text-muted-2 mt-0.5">
              {repo.language ?? "Unknown"} ·{" "}
              {new Date(repo.updated_at).toLocaleDateString("ko-KR")} 업데이트
            </div>
          </div>
          <button
            onClick={() => toggle(repo)}
            disabled={loading === repo.full_name}
            className={`shrink-0 px-4 py-1.5 rounded-lg text-sm font-semibold border transition-colors ${
              repo.connected
                ? "bg-accent-soft text-accent border-accent-border"
                : "bg-surface text-foreground border-border hover:bg-surface-2"
            }`}
          >
            {loading === repo.full_name
              ? "…"
              : repo.connected
                ? "연동됨"
                : "연동하기"}
          </button>
        </div>
      ))}
    </div>
  );
}
