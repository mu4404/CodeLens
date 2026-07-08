import { apiFetch } from "@/lib/api";
import RepoList from "./RepoList";

export default async function ReposPage() {
  const repos = await apiFetch("/repos");

  return (
    <div className="max-w-[840px] mx-auto px-8 py-10">
      <h2 className="text-[27px] font-bold tracking-tight mb-2">저장소 연동</h2>
      <p className="text-[15px] text-muted mb-6">
        연동한 저장소의 PR에만 CodeLens가 동작합니다.
      </p>
      <RepoList initialRepos={repos} />
    </div>
  );
}
