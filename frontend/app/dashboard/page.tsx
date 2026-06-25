import { apiFetch } from "@/lib/api";

interface Review {
  id: number;
  repo_full_name: string;
  pr_number: number;
  summary: string;
  created_at: string;
}

export default async function DashboardPage() {
  const reviews: Review[] = await apiFetch("/reviews");

  return (
    <div className="max-w-[1080px] mx-auto px-8 py-10">
      <h2 className="text-[27px] font-bold tracking-tight mb-6">
        리뷰 대시보드
      </h2>
      <div className="bg-surface border border-border rounded-2xl shadow overflow-hidden">
        {reviews.map((review) => (
          <div key={review.id} className="px-5 py-4 border-b border-border">
            <div className="font-mono text-xs text-muted mb-1">
              {review.repo_full_name} #{review.pr_number}
            </div>
            <div className="text-[15px] font-semibold">{review.summary}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
