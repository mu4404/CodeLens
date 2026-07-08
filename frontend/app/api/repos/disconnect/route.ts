import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";

export async function DELETE(req: NextRequest) {
  const token = cookies().get("access_token")?.value;
  const body = await req.json();

  const res = await fetch("http://localhost:8000/repos/disconnect", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      Cookie: `access_token=${token}`,
    },
    body: JSON.stringify(body),
  });

  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
