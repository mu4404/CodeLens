import { apiFetch } from "@/lib/api";
import { formatRelativeTime } from "@/lib/format";

import Link from "next/link";

interface Review {
  id: number;
  repo_full_name: string;
  pr_number: number;
  title: string;
  author: string;
  summary: string;
  created_at: string;
  critical_count: number;
  warning_count: number;
  info_count: number;
}

const badgeStyles = {
  critical: "bg-crit-soft text-crit border-crit-border",
  warning: "bg-warn-soft text-warn border-warn-border",
  info: "bg-info-soft text-info border-info-border",
};

export default async function DashboardPage() {
  const reviews: Review[] = await apiFetch("/reviews");

  return (
    <div className="max-w-[1080px] mx-auto px-8 py-10">
      <h2 className="text-[27px] font-bold tracking-tight mb-6">
        리뷰 대시보드
      </h2>
      <div className="bg-surface border border-border rounded-2xl shadow overflow-hidden">
        {reviews.map((review) => (
          <Link
            key={review.id}
            href={`/dashboard/${review.id}`}
            className="block px-5 py-4 border-b border-border hover:bg-surface-2"
          >
            <div className="font-mono text-xs text-muted mb-1">
              {review.repo_full_name} #{review.pr_number}
            </div>
            <div className="text-[15px] font-semibold mb-2">{review.title}</div>
            <div className="flex items-center gap-3">
              <span className="text-sm text-muted">{review.author}</span>
              <span className="text-sm text-muted-2">
                · {formatRelativeTime(review.created_at)}
              </span>
              <div className="flex gap-1.5 ml-auto">
                {review.critical_count > 0 && (
                  <span
                    className={`font-mono text-xs font-semibold px-2 py-0.5 rounded border ${badgeStyles.critical}`}
                  >
                    {review.critical_count}
                  </span>
                )}
                {review.warning_count > 0 && (
                  <span
                    className={`font-mono text-xs font-semibold px-2 py-0.5 rounded border ${badgeStyles.warning}`}
                  >
                    {review.warning_count}
                  </span>
                )}
                {review.info_count > 0 && (
                  <span
                    className={`font-mono text-xs font-semibold px-2 py-0.5 rounded border ${badgeStyles.info}`}
                  >
                    {review.info_count}
                  </span>
                )}
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
