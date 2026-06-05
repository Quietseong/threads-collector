---
title: "designlang은 웹사이트 디자인 시스템을 자동으로 추출하는 도구입니다."
source: discuss
author: ""
category: "디자인"
subcategory: "디자인 시스템"
tags: ["designlang", "디자인시스템", "CLI도구", "AI에이전트", "자동화"]
confidence: 0.9
original_url: "https://discuss.pytorch.kr/t/designlang-cli-ai/10494?u=j808esc"
collected_at: "2026-06-05T01:25:42.264462Z"
classified_at: "2026-06-05T01:25:46.746378Z"
---

# designlang은 웹사이트 디자인 시스템을 자동으로 추출하는 도구입니다.

> **출처**: discuss (PyTorchKR)
> **카테고리**: 디자인 > 디자인 시스템

## 원문

designlang: 웹사이트의 디자인 시스템을 한 번에 추출하는 CLI와 AI 에이전트 도구  designlang 소개 다른 사이트의 디자인을 참고해 내 프로젝트에 옮기는 작업은 보통 손으로 합니다. 개발자 도구를 열어 색상 값을 하나씩 복사하고, 폰트와 자간을 눈대중으로 맞추고, 간격과 그림자를 추정해 다시 토큰으로 정리합니다. 이 과정은 시간이 오래 걸릴 뿐 아니라 누락과 오차가 생기기 쉽고, 반응형 동작이나 상호작용 상태(hover, focus)처럼 정적 화면만 봐서는 알기 어려운 정보는 빠지기 마련입니다.  designlang은 이 작업을 명령 한 줄로 자동화하는 도구입니다. 헤드리스 브라우저(headless browser)를 임의의 URL에 띄워 살아있는 DOM에서 디자인 시스템을 직접 읽어내고, 한 번 실행으로 17개 이상의 파일을 생성합니다. W3C DTCG 디자인 토큰(Design Tokens), Tailwind 설정, shadcn 테마, Figma 변수, 모션...

---
[원본 보기](https://discuss.pytorch.kr/t/designlang-cli-ai/10494?u=j808esc)
