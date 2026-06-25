당신은 시니어 풀스택 개발자이자 기술 아키텍트입니다.

모든 개발 관련 요청에 대해 다음 원칙으로 응답하세요.

1. 사용 언어/프레임워크는 코드에서 자동 감지하거나, 명시되지 않으면 먼저 질문하세요.
2. 요청의 성격을 파악해 아래 중 해당하는 항목만 다루세요.
   - 아이디어 구상: 접근 방법 2~3가지를 비교하고 상황별 추천 제시
   - 코드 리뷰: 버그, 보안, 성능, 스타일 순으로 점검
   - 디버깅: 에러 원인을 단계적으로 분석하고 수정 코드 제공
   - 리팩터링: 기능 변경 없이 가독성과 구조 개선
   - 성능 최적화: 병목 지점을 설명하고 개선된 코드 제공
   - 보안 감사: SQL 인젝션, XSS, 인증 이슈 등 취약점 점검
   - 테스트 코드: 해피패스, 엣지케이스, 에러 케이스 포함
   - 문서화: 파라미터, 반환값, 예시, 예외 상황 포함
   - 설계/아키텍처: API, DB 스키마, 시스템 구조 설계
   - 코드 구현: 실제 동작 가능한 코드로 제공
3. 수정/개선 사항은 변경 이유를 간략히 설명하세요.
4. 추가로 주의할 사항이 있으면 마지막에 한 줄로 언급하세요.

# CLAUDE.md — AI Code Review Service

> 이 파일은 Claude가 프로젝트 컨텍스트를 빠르게 파악하기 위한 문서입니다.
> 새 대화를 시작할 때 이 파일을 먼저 읽어주세요.

---

## 프로젝트 개요

**서비스명:** AI Code Review  
**목적:** GitHub PR이 올라오면 AI가 자동으로 코드 품질, 버그 가능성, 리팩토링 포인트를 분석해 PR 코멘트로 남겨주는 서비스  
**개발 형태:** 1인 개발, 포트폴리오 목적

### 핵심 기능

- GitHub Webhook으로 PR 이벤트 수신
- PR diff를 LLM에 전달해 코드 리뷰 생성
- 심각도 분류 (Critical / Warning / Info) + 파일별 요약 + 개선 코드 스니펫 제안
- GitHub PR에 자동 코멘트 등록
- 리뷰 히스토리 및 통계 대시보드

---

## 기술 스택

### 백엔드

| 역할            | 기술       | 버전 |
| --------------- | ---------- | ---- |
| API 서버        | FastAPI    | 최신 |
| 비동기 작업 큐  | Celery     | 최신 |
| 큐 브로커       | Redis      | 7.x  |
| ORM             | SQLAlchemy | 2.x  |
| DB              | PostgreSQL | 16.x |
| HTTP 클라이언트 | httpx      | 최신 |
| JWT             | PyJWT      | 최신 |

### 프론트엔드

| 역할        | 기술                    |
| ----------- | ----------------------- |
| 프레임워크  | Next.js 14 (App Router) |
| 언어        | TypeScript              |
| 스타일링    | TailwindCSS             |
| UI 컴포넌트 | shadcn/ui               |

### AI / 외부 연동

| 역할        | 기술                                                        |
| ----------- | ----------------------------------------------------------- |
| LLM         | OpenAI API (1차 구현) — `LLM_PROVIDER` env로 전환 가능한 provider 추상화. Claude API는 추후 두 번째 provider로 추가 예정 |
| GitHub 연동 | GitHub REST API v3                                           |
| 인증        | GitHub OAuth 2.0                                              |

### 인프라

| 역할            | 기술                |
| --------------- | ------------------- |
| 로컬 개발 환경  | Docker Compose      |
| 백엔드 배포     | Railway 또는 Render |
| 프론트엔드 배포 | Vercel              |

---

## 프로젝트 구조

```
ai-code-review/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── auth.py        # GitHub OAuth 인증
│   │   │   └── webhook.py     # GitHub Webhook 수신
│   │   ├── dependencies/
│   │   │   └── auth.py        # JWT 인증 미들웨어 (Depends)
│   │   ├── models/
│   │   │   └── user.py        # SQLAlchemy 모델
│   │   ├── services/          # 비즈니스 로직
│   │   └── core/
│   │       └── config.py      # 환경변수 관리 (pydantic-settings)
│   ├── main.py                # FastAPI 앱 엔트리포인트
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/
│   │   ├── page.tsx           # 랜딩 / 로그인
│   │   ├── dashboard/
│   │   │   └── page.tsx       # 리뷰 히스토리 대시보드
│   │   └── api/
│   │       └── logout/
│   │           └── route.ts   # 로그아웃 API Route
│   ├── components/
│   └── lib/
├── docker-compose.yml
├── .gitignore
└── CLAUDE.md                  # 이 파일
```

---

## 아키텍처 흐름

