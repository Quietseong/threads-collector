---
title: "Gemma Gem은 브라우저에서 AI를 온디바이스로 실행하는 확장입니다."
source: discuss
author: ""
category: "개발/기술"
subcategory: "온디바이스 AI"
tags: ["GemmaGem", "WebGPU", "AI어시스턴트", "크롬확장", "온디바이스"]
confidence: 0.9
original_url: "https://discuss.pytorch.kr/t/gemma-gem-google-gemma-4-webgpu-ai/9660?u=j808esc"
collected_at: "2026-04-17T02:09:32.797413Z"
classified_at: "2026-04-17T02:09:36.826061Z"
---

# Gemma Gem은 브라우저에서 AI를 온디바이스로 실행하는 확장입니다.

> **출처**: discuss (PyTorchKR)
> **카테고리**: 개발/기술 > 온디바이스 AI

## 원문

Gemma Gem: Google의 Gemma 4 모델을 WebGPU로 브라우저에서 완전히 실행하는 온디바이스 AI 어시스턴트 크롬 확장

Gemma Gem 소개 ChatGPT나 Claude 같은 AI 어시스턴트를 브라우저에서 사용할 때, 입력한 모든 텍스트는 외부 서버로 전송됩니다. 민감한 정보가 포함된 웹 페이지를 분석하거나, 개인 데이터를 다루는 업무에 AI를 활용하고 싶을 때 이 점은 언제나 아쉬운 제약이었습니다. 특히 기업 내부 문서, 의료 기록, 법률 자료 등을 다루는 환경에서는 클라우드 기반 AI의 활용이 사실상 불가능한 경우도 많습니다.  Gemma Gem은 이 문제를 정면으로 해결하는 오픈소스 크롬 확장 프로그램입니다. Google의 Gemma 4 모델을 WebGPU를 통해 완전히 브라우저 내에서 실행함으로써, 사용자의 데이터가 단 한 바이트도 외부로 나가지 않는 온디바이스(On-Device) AI 환경을 구현합니다. API 키 없이, 클라우드 연결 없이, 오직 사용자의 GPU만으로 동작합니다. kessler가 개발한 이 프로젝트는 Apache-2.0 라이선스 하에 공개되어 있으며, Hugging ...

---
[원본 보기](https://discuss.pytorch.kr/t/gemma-gem-google-gemma-4-webgpu-ai/9660?u=j808esc)
