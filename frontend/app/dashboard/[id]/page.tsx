import { apiFetch } from "@/lib/api";
import { formatRelativeTime } from "@/lib/format";

interface ReviewIssue {
  id: number;
  file: string;
  severity: "critical" | "warning" | "info";
  title: string;
  description: string;
  suggestion: string;
}

interface ReviewDetail {
  id: number;
  repo_full_name: string;
  pr_number: number;
  title: string;
  author: string;
  summary: string;
  created_at: string;
  issues: ReviewIssue[];
}

const severityStyles: Record<string, string> = {
  critical: "bg-crit-soft text-crit border-crit-border",
  warning: "bg-warn-soft text-warn border-warn-border",
  info: "bg-info-soft text-info border-info-border",
};

const severityLabels: Record<string, string> = {
  critical: "Critical",
  warning: "Warning",
  info: "Info",
};

export default async function ReviewDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const review: ReviewDetail = await apiFetch(`/reviews/${params.id}`);

  const issuesByFile = new Map<string, ReviewIssue[]>();
  for (const issue of review.issues) {
    const list = issuesByFile.get(issue.file) ?? [];
    list.push(issue);
    issuesByFile.set(issue.file, list);
  }

  return (
    <div className="max-w-[980px] mx-auto px-8 py-8">
      <div className="font-mono text-xs text-muted mb-2">
        {review.repo_full_name} #{review.pr_number}
      </div>
      <h2 className="text-[27px] font-bold tracking-tight mb-6">
        {review.title}
      </h2>
      <div className="text-sm text-muted mb-6">
        {review.author} · {formatRelativeTime(review.created_at)}
      </div>
      <p className="text-[15px] text-muted mb-8">{review.summary}</p>
      {Array.from(issuesByFile.entries()).map(([file, issues]) => (
        <div
          key={file}
          className="bg-surface border border-border rounded-2xl shadow mb-5 overflow-hidden"
        >
          <div className="px-5 py-3 bg-surface-2 border-b border-border font-mono text-sm font-semibold">
            {file}
          </div>
          <div className="px-5">
            {issues.map((issue) => (
              <div
                key={issue.id}
                className="py-4 border-t border-border first:border-t-0"
              >
                <span
                  className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-bold border ${severityStyles[issue.severity]}`}
                >
                  {severityLabels[issue.severity]}
                </span>
                <div className="text-[14.5px] font-semibold mt-2 mb-1">
                  {issue.title}
                </div>
                <div className="text-[13.5px] text-muted mb-2">
                  {issue.description}
                </div>
                <div className="font-mono text-xs bg-surface-2 border border-border rounded-lg p-3 whitespace-pre-wrap">
                  {issue.suggestion}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
