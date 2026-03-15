"""
Vercel Serverless Function: Telegram Webhook Handler
Threads 링크를 받으면 즉시 분류 → Obsidian(GitHub) 저장 → 답장
"""

import json
import os
import re
import html
import urllib.request
import base64
from datetime import datetime
from http.server import BaseHTTPRequestHandler

# ── 설정 ──────────────────────────────────────────────
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "")  # "username/threads-collector"

CATEGORIES = [
    "개발/기술", "디자인", "커리어", "뉴스/트렌드",
    "인사이트", "도구/리소스", "일상/유머", "기타",
]

CATEGORY_FOLDER_MAP = {
    "개발/기술": "tech", "디자인": "design", "커리어": "career",
    "뉴스/트렌드": "news", "인사이트": "insights",
    "도구/리소스": "tools", "일상/유머": "lifestyle", "기타": "misc",
}

SYSTEM_PROMPT = f"""당신은 소셜 미디어 게시글 분류 전문가입니다.

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


# ── Threads 게시글 추출 ──────────────────────────────
def extract_thread_post(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8", errors="ignore")

    og = {}
    for match in re.finditer(
        r'<meta\s+(?:property|name)="(og|twitter):(\w+)"\s+content="([^"]*?)"', raw
    ):
        key = f"{match.group(1)}:{match.group(2)}"
        og[key] = html.unescape(match.group(3))

    text = og.get("og:description", "") or og.get("twitter:description", "")
    title = og.get("og:title", "") or og.get("twitter:title", "")
    image = og.get("og:image", "") or og.get("twitter:image", "")
    canonical = og.get("og:url", url)

    author_match = re.match(r"(.+?)\s*\(@(\w+)\)\s*on Threads", title)
    author_name = author_match.group(1) if author_match else title
    author_handle = f"@{author_match.group(2)}" if author_match else ""

    post_id_match = re.search(r"/post/([A-Za-z0-9_-]+)", url)
    post_id = post_id_match.group(1) if post_id_match else ""

    return {
        "id": post_id,
        "author": author_handle,
        "authorName": author_name,
        "postUrl": canonical,
        "text": text,
        "image": image,
        "collectedAt": datetime.utcnow().isoformat() + "Z",
    }


# ── LLM 분류 ─────────────────────────────────────────
def classify_post(post):
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"작성자: {post['author']}\n텍스트: {post['text']}"},
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
    slug = re.sub(r"[^\w\s가-힣-]", "", summary)
    slug = re.sub(r"\s+", "-", slug.strip())[:40] or "untitled"
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    filepath = f"obsidian-vault/threads-archive/{folder}/{date_str}-{slug}.md"

    tags_yaml = json.dumps(classification.get("tags", []), ensure_ascii=False)
    content = f"""---
title: "{summary}"
source: threads
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

> **작성자**: {post.get('author', '')} ({post.get('authorName', '')})
> **카테고리**: {category} > {classification.get('subcategory', '')}

## 원문

{post.get('text', '')}

---
[원본 보기]({post.get('postUrl', '')})
"""

    # GitHub Contents API로 파일 생성
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filepath}"
    payload = json.dumps({
        "message": f"collect: {summary}",
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
    }).encode("utf-8")
    req = urllib.request.Request(api_url, data=payload, method="PUT", headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github+json",
    })
    urllib.request.urlopen(req, timeout=15)
    return filepath


# ── URL 파싱 ──────────────────────────────────────────
def extract_threads_url(text):
    patterns = [
        r"https?://(?:www\.)?threads\.(?:net|com)/@[\w.]+/post/[A-Za-z0-9_-]+",
        r"https?://(?:www\.)?threads\.(?:net|com)/t/[A-Za-z0-9_-]+",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None


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
                    "Threads Collector 봇입니다.\n\n"
                    "Threads 게시글 링크를 보내주시면 자동으로 분류하여 Obsidian에 저장합니다."
                )
                return

            url = extract_threads_url(text)
            if not url:
                telegram_reply(chat_id, "Threads 게시글 링크를 보내주세요.\n예: https://threads.net/@user/post/xxx")
                return

            # 처리
            post = extract_thread_post(url)
            if not post["text"]:
                telegram_reply(chat_id, "게시글 내용을 추출할 수 없습니다. (비공개 계정일 수 있습니다)")
                return

            classification = classify_post(post)
            filepath = save_to_github(post, classification)

            cat = classification.get("category", "기타")
            sub = classification.get("subcategory", "")
            summary = classification.get("summary", "")
            tags = " ".join(f"#{t}" for t in classification.get("tags", []))

            telegram_reply(chat_id,
                f"✅ <b>수집 완료!</b>\n\n"
                f"<b>분류</b>: {cat} &gt; {sub}\n"
                f"<b>요약</b>: {summary}\n"
                f"<b>태그</b>: {tags}\n"
                f"<b>저장</b>: {filepath.split('/')[-1]}"
            )

        except Exception as e:
            if chat_id:
                telegram_reply(chat_id, f"오류: {str(e)[:100]}")

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Threads Collector Bot is running.")
