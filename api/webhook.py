"""
Vercel Serverless Function: Telegram Webhook Handler
아무 링크를 받으면 즉시 분류 → Obsidian(GitHub) 저장 → 답장
지원: Threads, 블로그, 뉴스, YouTube, X(Twitter), 카카오 등 모든 URL
"""

import json
import os
import re
import html
import urllib.request
import base64
import hashlib
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

# ── 설정 ──────────────────────────────────────────────
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "")

CATEGORIES = [
    "개발/기술", "디자인", "커리어", "뉴스/트렌드",
    "인사이트", "도구/리소스", "일상/유머", "기타",
]

CATEGORY_FOLDER_MAP = {
    "개발/기술": "tech", "디자인": "design", "커리어": "career",
    "뉴스/트렌드": "news", "인사이트": "insights",
    "도구/리소스": "tools", "일상/유머": "lifestyle", "기타": "misc",
}

# 플랫폼 감지
PLATFORM_MAP = {
    "threads.net": "threads", "threads.com": "threads",
    "x.com": "x", "twitter.com": "x",
    "youtube.com": "youtube", "youtu.be": "youtube",
    "instagram.com": "instagram",
    "brunch.co.kr": "brunch",
    "tistory.com": "tistory",
    "velog.io": "velog",
    "medium.com": "medium",
    "github.com": "github",
    "news.ycombinator.com": "hackernews",
    "reddit.com": "reddit",
    "linkedin.com": "linkedin",
    "naver.me": "naver", "blog.naver.com": "naver", "n.news.naver.com": "naver",
    "v.daum.net": "daum", "news.v.daum.net": "daum",
}

SYSTEM_PROMPT = f"""당신은 웹 콘텐츠 분류 전문가입니다.

## 대분류 (반드시 하나 선택)
{chr(10).join(f'- {c}' for c in CATEGORIES)}

## 응답 규칙
- category: 위 목록 중 하나
- subcategory: 세부 주제 (자유 생성)
- tags: 핵심 키워드 3-5개 (고유명사는 원어 유지)
- summary: 30-50자 한줄 요약 (한국어)
- confidence: 0.0-1.0

JSON으로만 응답하세요."""


# ── Telegram API ──────────────────────────────────────
def telegram_reply(chat_id, text):
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass


# ── 플랫폼 감지 ──────────────────────────────────────
def detect_platform(url):
    hostname = urlparse(url).hostname or ""
    hostname = hostname.removeprefix("www.")
    for domain, platform in PLATFORM_MAP.items():
        if hostname == domain or hostname.endswith("." + domain):
            return platform
    return hostname.split(".")[0] if hostname else "web"


# ── 콘텐츠 추출 (범용 OG 태그) ───────────────────────
def fetch_page(url, retries=2):
    """URL에서 HTML 가져오기 (쿠키 + 브라우저 헤더 + 재시도)"""
    import http.cookiejar
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    ]
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": agents[i % len(agents)],
                "Accept-Language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Upgrade-Insecure-Requests": "1",
            })
            with opener.open(req, timeout=15) as resp:
                return resp.read(500_000).decode("utf-8", errors="ignore")
        except urllib.error.HTTPError as e:
            if e.code == 403 and i < retries:
                continue
            raise
    return ""


def extract_content(url):
    raw = fetch_page(url)

    og = {}
    # 범용 OG/Twitter 메타 태그 파싱 (data-rh 등 추가 속성 허용)
    for match in re.finditer(
        r'<meta\s+[^>]*?(?:property|name)="(og|twitter):(\w+)"[^>]*?content="([^"]*?)"', raw
    ):
        key = f"{match.group(1)}:{match.group(2)}"
        og[key] = html.unescape(match.group(3))
    for match in re.finditer(
        r'<meta\s+[^>]*?content="([^"]*?)"[^>]*?(?:property|name)="(og|twitter):(\w+)"', raw
    ):
        key = f"{match.group(2)}:{match.group(3)}"
        if key not in og:
            og[key] = html.unescape(match.group(1))

    title = og.get("og:title", "") or og.get("twitter:title", "")
    description = og.get("og:description", "") or og.get("twitter:description", "")
    image = og.get("og:image", "") or og.get("twitter:image", "")
    canonical = og.get("og:url", url)
    site_name = og.get("og:site_name", "")

    # OG 태그 없으면 <title> 태그에서 추출
    if not title:
        m = re.search(r"<title[^>]*>([^<]+)</title>", raw)
        title = html.unescape(m.group(1).strip()) if m else ""

    # meta description 폴백
    if not description:
        m = re.search(r'<meta\s+name="description"\s+content="([^"]*?)"', raw)
        description = html.unescape(m.group(1)) if m else ""

    platform = detect_platform(url)

    # 플랫폼별 작성자 추출
    author = ""
    if platform == "threads":
        m = re.match(r"(.+?)\s*\(@(\w+)\)\s*on Threads", title)
        if m:
            author = f"@{m.group(2)}"
            title = m.group(1)
    elif platform == "x":
        m = re.match(r"(.+?)\s*(?:\(@(\w+)\))?\s*(?:on X|/ X)", title)
        if m and m.group(2):
            author = f"@{m.group(2)}"
    elif platform in ("velog", "brunch", "medium"):
        author = site_name or ""

    # 고유 ID 생성
    content_id = hashlib.md5(url.encode()).hexdigest()[:10]

    # 본문 텍스트: description이 짧으면 title도 합침
    text = description
    if title and title not in description:
        text = f"{title}\n\n{description}" if description else title

    return {
        "id": content_id,
        "platform": platform,
        "author": author,
        "title": title,
        "postUrl": canonical,
        "text": text,
        "image": image,
        "siteName": site_name,
        "collectedAt": datetime.utcnow().isoformat() + "Z",
    }


