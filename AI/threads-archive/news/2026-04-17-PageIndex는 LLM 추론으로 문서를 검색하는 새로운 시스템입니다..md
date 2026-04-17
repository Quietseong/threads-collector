---
title: "PageIndex는 LLM 추론으로 문서를 검색하는 새로운 시스템입니다."
source: discuss
author: ""
category: "뉴스/트렌드"
subcategory: "AI 및 머신러닝"
tags: ["PageIndex", "RAG", "LLM", "벡터DB", "청킹"]
confidence: 0.9
original_url: "https://discuss.pytorch.kr/t/pageindex-db-llm-rag/9579?u=j808esc"
collected_at: "2026-04-17T02:12:06.472077Z"
classified_at: "2026-04-17T02:12:08.371219Z"
---

# PageIndex는 LLM 추론으로 문서를 검색하는 새로운 시스템입니다.

> **출처**: discuss (PyTorchKR)
> **카테고리**: 뉴스/트렌드 > AI 및 머신러닝

## 원문

PageIndex: 벡터 DB와 청킹 없이 LLM 추론으로 문서를 검색하는 계층형 인덱스 기반 RAG 시스템

PageIndex 소개 검색 증강 생성(RAG, Retrieval-Augmented Generation) 시스템의 가장 큰 도전 중 하나는 문서를 어떻게 분할하고 검색할 것인가의 문제입니다. 기존의 벡터 기반 RAG 시스템은 문서를 임의의 크기로 분할(청킹, Chunking)한 뒤 임베딩 벡터로 변환하여 검색하는 방식을 사용합니다. 그러나 이 방식은 자연스러운 문서 구조를 무시하고, 의미적으로 연관된 내용을 단절시키는 문제를 내포하고 있습니다. PageIndex는 이 문제를 근본적으로 다른 방식으로 해결합니다. 벡터 데이터베이스를 전혀 사용하지 않고, LLM의 추론 능력을 활용하여 인간과 유사한 방식으로 문서를 검색하는 시스템입니다.  PageIndex는 VectifyAI 팀이 개발한 오픈소스 프로젝트로, "Reasoning-based RAG(추론 기반 RAG)"라는 새로운 패러다임을 제안합니다. 핵심 아이디어는 문서를 목차(Table of Contents)와 유사한 계층형 트...

---
[원본 보기](https://discuss.pytorch.kr/t/pageindex-db-llm-rag/9579?u=j808esc)
