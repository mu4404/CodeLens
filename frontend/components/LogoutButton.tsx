"use client";

import { useRouter } from "next/navigation";

export default function LogoutButton() {
  const router = useRouter();

  async function logout() {
    await fetch("/api/logout", { method: "POST", credentials: "include" });
    router.push("/");
    router.refresh();
  }

  return (
    <button
      onClick={logout}
      className="text-sm text-muted-2 hover:text-foreground transition-colors"
    >
      로그아웃
    </button>
  );
}
