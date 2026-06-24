# CodeLens

GitHub PR이 올라오면 AI(Claude)가 자동으로 코드 품질, 버그 가능성, 리팩토링 포인트를 분석해 PR 코멘트로 남겨주는 서비스입니다. 1인 포트폴리오 프로젝트로, 백엔드/프론트엔드 스택을 학습하면서 만들고 있습니다.

## 기술 스택

**백엔드:** FastAPI, SQLAlchemy 2.x (async), PostgreSQL, Alembic, Celery + Redis, httpx, PyJWT
**프론트엔드:** Next.js 14 (App Router), TypeScript, TailwindCSS
**AI:** Anthropic Claude API
**인프라:** Docker Compose(로컬), Railway/Render(백엔드 배포 예정), Vercel(프론트 배포 예정)

## 진행 상황

- [x] 프로젝트 스캐폴딩 (FastAPI + Next.js + Docker Compose)
- [x] DB 연결 및 `User` 모델 (SQLAlchemy + Alembic)
- [x] GitHub OAuth 로그인 (`/auth/github`, `/auth/callback`)
- [ ] 인증 미들웨어 (`Depends(get_current_user)`)
- [ ] GitHub Webhook 수신 및 서명 검증
- [ ] Celery 기반 비동기 작업 큐
- [ ] PR diff 파싱 + Claude API 코드 리뷰 생성
- [ ] GitHub PR 코멘트 자동 등록
- [ ] 리뷰 히스토리 대시보드
- [ ] 배포 (Railway/Render + Vercel)

## 로컬 실행

### 1. 인프라 (PostgreSQL + Redis)

```bash
docker compose up -d
```

### 2. 백엔드

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, JWT_SECRET 채우기
alembic upgrade head
uvicorn main:app --reload --port 8000
```

GitHub OAuth App 등록 시 Authorization callback URL은 `http://localhost:8000/auth/callback`로 설정해야 합니다.

### 3. 프론트엔드

```bash
cd frontend
npm install
npm run dev   # http://localhost:3000
```

## 프로젝트 구조

```
CodeLens/
├── backend/
│   ├── app/
│   │   ├── routers/      # auth.py, webhook.py 등 기능별 라우터
│   │   ├── models/       # SQLAlchemy 모델
│   │   ├── core/         # config, DB 연결
│   │   └── services/     # 비즈니스 로직
│   ├── alembic/          # DB 마이그레이션
│   └── main.py
├── frontend/
│   └── app/               # Next.js App Router
└── docker-compose.yml
```

자세한 아키텍처/설계 결정은 [CLAUDE.md](./CLAUDE.md)에 정리되어 있습니다.

<!-- webhook 테스트용 -->
