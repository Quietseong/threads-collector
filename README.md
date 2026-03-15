# Link Collector

흩어진 정보를 한곳에 모아 자동으로 분류하는 개인 지식 수집기.

Telegram에 링크를 보내면 AI가 자동으로 내용을 추출하고, 카테고리를 분류하여, Obsidian에 정리된 마크다운 노트로 저장합니다.

## 왜 만들었나

SNS, 블로그, 뉴스 등 여러 플랫폼에서 좋은 글을 발견해도 각 플랫폼의 "저장" 기능에 흩어져 나중에 찾기 어렵습니다. 이 도구는 **하나의 채널(Telegram)로 수집하고, 하나의 공간(Obsidian)에 분류하여 저장**합니다.

## 동작 구조

```
어디서든 좋은 글 발견 → 공유하기 → Telegram 봇에 링크 보내기
                                        │
                                        ▼ (즉시)
                              Vercel Serverless Function
                              ├── 링크에서 콘텐츠 추출 (OG 메타태그)
                              ├── GPT-4o-mini로 카테고리 분류 + 요약
                              ├── GitHub repo에 마크다운 커밋
                              └── Telegram에 분류 결과 답장
                                        │
                                        ▼ (Obsidian 앱 열 때)
                              Obsidian Git 플러그인 (auto-pull)
                              └── GitHub → Obsidian vault 동기화
                                        │
                                        ▼ (자동)
                              Obsidian Sync → 다른 기기 반영
```

## 지원 플랫폼

링크면 다 됩니다. OG 메타태그가 있는 모든 웹페이지를 지원합니다.

| 플랫폼 | 자동 감지 |
|--------|----------|
| Threads | ✅ |
| X (Twitter) | ✅ |
| YouTube | ✅ |
| Medium | ✅ |
| Velog / Brunch / Tistory | ✅ |
| 네이버 블로그 / 뉴스 | ✅ |
| GitHub | ✅ |
| Reddit / Hacker News | ✅ |
| 기타 모든 URL | ✅ |

## 카테고리

GPT-4o-mini가 아래 8개 대분류 중 하나로 자동 분류하고, 소분류와 태그를 자동 생성합니다.

| 대분류 | 폴더명 |
|--------|--------|
| 개발/기술 | `tech/` |
| 디자인 | `design/` |
| 커리어 | `career/` |
| 뉴스/트렌드 | `news/` |
| 인사이트 | `insights/` |
| 도구/리소스 | `tools/` |
| 일상/유머 | `lifestyle/` |
| 기타 | `misc/` |

## 설치 방법

### 사전 준비

- [Telegram](https://telegram.org/) 계정
- [GitHub](https://github.com/) 계정
- [Vercel](https://vercel.com/) 계정 (GitHub으로 로그인)
- [OpenAI API Key](https://platform.openai.com/api-keys)
- (선택) [Obsidian](https://obsidian.md/) + Obsidian Sync + Obsidian Git 플러그인

### 1. Telegram Bot 생성

1. Telegram에서 [@BotFather](https://t.me/BotFather)에게 `/newbot` 전송
2. 봇 이름과 username 설정 (`_bot`으로 끝나야 함)
3. 발급된 **Bot Token** 저장
4. 생성된 봇에게 아무 메시지 전송 (예: `/start`)
5. `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates` 에서 **Chat ID** 확인

### 2. GitHub 설정

1. 이 repo를 Fork하거나, 새 repo 생성 후 코드 복사
2. [Personal Access Token](https://github.com/settings/tokens/new) 생성 (Classic, `repo` 스코프 체크)

### 3. Vercel 배포

1. [Vercel](https://vercel.com/new)에서 GitHub repo Import
2. Framework Preset: **Other** 선택
3. Deploy 완료 후, **Settings → Environment Variables**에 추가:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | OpenAI API 키 |
| `TELEGRAM_BOT_TOKEN` | BotFather에서 받은 토큰 |
| `GITHUB_TOKEN` | GitHub Personal Access Token |
| `GITHUB_REPO` | `username/repo-name` |

4. 환경변수 추가 후 **Redeploy**

### 4. Telegram Webhook 등록

배포 완료 후 아래 URL을 브라우저에서 열기:

```
https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://<your-app>.vercel.app/api/webhook
```

`{"ok":true}` 응답이 오면 성공.

### 5. Obsidian 동기화 (선택)

이 레포를 Obsidian 보관함으로 직접 사용합니다. `.obsidianignore` 파일이 포함되어 있어 코드 파일(`api/`, `vercel.json` 등)은 Obsidian에서 자동으로 숨겨집니다.

#### 초기 설정

1. 이 레포를 clone합니다:
   ```bash
   git clone https://github.com/<username>/<repo-name>.git "<원하는 경로>"
   ```

2. Obsidian에서 **보관함 열기** → clone한 폴더 선택

3. **Obsidian Git 플러그인** 설치:
   - 설정 → 커뮤니티 플러그인 → 탐색 → "Obsidian Git" 검색 → 설치
   - 플러그인 설정에서:
     - **Auto pull on open**: `true` (앱 열 때 자동으로 새 노트 가져오기)
     - **Pull interval**: `5` (5분마다 자동 pull)
     - **Disable push**: `true` (이 보관함은 읽기 전용, push 불필요)

4. (Obsidian Sync 사용 시) Sync 설정에서 **제외 폴더**에 `.git` 추가

#### 동기화 흐름

```
텔레그램으로 링크 전송 → GitHub에 자동 저장 (즉시)
        ↓
Obsidian 앱 열기 → Git 플러그인이 auto-pull → 새 노트 반영
        ↓
Obsidian Sync → 다른 기기에 자동 전파 (모바일 포함)
```

PC, 모바일 어디서든 Obsidian을 열기만 하면 새 노트가 동기화됩니다.

## 알려진 제한사항

**Obsidian을 열어야 동기화됩니다.**

Telegram으로 링크를 보내면 수집, 분류, GitHub 저장, Telegram 답장은 **24시간 즉시 동작**합니다 (Vercel 서버리스). Obsidian에 반영하려면 아무 기기에서 Obsidian 앱을 열면 됩니다 (Git 플러그인이 auto-pull).

- 수집된 노트는 **유실되지 않습니다** (GitHub에 안전하게 보관)
- Obsidian을 열면 밀린 노트가 **한꺼번에 동기화**됩니다
- Obsidian Sync가 있으면 한 기기에서 pull한 노트가 **다른 기기에 자동 전파**됩니다
- Telegram에서 분류 결과는 즉시 확인할 수 있습니다

## 비용

| 항목 | 비용 |
|------|------|
| Vercel | 무료 (Hobby) |
| Telegram Bot | 무료 |
| GitHub repo | 무료 |
| OpenAI API (GPT-4o-mini) | ~$0.28/월 (일 30건 기준) |
| **합계** | **월 ~$0.28** |

## 프로젝트 구조

```
├── api/
│   └── webhook.py          # Vercel 서버리스 함수 (핵심 로직 전부)
├── obsidian-vault/
│   └── threads-archive/    # 수집된 마크다운 노트 (카테고리별 폴더)
│       └── _dashboard.md   # Obsidian Dataview 대시보드
├── .obsidianignore          # Obsidian에서 코드 파일 숨김
├── vercel.json             # Vercel 배포 설정
└── requirements.txt        # Python 의존성
```

## 사용법

링크를 Telegram 봇에 보내면 끝입니다.

모바일에서는 "공유하기 → Telegram" 으로 더 빠르게 보낼 수 있습니다.