# ── LLM 분류 ─────────────────────────────────────────
def classify_post(post):
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)

    user_msg = f"출처: {post['platform']}\n제목: {post.get('title', '')}\n내용: {post['text']}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.3,
        max_tokens=300,
    )
    return json.loads(response.choices[0].message.content)


# ── GitHub에 마크다운 저장 ────────────────────────────
def save_to_github(post, classification):
    category = classification.get("category", "기타")
    folder = CATEGORY_FOLDER_MAP.get(category, "misc")
    summary = classification.get("summary", "untitled")
    platform = post.get("platform", "web")
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    # 파일명: 날짜-요약제목 (한글 포함, GitHub API용 UTF-8 인코딩)
    slug = re.sub(r"[\\/:*?\"<>|]", "", summary)  # 파일시스템 금지 문자만 제거
    slug = re.sub(r"\s+", " ", slug.strip())[:50] or "untitled"
    filepath = f"AI/threads-archive/{folder}/{date_str}-{slug}.md"

    tags_yaml = json.dumps(classification.get("tags", []), ensure_ascii=False)
    platform = post.get("platform", "web")
    author_line = f"{post.get('author', '')} " if post.get("author") else ""
    site_line = f"({post.get('siteName', '')})" if post.get("siteName") else ""

    content = f"""---
title: "{summary}"
source: {platform}
author: "{post.get('author', '')}"
category: "{category}"
subcategory: "{classification.get('subcategory', '')}"
tags: {tags_yaml}
confidence: {classification.get('confidence', 0)}
original_url: "{post.get('postUrl', '')}"
collected_at: "{post.get('collectedAt', '')}"
classified_at: "{datetime.utcnow().isoformat()}Z"
---

# {summary}

> **출처**: {platform} {author_line}{site_line}
> **카테고리**: {category} > {classification.get('subcategory', '')}

## 원문

{post.get('text', '')}

---
[원본 보기]({post.get('postUrl', '')})
"""

    encoded_path = urllib.parse.quote(filepath, safe="/")
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{encoded_path}"
    commit_msg = f"collect: [{platform}] {summary}"
    payload = json.dumps({
        "message": commit_msg,
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
    }, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(api_url, data=payload, method="PUT", headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github+json",
    })
    urllib.request.urlopen(req, timeout=15)
    return filepath


# ── URL 추출 (범용) ───────────────────────────────────
def extract_url(text):
    match = re.search(r"https?://[^\s<>\"']+", text)
    return match.group(0).rstrip(".,;:)>」】") if match else None


# ── Vercel Handler ────────────────────────────────────
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

        try:
            update = json.loads(body)
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "")

            if not chat_id or not text:
                return

            if text.strip() == "/start":
                telegram_reply(chat_id,
                    "📌 <b>Link Collector 봇</b>\n\n"
                    "아무 링크나 보내주시면 자동으로 분류하여 Obsidian에 저장합니다.\n\n"
                    "<b>지원 플랫폼</b>: Threads, X, YouTube, 블로그, 뉴스, 카카오 등 모든 URL"
                )
                return

            url = extract_url(text)
            if not url:
                telegram_reply(chat_id, "링크를 보내주세요.")
                return

            # 처리
            post = extract_content(url)
            if not post["text"]:
                telegram_reply(chat_id, "콘텐츠를 추출할 수 없습니다. (비공개이거나 지원하지 않는 형식)")
                return

            classification = classify_post(post)
            filepath = save_to_github(post, classification)

            cat = classification.get("category", "기타")
            sub = classification.get("subcategory", "")
            summary = classification.get("summary", "")
            tags = " ".join(f"#{t}" for t in classification.get("tags", []))
            platform = post.get("platform", "web")

            telegram_reply(chat_id,
                f"✅ <b>수집 완료!</b>\n\n"
                f"<b>출처</b>: {platform}\n"
                f"<b>분류</b>: {cat} &gt; {sub}\n"
                f"<b>요약</b>: {summary}\n"
                f"<b>태그</b>: {tags}"
            )

        except Exception as e:
            if chat_id:
                telegram_reply(chat_id, f"오류: {str(e)[:200]}")

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Link Collector Bot is running.")
