import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export default function LandingPage() {
  const token = cookies().get("access_token");
  if (token) redirect("/dashboard");

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-8">
      <div className="max-w-[480px] w-full text-center">
        <div className="inline-flex items-center gap-2 mb-8">
          <div className="w-8 h-8 rounded-lg bg-accent flex items-center justify-center">
            <div className="w-3 h-3 rounded-full border-[2.5px] border-white" />
          </div>
          <span className="font-mono text-lg font-semibold tracking-tight">
            CodeLens
          </span>
        </div>

        <h1 className="text-[42px] font-bold leading-tight tracking-tight mb-4">
          PR을 열면,
          <br />
          AI가 코드를
          <br />
          먼저 읽습니다
        </h1>
        <p className="text-[16px] text-muted leading-relaxed mb-10">
          GitHub Pull Request가 올라오면 AI가 자동으로 코드 품질·잠재
          버그·리팩토링 포인트를 분석해 PR 코멘트로 남깁니다.
        </p>

        <div className="flex flex-col gap-3">
          <a
            href="http://localhost:8000/auth/github"
            className="flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-[#1c2128] border border-[#2d333b] text-white text-[15px] font-semibold hover:bg-[#22272e] transition-colors"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
            </svg>
            GitHub로 계속하기
          </a>
          <a
            href="/dashboard"
            className="px-6 py-3 rounded-xl border border-border text-[15px] font-semibold text-muted hover:bg-surface-2 transition-colors"
          >
            대시보드 둘러보기 →
          </a>
        </div>
      </div>
    </div>
  );
}