```
GitHub PR 오픈
    ↓
Webhook → FastAPI (수신 + 서명 검증)
    ↓
Celery + Redis (비동기 큐에 작업 등록)
    ↓
Worker (PR diff 파싱 → LLM API 호출, provider는 LLM_PROVIDER로 전환)
    ↓
GitHub REST API (PR에 코멘트 등록)
    ↓
PostgreSQL (리뷰 결과 저장)
    ↓
Next.js Dashboard (히스토리 / 통계 조회)
```

---

## GitHub OAuth 인증 설계

### 흐름 요약

1. 프론트 → `GET /auth/github` → GitHub 인증 페이지로 302 리다이렉트
2. GitHub → `GET /auth/callback?code=xxx&state=yyy` 로 콜백
3. 백엔드 → code로 `access_token` 교환 (GitHub API)
4. 백엔드 → `access_token`으로 유저 정보 조회
5. 백엔드 → JWT 발급 후 **HttpOnly 쿠키**로 전달
6. 프론트 → 쿠키 자동 전송으로 인증 유지

### 보안 결정 사항

| 항목           | 결정                                     | 이유                         |
| -------------- | ---------------------------------------- | ---------------------------- |
| CSRF 방지      | `state` 파라미터 검증                    | code 탈취 공격 차단          |
| XSS 방지       | `httponly=True` 쿠키                     | JS에서 토큰 접근 불가        |
| 토큰 보관      | `access_token`을 JWT payload 내부에 포함 | 클라이언트에 직접 노출 안 됨 |
| OAuth 스코프   | `read:user user:email repo`              | 필요한 권한만 최소 요청      |
| 운영 환경 쿠키 | `secure=True`, `samesite="lax"`          | HTTPS 전용, CSRF 완화        |

### 인증 미들웨어 사용법

```python
# 보호된 라우트에 Depends로 주입
from app.dependencies.auth import get_current_user
from fastapi import Depends

@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    return {"login": user["login"]}
```

### state 저장소

- **현재:** 메모리 `set` (개발용)
- **운영 전 교체 필수:** Redis (`setex`로 TTL 10분 설정)

---

## 환경변수 목록

```env
# GitHub OAuth
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

# JWT
JWT_SECRET=                  # 충분히 길고 랜덤한 값 사용

# DB
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/ai_code_review

# Redis
REDIS_URL=redis://localhost:6379

# LLM Provider 선택 (openai | claude)
LLM_PROVIDER=openai

# OpenAI
OPENAI_API_KEY=

# Anthropic (LLM_PROVIDER=claude일 때 사용, 추후 구현)
ANTHROPIC_API_KEY=

# 서비스
FRONTEND_URL=http://localhost:3000
```

---

## 코드 컨벤션

### 공통

- 언어: **한국어 주석 허용**, 변수/함수명은 **영어 snake_case**
- 환경변수는 반드시 `core/config.py`의 pydantic-settings로 관리 (직접 `os.getenv` 지양)
- 시크릿 값은 절대 코드에 하드코딩 금지

### FastAPI (백엔드)

- 라우터는 기능 단위로 분리 (`routers/auth.py`, `routers/webhook.py` 등)
- 비즈니스 로직은 `services/` 레이어로 분리 (라우터에 직접 작성 금지)
- 인증이 필요한 모든 엔드포인트는 `Depends(get_current_user)` 사용
- DB 쿼리는 SQLAlchemy async 세션 사용
- 에러 응답은 `HTTPException` 사용, 메시지는 한국어로

### Next.js (프론트엔드)

- App Router 사용 (Pages Router 사용 금지)
- 서버 컴포넌트 기본, 클라이언트 컴포넌트는 `"use client"` 명시
- API 호출 시 반드시 `credentials: "include"` (쿠키 전송)
- 타입은 모두 TypeScript로 명시 (`any` 사용 금지)

---

## 아직 결정되지 않은 사항 (TODO)

- [x] DB 스키마 설계 — `users`, `reviews`, `review_issues` 완료. `repositories` 테이블은 1.2(저장소 연동) 구현 시 추가 필요
- [ ] GitHub Webhook 수신 및 서명 검증 (`X-Hub-Signature-256`)
- [ ] PR diff 파싱 로직
- [ ] LLM 프롬프트 설계 (심각도 분류 기준 포함, provider 공통 사용 가능하도록)
- [ ] Celery Worker 구조
- [ ] 리뷰 결과 심각도 분류 스펙 (Critical / Warning / Info 기준 정의)
- [ ] 대시보드 UI 설계
- [ ] 운영 배포 파이프라인 (CI/CD)
- [ ] state 저장소 Redis 교체

---

## 개발 시작 순서 (권장)

1. `docker-compose up` — PostgreSQL + Redis 로컬 실행
2. `backend/` — FastAPI 서버 실행 (`uvicorn main:app --reload`)
3. `frontend/` — Next.js 개발 서버 실행 (`npm run dev`)
4. GitHub OAuth 앱 등록 후 `.env` 작성
5. `/auth/github` 접속해서 OAuth 로그인 동작 확인
6. Webhook 엔드포인트 구현 → ngrok으로 로컬 테스트

---

_마지막 업데이트: 2026-06-24_
