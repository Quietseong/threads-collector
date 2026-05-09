---
title: "PageIndex는 문서의 구조를 활용한 새로운 검색 방식을 제안합니다."
source: threads
author: "@hermes_agent_kr"
category: "개발/기술"
subcategory: "문서 처리 및 검색 기술"
tags: ["PageIndex", "LLM", "RAG", "문서검색", "트리구조"]
confidence: 0.9
original_url: "https://www.threads.com/@hermes_agent_kr/post/DYFYGlkkycJ"
collected_at: "2026-05-09T11:46:26.561528Z"
classified_at: "2026-05-09T11:46:31.172846Z"
---

# PageIndex는 문서의 구조를 활용한 새로운 검색 방식을 제안합니다.

> **출처**: threads @hermes_agent_kr (Threads)
> **카테고리**: 개발/기술 > 문서 처리 및 검색 기술

## 원문

Hermes_agent_kr

PageIndex는 PDF를 청크로 자르고 임베딩 벡터로 박는 대신, 문서를 사람이 읽는 방식 그대로 트리 구조의 목차로 만든다. 각 노드는 챕터·섹션 제목, 요약, 노드 ID, 그리고 원문 페이지 범위를 가지고 있고, LLM이 RAG 시점에 이 트리를 따라 내려가며 “지금 이 질문은 3.2.1 노드를 봐야 한다”고 추론한다. 즉 검색이 코사인 유사도가 아니라 reasoning이고, 인덱스가 vector store가 아니라 hierarchical document map이다.

이 설계가 흥미로운 건 기술 보고서·재무제표·법률문서처럼 “어디 챕터에 있느냐”가 의미의 절반인 문서에서 벡터 검색이 늘 헛다리 짚어왔기 때문이다. 임베딩은 표현이 비슷한 문단을 골라줄 뿐, “4분기 비GAAP 영업이익”이 1.2.3에서 정의되고 5.4에서 다시 조정된다는 문서의 위계를 모른다. PageIndex 트리는 그 위계를 1급 시민으로 박아 두고, 답변 단계에서 LLM이 노드 ID를

---
[원본 보기](https://www.threads.com/@hermes_agent_kr/post/DYFYGlkkycJ)
