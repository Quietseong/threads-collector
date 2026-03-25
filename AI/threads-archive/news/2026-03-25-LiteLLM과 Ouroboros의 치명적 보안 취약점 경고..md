---
title: "LiteLLM과 Ouroboros의 치명적 보안 취약점 경고."
source: threads
author: "@feelfree_ai"
category: "뉴스/트렌드"
subcategory: "사이버 보안"
tags: ["LiteLLM", "Ouroboros", "API키", "악성코드", "사이버공격"]
confidence: 0.9
original_url: "https://www.threads.com/@feelfree_ai/post/DWSzE23gCGQ"
collected_at: "2026-03-25T13:19:51.759090Z"
classified_at: "2026-03-25T13:19:55.828642Z"
---

# LiteLLM과 Ouroboros의 치명적 보안 취약점 경고.

> **출처**: threads @feelfree_ai (Threads)
> **카테고리**: 뉴스/트렌드 > 사이버 보안

## 원문

feelfree_ai

🚨 3월 23일 이후 LiteLLM이나 Ouroboros 설치하신 분들, 지금 당장 API 키부터 전부 폐기하세요. 
치명적인 공급망 공격이 터졌습니다.

단순 import가 아니라 Python을 켤 때마다 몰래 작동해서, 내 PC의 API 키, SSH, 클라우드 권한을 싹 다 외부로 빼돌립니다.

가장 중요한 건, 앱을 업데이트해도 악성 파일은 안 날아갑니다. 내 손으로 직접 걷어내야 해요.

1️⃣ 악성 파일 직접 삭제 (터미널에 find / -name "litellm_init.pth" 치고 나오면 즉시 삭제)
2️⃣ 패키지/캐시 비우기 (pip uninstall litellm 및 캐시 정리)
3️⃣ 크레덴셜 전면 교체 (기간 내 PC에 있던 모든 API 키, 클라우드 토큰 무조건 재발급)

Ouroboros는 문제의 의존성을 완전히 뺐으니, 
위 3단계 조치를 꼭 끝내시고 최신 버전으로 업데이트하세요.

2차 피해 막게 주변 개발자분들께도 빨리 알려주세요.

---
[원본 보기](https://www.threads.com/@feelfree_ai/post/DWSzE23gCGQ)
