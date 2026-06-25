import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export async function apiFetch(path: string) {
  const token = cookies().get("access_token")?.value;

  const response = await fetch(`http://localhost:8000${path}`, {
    headers: { Cookie: `access_token=${token}` },
    cache: "no-store",
  });

  if (response.status === 401) {
    redirect("/");
  }

  if (!response.ok) {
    throw new Error(`API 요청 실패: ${path}`);
  }

  return response.json();
}
