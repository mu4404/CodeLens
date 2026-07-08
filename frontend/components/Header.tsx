import { cookies } from "next/headers";
import Link from "next/link";
import LogoutButton from "./LogoutButton";

function getLogin(token: string): string | null {
  try {
    const payload = JSON.parse(
      atob(token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/")),
    );
    return payload.login ?? null;
  } catch {
    return null;
  }
}

export default function Header() {
  const token = cookies().get("access_token")?.value;
  if (!token) return null;

  const login = getLogin(token);

  return (
    <header className="sticky top-0 z-20 flex items-center gap-6 px-6 py-3 bg-[#15181d] border-b border-white/[0.07]">
      <Link href="/dashboard" className="flex items-center gap-2">
        <div className="w-6 h-6 rounded-lg bg-accent flex items-center justify-center">
          <div className="w-2.5 h-2.5 rounded-full border-[2.5px] border-white" />
        </div>
        <span className="font-mono text-[15px] font-semibold text-white tracking-tight">
          CodeLens
        </span>
      </Link>

      <nav className="flex gap-1">
        <Link
          href="/dashboard"
          className="px-3 py-1.5 rounded-lg text-sm font-medium text-white/60 hover:text-white hover:bg-white/10 transition-colors"
        >
          리뷰 대시보드
        </Link>
        <Link
          href="/repos"
          className="px-3 py-1.5 rounded-lg text-sm font-medium text-white/60 hover:text-white hover:bg-white/10 transition-colors"
        >
          저장소 연동
        </Link>
      </nav>

      <div className="flex-1" />

      {login && (
        <span className="text-sm text-white/50 font-mono">{login}</span>
      )}
      <LogoutButton />
    </header>
  );
}
