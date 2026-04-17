---
title: "LightRAG는 지식 그래프를 활용한 새로운 RAG 프레임워크입니다."
source: discuss
author: ""
category: "뉴스/트렌드"
subcategory: "AI 연구"
tags: ["LightRAG", "RAG", "지식그래프", "EMNLP2025", "검색증강생성"]
confidence: 0.9
original_url: "https://discuss.pytorch.kr/t/lightrag-graphrag-rag-feat-emnlp-2025/9612?u=j808esc"
collected_at: "2026-04-17T02:10:00.522196Z"
classified_at: "2026-04-17T02:10:04.639658Z"
---

# LightRAG는 지식 그래프를 활용한 새로운 RAG 프레임워크입니다.

> **출처**: discuss (PyTorchKR)
> **카테고리**: 뉴스/트렌드 > AI 연구

## 원문

LightRAG: 지식 그래프 기반의 이중 검색 구조로 GraphRAG보다 빠른 RAG 프레임워크 (feat. EMNLP 2025)

LightRAG 소개 대규모 언어 모델(LLM, Large Language Model)을 기업 내부 문서나 전문 지식과 결합하는 방식으로 검색 증강 생성(RAG, Retrieval-Augmented Generation)이 폭넓게 사용되고 있습니다. 그러나 전통적인 RAG 방식은 문서를 청크(chunk)로 나누어 벡터 데이터베이스에 저장하고, 질의와 유사한 청크를 검색해 LLM에 전달하는 구조로, 개별 청크 간의 연결성이나 문서 전체를 관통하는 개념적 관계를 파악하기 어렵다는 한계가 있습니다. 홍콩 대학교 데이터 사이언스(HKUDS) 연구팀은 이 문제를 해결하기 위해 지식 그래프(Knowledge Graph)와 벡터 검색을 결합한 LightRAG를 개발하였으며, 해당 연구는 EMNLP 2025에 발표되었습니다.     LightRAG는 기존 RAG의 청크 검색 방식을 넘어, 문서에서 자동으로 엔티티(entity)와 관계(relation)를 추출하여 지식 그래프를 구성합니다. 이렇...

---
[원본 보기](https://discuss.pytorch.kr/t/lightrag-graphrag-rag-feat-emnlp-2025/9612?u=j808esc)
